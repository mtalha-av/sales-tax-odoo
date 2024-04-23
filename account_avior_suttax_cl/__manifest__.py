{
    "name": "Avior SutTax",
    "version": "16.0.0.0.4",
    "author": "Avior, Collins Lagat",
    "summary": "Compute Sales Tax in the United States using the Avior Tax API",
    "description": "Compute Sales Tax in the United States using the Avior Tax API",
    "license": "AGPL-3",
    "category": "Accounting",
    "website": "https://avior.tax",
    "depends": ["account", "sale", "base_geolocalize"],
    "data": [
        "security/ir.model.access.csv",
        "data/aviortax_data.xml",
        "wizard/aviortax_configuration_login_view.xml",
        "views/aviortax_view.xml",
        "views/partner_view.xml",
        "views/account_move_action.xml",
        "views/account_move_view.xml",
        "views/account_tax_view.xml",
        "views/account_fiscal_position_view.xml",
    ],
    "images": ["static/description/invoice_screenshot.png"],
    "installable": True,
    "application": True,
}
