from odoo import api, fields, models


class AviortaxConfigurationLogin(models.TransientModel):
    _name = "aviortax.configuration.login"
    _description = "Login Service"

    name = fields.Char()

    @api.model
    def login(self):
        """Get Token from Aviortax."""
        active_id = self.env.context.get("active_id")
        if active_id:
            avatax = self.env["aviortax.configuration"].browse(active_id)
            avatax.login()
        return True
