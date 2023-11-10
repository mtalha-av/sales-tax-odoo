from odoo import fields, models


class AccountTax(models.Model):
    """Inherit to implement the tax using Avior Tax API"""

    _inherit = "account.tax"

    is_avior = fields.Boolean()
