{
    "name": "Questions on Events - Type multiple",
    "version": "16.0.1.0.0",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "development_status": "Production/Stable",
    "author": "Le Filament, Odoo Community Association (OCA), Odoo",
    "license": "LGPL-3",
    "application": False,
    "depends": ["website_event_questions"],
    "data": [
        "templates/event_template.xml",
        "views/event_questions_views.xml",
        "views/event_registration_views.xml",
    ],
    "assets": {
        "web.assets_frontend": ["website_event_questions_multiple/static/src/**/*"],
    },
    "installable": True,
    "auto_install": False,
}
