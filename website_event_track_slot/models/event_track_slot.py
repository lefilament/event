# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import api, fields, models


class TrackSlot(models.Model):
    """ Table linking track and slots. """
    _name = 'event.track.slot'
    _description = 'Track Slots'

    track_id = fields.Many2one(
        "event.track", string="Track",
        index=True, required=True, ondelete="cascade")
    date = fields.Datetime("Date start track slot")
    date_end = fields.Datetime("Track slot End Date", compute='_compute_end_date',
                               store=True)
    duration = fields.Float('Duration', default=0.5, help="Track slot duration in hours.")
    # ------------------------------------------------------
    # SQL Constraints
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Default methods
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Computed fields / Search Fields
    # ------------------------------------------------------
    @api.depends("date", "duration")
    def _compute_end_date(self):
        for slot in self:
            if slot.date:
                delta = timedelta(minutes=60 * slot.duration)
                slot.date_end = slot.date + delta
            else:
                slot.date_end = False

    # ------------------------------------------------------
    # Onchange / Constraints
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CRUD methods (ORM overrides)
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Actions
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Business methods
    # ------------------------------------------------------
