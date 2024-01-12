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

    def _avior_tax_prepare_lines(self):
        """
        Prepare the lines to use for Avior Tax computation.
        Returns a list of dicts
        """
        sign = 1 if self.move_type.startswith("out") else -1
        lines = [
            line._avior_tax_prepare_line(sign=sign)
            for line in self.invoice_line_ids
            if line.price_subtotal or line.quantity
        ]
        return [x for x in lines if x]

    def _avior_tax_compute_tax(self):
        if not self:
            return
        self.ensure_one()
        avior_tax_config = self.env.company.get_avior_tax_config()
        if not avior_tax_config:
            return

        taxable_lines = self._avior_tax_prepare_lines()

        if len(taxable_lines) == 0:
            return

        tax_results = avior_tax_config.calculate_tax(
            doc_date=self.invoice_date or fields.Date.today(),
            lines=taxable_lines,
            shipping_address=self.partner_id,
        )

        if self.state == "draft":
            taxes_to_set = []
            tax_result_lines = {int(x.record_number): x for x in tax_results}
            for index, line in enumerate(self.invoice_line_ids):
                tax_result_line = tax_result_lines.get(line.id)
                if not tax_result_line:
                    continue
                for tax in tax_result_line.taxes:
                    tax_id = self.env["account.tax"].get_avior_tax(tax.fips_tax_rate)
                    if tax_id and tax_id not in line.tax_ids:
                        line_tax_ids = line.tax_ids.filtered(lambda x: not x.is_avatax)
                        taxes_to_set.append((index, line_tax_ids | tax_id))
                line.avior_amt_line = tax_result_line.tax_amount

            self.with_context(check_move_validity=False).avior_amount = sum(
                x.tax_amount for x in tax_results
            )

            container = {"records": self}
            self.with_context(
                avior_invoice=self, check_move_validity=False
            )._sync_dynamic_lines(container)
            self.line_ids.mapped("move_id")._check_balanced(container)

            # Set Taxes on lines in a way that properly triggers onchanges
            # This same approach is also used by the official account_taxcloud connector
            with Form(self) as move_form:
                for index, taxes in taxes_to_set:
                    with move_form.invoice_line_ids.edit(index) as line_form:
                        line_form.tax_ids.clear()
                        for tax in taxes:
                            line_form.tax_ids.add(tax)

        return tax_results

    def avior_tax_compute_taxes(self):
        """
        Computes the taxes for the invoice using the Avior Tax API.
        It's also called from Invoice's Action menu to force computation of the Invoice taxes.
        """
        for invoice in self:
            if (
                invoice.move_type
                in [
                    "out_invoice",
                    "out_refund",
                ]  # only Customer Invoice and Customer Credit Note
                and invoice.fiscal_position_id.is_avior  # only if Avior Tax is enabled
                and (invoice.state == "draft")
            ):
                invoice._avior_tax_compute_tax()
        return True

    def is_avior_calculated(self):
        """
        Only apply Avior Tax for these types of documents.
        Can be extended to support other types.
        """
        return self.is_sale_document()

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        for invoice in res:
            if invoice.is_avior_calculated():
                invoice.avior_tax_compute_taxes()
        return res

    def _reverse_move_vals(self, default_values, cancel=True):
        # OVERRIDE
        # Don't keep anglo-saxon lines if not cancelling an existing invoice.
        move_vals = super()._reverse_move_vals(default_values, cancel=cancel)
        move_vals.update(
            {
                "invoice_date": self.invoice_date,
            }
        )
        return move_vals

    def write(self, vals):
        result = super().write(vals)
        for record in self:
            if record.state == "draft" and not self._context.get(
                "skip_second_write", False
            ):
                record.with_context(skip_second_write=True).write(
                    {"calculate_tax_on_save": False}
                )
                record.avior_tax_compute_taxes()
        return result

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if not self._context.get("skip_second_write", False):
            record.with_context(skip_second_write=True).write(
                {"calculate_tax_on_save": False}
            )
            record.avior_tax_compute_taxes()
        return record


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
