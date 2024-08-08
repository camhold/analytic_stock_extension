from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Analytic Accounts'
    )

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account',
        string='Analytic Accounts'
    )
