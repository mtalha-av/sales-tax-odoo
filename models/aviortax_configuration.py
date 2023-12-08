import logging

from odoo import fields, models


_logger = logging.getLogger(__name__)


class AviortaxConfiguration(models.Model):
    _name = "aviortax.configuration"
    _description = "Avior Tax Configuration"

    company_name = fields.Char(
        string="Company Name",
        help="The company name to connect with",
    )

    username = fields.Char(required=True, help="Avior username")
    password = fields.Char(required=True, help="Avior password")
    service_url = fields.Char(
        string="Service URL",
        help="The url to connect with",
    )

    token = fields.Char(
        string="Token",
        help="The token to connect with",
    )

    seller_id = fields.Char(
        string="Seller ID",
        help="The seller id to connect with",
    )
    seller_location_id = fields.Char(
        string="Seller Location ID",
        help="The seller location id to connect with",
    )
    seller_state = fields.Char(
        string="Seller State",
        help="The seller state to connect with",
    )
    customer_entity_code = fields.Char(
        string="Customer Entity Code",
        help="The customer entity code to connect with",
    )
