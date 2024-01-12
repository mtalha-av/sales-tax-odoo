from math import copysign
from odoo import exceptions, fields, models, api, _
from odoo.tools import float_compare


class AccountTax(models.Model):
    """Inherit to implement the tax using Avior Tax API"""

    _inherit = "account.tax"

    is_avior = fields.Boolean()

    @api.model
    def get_avior_tax(self, tax_rate):
        """
        Returns the Avior Tax record for the given tax rate.
        If the record does not exist, it creates it from the Avior Tax template.
        """
        domain = [
            ("amount", "=", tax_rate),
            ("is_avior", "=", True),
            ("company_id", "=", self.env.company.id),
        ]
        tax = self.with_context(active_test=False).search(domain, limit=1)
        if tax and not tax.active:
            tax.active = True
        if not tax:
            domain = [
                ("amount", "=", 0),
                ("is_avior", "=", True),
                ("company_id", "=", self.env.company.id),
            ]
            tax_template = self.search(domain, limit=1)
            if not tax_template:
                raise exceptions.UserError(
                    _("Please configure Avior Tax for Company %s:")
                    % self.env.company.name
                )
            # If you get a unique constraint error here,
            # check the data for your existing Avior taxes.
            vals = {
                "amount": tax_rate,
                "name": _("{}%*").format(str(tax_rate)),
            }
            tax = tax_template.sudo().copy(default=vals)
            # Odoo core does not use the name set in default dict
            tax.name = vals.get("name")
        return tax

    def compute_all(
        self,
        price_unit,
        currency=None,
        quantity=1.0,
        product=None,
        partner=None,
        is_refund=False,
        handle_price_include=True,
        include_caba_tags=False,
        fixed_multiplicator=1,
    ):
        """
        Adopted as the central point to inject custom tax computations.
        Avior Tax logic is triggered if the "avior_invoice" is set in the context.
        To find the Avior amount, we search an Invoice line with the same
        quantity, price and product.
        """
        res = super().compute_all(
            price_unit,
            currency,
            quantity,
            product,
            partner,
            is_refund,
            handle_price_include,
            include_caba_tags=False,
            fixed_multiplicator=1,
        )
        avior_invoice = self.env.context.get("avior_invoice")

        if not avior_invoice:
            return res

        # Find the Avior amount in the invoice Lines
        # Looks up the line for the current product, price_unit, and quantity
        # Note that the price_unit used must consider discount
        base = res["total_excluded"]
        digits = 6
        avior_line_amount = None
        for line in avior_invoice.invoice_line_ids:
            price_unit = line.currency_id._convert(
                price_unit,
                avior_invoice.company_id.currency_id,
                avior_invoice.company_id,
                avior_invoice.date,
            )
            if (
                line.product_id == product
                and float_compare(line.quantity, quantity, digits) == 0
            ):
                avior_line_amount = copysign(line.avior_amt_line, base)
                break
        if avior_line_amount is None:
            avior_line_amount = 0.0
            raise exceptions.UserError(
                _(
                    "Incorrect retrieval of Avior amount for Invoice %(avior_invoice)s:"
                    " product %(product.display_name)s, price_unit %(-price_unit)f"
                    " , quantity %(quantity)f"
                )
            )
        for tax_item in res["taxes"]:
            if tax_item["amount"] != 0:
                tax_item["amount"] = avior_line_amount
        res["total_included"] = base + avior_line_amount
        return res
