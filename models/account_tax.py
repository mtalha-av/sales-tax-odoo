from odoo import exceptions, fields, models, api, _


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
