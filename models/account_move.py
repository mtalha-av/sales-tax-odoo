from odoo import models, api, fields
from odoo.tests.common import Form


class AccountMove(models.Model):
    _inherit = "account.move"

    is_avior = fields.Boolean(related="fiscal_position_id.is_avior")
    avior_amount = fields.Float(string="Avior", copy=False)
    tax_on_shipping_address = fields.Boolean(
        "Tax based on shipping address", default=True
    )

    @api.depends(
        "line_ids.debit",
        "line_ids.credit",
        "line_ids.currency_id",
        "line_ids.amount_currency",
        "line_ids.amount_residual",
        "line_ids.amount_residual_currency",
        "line_ids.payment_id.state",
        "avior_amount",
    )
    def _compute_amount(self):
        res = super()._compute_amount()
        for inv in self:
            if not inv.avior_amount:
                continue
            inv.amount_tax = abs(inv.avior_amount)
            inv.amount_total = inv.amount_untaxed + inv.amount_tax
            sign = inv.move_type in ["in_refund", "out_refund"] and -1 or 1
            inv.amount_total_signed = inv.amount_total * sign
        return res
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
