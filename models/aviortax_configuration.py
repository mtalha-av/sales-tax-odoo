import logging

from odoo import fields, models
from ..api.aviortax_v1_client import AviortaxV1Client
from ..api.dtos import Input

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

    def calculate_tax(self, doc_date, lines, shipping_address):
        avior = AviortaxV1Client(
            service_url=self.service_url,
            auth_token=self.token,
        )
        prepared_lines = [
            Input.Product(
                date=doc_date.strftime("%Y%m%d"),
                record_number=str(line.get("id").id),
                seller_id=self.seller_id,
                seller_location_id=self.seller_location_id,
                seller_state=self.seller_state,
                customer_entity_code=self.customer_entity_code,
                delivery_method="N",
                ship_to_address=shipping_address.street,
                ship_to_suite="",
                ship_to_city=shipping_address.city,
                ship_to_county=shipping_address.county,  #  FIXME: county is not a field on res.partner
                ship_to_state=shipping_address.state_id.code,
                ship_to_zip_code=shipping_address.zip,
                ship_to_zip_plus="",
                sku=line.get("sku"),
                amount_of_sale=line.get("amount", 0.0),
            )
            for line in lines
        ]

        result = avior.get_tax(prepared_lines)
        return result

    def login(self):
        """Login to Avior Tax"""
        authToken = AviortaxV1Client.login(
            service_url=self.service_url, username=self.username, password=self.password
        )
        self.write({"token": authToken})
        return True
