# © 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Event Private",
    "summary": "Website Event Private",
    "version": "16.0.1.0.0",
    "author": "Odoo Community Association (OCA),Le Filament",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "application": False,
    "category": "Marketing",
    "depends": ["website_event"],
    "data": [
        "templates/event_templates_list.xml",
        "views/event_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_event_private/static/src/scss/website_event_private.scss",
        ],
    },
    "installable": True,
    "auto_install": False,
}
