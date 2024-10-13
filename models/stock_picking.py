# models/stock_picking.py

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Analytic Accounts'
    )
    

    def button_validate(self):
        res = super(StockPicking, self).button_validate()

        for picking in self:
            if picking.picking_type_id.code == 'internal' and picking.location_dest_id.usage == 'production':
                # Validar que se ingresen exactamente 2 cuentas analíticas
                if len(picking.analytic_account_ids) != 2:
                    raise UserError("Error: Se deben ingresar dos cuentas analíticas (Centro de Costo y Proyecto) para continuar con la validación.")

                # Validar que las cuentas analíticas sean de distintos planes analíticos
                analytic_plans = picking.analytic_account_ids.mapped('plan_id')
                if len(set(analytic_plans)) != 2:
                    raise UserError("Error: Las dos cuentas analíticas deben ser de distintos planes analíticos.")

                for move in picking.move_ids:
                    move.analytic_account_ids = picking.analytic_account_ids
                    for move_line in move.move_line_ids:
                        move_line.analytic_account_ids = picking.analytic_account_ids

                    account_move = move.account_move_ids[:1]
                    if account_move:
                        account_move.sudo()
                        for line in account_move.line_ids:
                            analytic_distribution = {analytic_account.id: 100 for analytic_account in picking.analytic_account_ids}

                            # Distribuir en la cuenta principal
                            if picking.location_id.usage == 'production' and line.debit != 0.0:
                                line.sudo().write({
                                    'analytic_distribution': analytic_distribution
                                })
                            elif picking.location_dest_id.usage == 'production' and line.credit != 0.0:
                                line.sudo().write({
                                    'analytic_distribution': analytic_distribution
                                })

                            # Distribuir en la contracuenta
                            contra_line = account_move.line_ids.filtered(lambda l: l.account_id.id != line.account_id.id and l.id != line.id)
                            if contra_line:
                                contra_line.sudo().write({
                                    'analytic_distribution': analytic_distribution
                                })

        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Analytic Accounts'
    )

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Analytic Accounts'
    )
