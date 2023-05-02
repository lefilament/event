# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.http import request
from odoo import http

from odoo.addons.website_event.controllers.main import WebsiteEventController

_logger = logging.getLogger(__name__)


class WebsiteEvent(WebsiteEventController):

    @http.route(['''/event/<model("event.event"):event>/page/<path:page>'''], type='http', auth="public", website=True, sitemap=False)
    def event_page(self, event, page, **post):
        if event.type_event == "private":
            access_token = post.get('access_token') or False
            if not access_token or access_token != event.access_token:
                _logger.warning("Access denied to event %s" % event.name)
                return request.redirect("/event")
        return super(WebsiteEvent, self).event_page(event, page, **post)

    @http.route(['''/event/<model("event.event"):event>'''], type='http', auth="public", website=True, sitemap=True)
    def event(self, event, **post):
        if event.type_event == "private":
            access_token = post.get('access_token') or False
            if not access_token or access_token != event.access_token:
                _logger.warning("Access denied to event %s" % event.name)
                return request.redirect("/event")
            else:
                res = super(WebsiteEvent, self).event(event, **post)
                target_url = '/event/%s/register?access_token=%s' % (str(event.id), access_token)
                return request.redirect(target_url)
        return super(WebsiteEvent, self).event(event, **post)

    @http.route(['''/event/<model("event.event"):event>/register'''], type='http', auth="public", website=True, sitemap=False)
    def event_register(self, event, **post):
        if event.type_event == "private":
            access_token = post.get('access_token') or False
            if not access_token or access_token != event.access_token:
                _logger.warning("Access denied to event %s" % event.name)
                return request.redirect("/event")
        return super(WebsiteEvent, self).event_register(event, **post)
