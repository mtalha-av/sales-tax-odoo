from odoo import models, api, fields
from odoo.tests.common import Form


class AccountMove(models.Model):
    _inherit = "account.move"

    is_avior = fields.Boolean(related="fiscal_position_id.is_avior")
    avior_amount = fields.Float(string="Avior", copy=False)
    tax_on_shipping_address = fields.Boolean(
        "Tax based on shipping address", default=True
    )

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
