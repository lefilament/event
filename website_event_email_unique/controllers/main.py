# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import _
from odoo.exceptions import UserError

from odoo.addons.website_event.controllers.main import WebsiteEventController

_logger = logging.getLogger(__name__)


class WebsiteEvent(WebsiteEventController):

    def _process_attendees_form(self, event, form_details):
        """ Process data posted from the attendee details form.

        :param form_details: posted data from frontend registration form, like
            {'1-name': 'r', '1-email': 'r@r.com', '1-phone': '', '1-event_ticket_id': '1'}
        """
        res = super(WebsiteEvent, self)._process_attendees_form(event, form_details)
        emails = [r.get("email") for r in res]
        attendee_ids = event.sudo().registration_ids.filtered(
            lambda a: a.email in emails
        )
        if attendee_ids:
            attendee_email = attendee_ids.mapped("email")
            raise UserError(_("This users are already registered: %s"))

        return res
    #     allowed_fields = request.env['event.registration']._get_website_registration_allowed_fields()
    #     registration_fields = {key: v for key, v in request.env['event.registration']._fields.items() if key in allowed_fields}
    #     for ticket_id in list(filter(lambda x: x is not None, [form_details[field] if 'event_ticket_id' in field else None for field in form_details.keys()])):
    #         if int(ticket_id) not in event.event_ticket_ids.ids and len(event.event_ticket_ids.ids) > 0:
    #             raise UserError(_("This ticket is not available for sale for this event"))
    #
    # @http.route()
    # def registration_confirm(self, event, **post):
    #     if event.unique_attendee_email:
    #         registrations = self._process_attendees_form(event, post)
    #         emails = [r.get("email") for r in registrations]
    #         attendee_ids = event.sudo().registration_ids.filtered(
    #             lambda a: a.email in emails
    #         )
    #         if attendee_ids:
    #             attendee_email = attendee_ids.mapped("email")
    #             values = self._prepare_event_register_values(event, **post)
    #             values.update(
    #                 {
    #                     "error": "This users are already registered: %s"
    #                     % ", ".join(attendee_email)
    #                 }
    #             )
    #             return request.render("website_event.event_description_full", values)
    #
    #     return super(WebsiteEvent, self).registration_confirm(event, **post)
