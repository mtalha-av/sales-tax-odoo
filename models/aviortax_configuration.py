import logging

from odoo import fields, models
from ..api.aviortax_v1_client import AviortaxV1Client

_logger = logging.getLogger(__name__)


class AviortaxConfiguration(models.Model):
    _name = "aviortax.configuration"
    _description = "Avior Tax Configuration"

    # Fields
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        help="Company which has do you want to connect with",
    )
    username = fields.Char(string="Username", required=True, help="Avior username")
    password = fields.Char(string="Password", required=True, help="Avior password")
    service_url = fields.Char(
        string="Service URL", required=True, help="The url to connect with"
    )
    token = fields.Char(string="Token", readonly=True, help="The token to connect with")
    seller_id = fields.Char(string="Seller ID", help="The seller id to connect with")
    seller_location_id = fields.Char(
        string="Seller Location ID", help="The seller location id to connect with"
    )
    seller_state = fields.Char(
        string="Seller State", help="The seller state to connect with"
    )
    customer_entity_code = fields.Char(
        string="Customer Entity Code", help="The customer entity code to connect with"
    )
    enabled = fields.Boolean(
        "Enabled",
        default=True,
        help="Set to false to disable this Avior Tax configuration without deleting it.",
    )

    # Methods

    def login(self):
        """Login to Avior Tax"""
        authToken = AviortaxV1Client.login(
            service_url=self.service_url, username=self.username, password=self.password
        )
        self.write({"token": authToken})
        return True
