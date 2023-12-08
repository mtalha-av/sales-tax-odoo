{
    "name": "Avior Tax API Integration",
    "version": "0.0.1",
    "author": "Collins Lagat",
    "description": "Compute Sales Tax in the United States using the Avior Tax API",
    "license": "LGPL-3",
    "category": "Accounting",
    "website": "https://collinslagat.com",
    "depends": ["account", "sale", "base_geolocalize"],
    "data": [
        "security/ir.model.access.csv",
        "data/aviortax_data.xml",
        "views/aviortax_view.xml",
    ],
    "installable": True,
    "application": True,
}
