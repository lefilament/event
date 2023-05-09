# © 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Event Track slots",
    "summary": "Website Event Track Slots",
    "version": "16.0.1.0.0",
    "author": "Odoo Community Association (OCA),Le Filament",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/event",
    "application": False,
    "category": "Marketing",
    "depends": ["website_event", "website_event_track"],
    "data": [
        "security/ir.model.access.csv",
        # "templates/event_templates.xml",
        "views/event_track_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
