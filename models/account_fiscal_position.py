from odoo import fields, models


class FiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    is_avior = fields.Boolean(string="Use Avior Tax")
