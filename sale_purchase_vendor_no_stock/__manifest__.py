#  GNU nano 6.2
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Purchase Vendor No Stock",
    "version": "17.0.1.0.0",
    "category": "Category",
    "website": "https://github.com/OCA/purchase-workflow",
    "author": "<Odoo Community Association (OCA)>",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "sale", "purchase"],
    "data": [
        "views/res_config_settings_view.xml",
        "views/sale_order_view.xml",
    ],
}
