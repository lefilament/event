# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Event(models.Model):
    _inherit = "event.event"

    unique_attendee_email = fields.Boolean(
        string="Unique registation email", default=False
    )
