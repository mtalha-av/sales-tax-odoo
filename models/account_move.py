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
        """
        Compute the amount fields for the invoice.

        This method overrides the parent method to calculate the amount fields for the invoice.
        It takes into account various factors such as debit, credit, currency, payment state,
        and avior amount.
        """

        res = super()._compute_amount()
        for inv in self:
            if not inv.avior_amount:
                continue
            inv.amount_tax = abs(inv.avior_amount)
            inv.amount_total = inv.amount_untaxed + inv.amount_tax
            sign = inv.move_type in ["in_refund", "out_refund"] and -1 or 1
            inv.amount_total_signed = inv.amount_total * sign
        return res

    @api.onchange("fiscal_position_id")
    def onchange_reset_avior_amount(self):
        """
        Reset the Avior Tax computed amount when changing the fiscal position.

        This method is triggered when the fiscal position of an invoice is changed.
        It resets the Avior Tax computed amount to 0 and resets the invoice lines accordingly.

        The Odoo computed tax amount will then be shown, as a reference.
        The Avior Tax amount will be recomputed upon document validation.
        """
        for inv in self:
            inv.avior_amount = 0
            for line in inv.invoice_line_ids:
                line.avior_amt_line = 0
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    avior_amt_line = fields.Float(string="Avior Line", copy=False)

    def _get_avior_tax_amount(self):
        """
        Return the company currency line amount, after discounts,
        to use for Tax calculation.

        Can be used to compute unit price only, using qty=1.

        Code extracted from account/models/account_move.py,
        from the compute_base_line_taxes() nested function,
        adjusted to compute line amount instead of unit price.
        """
        self.ensure_one()
        move = self.move_id
        sign = -1 if move.is_inbound() else 1
        base_amount = self.price_unit * self.quantity
        if self.currency_id:
            price_unit_foreign_curr = sign * base_amount * (1 - (self.discount / 100.0))
            price_unit_comp_curr = self.currency_id._convert(
                price_unit_foreign_curr,
                move.company_id.currency_id,
                move.company_id,
                move.date,
            )
        else:
            price_unit_comp_curr = sign * base_amount * (1 - (self.discount / 100.0))
        return -price_unit_comp_curr

    def _avior_tax_prepare_line(self, sign=1):
        """
        Prepare a line to use for Avior Tax computation.
        Returns a dict
        """
        res = {}
        amount = sign * self._get_avior_tax_amount()
        if self.quantity < 0:
            amount = -amount
        res = {"sku": self.product_id.default_code, "amount": amount, "id": self}
        return res
