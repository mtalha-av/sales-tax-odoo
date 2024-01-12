from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    county = fields.Char(
        string="County",
        help="The county where the company is located. Required for use with Avior Tax.",
    )
