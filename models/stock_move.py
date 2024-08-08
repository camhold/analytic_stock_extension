from odoo import models, fields

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
