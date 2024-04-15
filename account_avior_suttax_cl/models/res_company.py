import logging

from odoo import _, models

_LOGGER = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = "res.company"

    def get_avior_tax_config(self):
        """Returns the Avior Tax configuration for the Company. Should only be one."""
        if not self:
            return

        self.ensure_one()
        res = self.env["aviortax.configuration"].search(
            [("company_id", "=", self.id), ("enabled", "=", True)],
            limit=2,
        )
        if len(res) > 1:
            _LOGGER.warning(
                _(
                    "Company %s has too many Avior Tax configurations! Disable or delete the ones you don't need."
                ),
                self.display_name,
            )
        if len(res) < 1:
            _LOGGER.warning(
                _(
                    "Company %s has no Avior Tax configuration. Please create one in the Avior Tax Configuration Section."
                ),
                self.display_name,
            )
        return res and res[0]
