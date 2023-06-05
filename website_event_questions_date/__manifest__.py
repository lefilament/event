# © 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Questions on Events - Type date",
    "summary": "Questions on Events - Type date",
    "version": "16.0.1.0.0",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Odoo Community Association (OCA),Le Filament",
    "license": "AGPL-3",
    "application": False,
    "depends": ["website_event_questions"],
    "data": [
        "templates/event_template.xml",
        "views/event_questions_views.xml",
        "views/event_registration_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
