# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import http
from odoo.http import request

from odoo.addons.website_event.controllers.main import WebsiteEventController

_logger = logging.getLogger(__name__)


class WebsiteEvent(WebsiteEventController):
    @http.route()
    def registration_confirm(self, event, **post):
        if event.unique_attendee_email:
            registrations = self._process_attendees_form(event, post)
            emails = [r.get("email") for r in registrations]
            attendee_ids = event.sudo().registration_ids.filtered(
                lambda a: a.email in emails
            )
            if attendee_ids:
                attendee_email = attendee_ids.mapped("email")
                values = self._prepare_event_register_values(event, **post)
                values.update(
                    {
                        "error": "This users are already registered: %s"
                        % ", ".join(attendee_email)
                    }
                )
                return request.render("website_event.event_description_full", values)

        return super(WebsiteEvent, self).registration_confirm(event, **post)
