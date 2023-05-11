# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

import pytz

from odoo import fields, _
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_event_track.controllers.event_track import EventTrackController


class EventTrackController(EventTrackController):


    def _prepare_calendar_values(self, event):
        """ This methods allows to calculate the number of tracks by days if slots
        configurated in track event. """
        res = super(EventTrackController, self)._prepare_calendar_values(event)
        days = res["days"]

        event = event.with_context(tz=event.date_tz or 'UTC')
        local_tz = pytz.timezone(event.date_tz or 'UTC')

        base_track_domain = expression.AND([
            self._get_event_tracks_agenda_domain(event),
            [('date', '!=', False)]
        ])
        tracks_sudo = request.env['event.track'].sudo().search(base_track_domain)

        # count the number of tracks by days
        tracks_by_days = dict.fromkeys(days, 0)

        for track in tracks_sudo:
            for slot in track.event_track_slot_ids:
                track_day = fields.Datetime.from_string(slot.date).replace(tzinfo=pytz.utc).astimezone(local_tz).date()
                tracks_by_days[track_day] += 1

        res["tracks_by_days"] = tracks_by_days
        return res

    def _split_track_slot_by_days(self, slot, local_tz):
        """
        Based on the track slot date and the duration,
        split the track duration into :
            start_time by day : number of time slot (15 minutes) that the track takes on that day.
        E.g. :  start date = 01-01-2000 10:00 PM and duration = 3 hours
                return {
                    01-01-2000 10:00:00 PM: 8 (2 * 4),
                    01-02-2000 00:00:00 AM: 4 (1 * 4)
                }
        Also return a set of all the time slots
        """
        start_date = fields.Datetime.from_string(slot.date).replace(tzinfo=pytz.utc).astimezone(local_tz)
        start_datetime = self.time_slot_rounder(start_date, 15)
        end_datetime = self.time_slot_rounder(
            start_datetime + timedelta(hours=(slot.duration or 0.25)), 15)
        time_slots_count = int(
            ((end_datetime - start_datetime).total_seconds() / 3600) * 4)

        time_slots_by_day_start_time = {start_datetime: 0}
        for i in range(0, time_slots_count):
            # If the new time slot is still on the current day
            next_day = (start_datetime + timedelta(days=1)).date()
            if (start_datetime + timedelta(minutes=15 * i)).date() <= next_day:
                time_slots_by_day_start_time[start_datetime] += 1
            else:
                start_datetime = next_day.datetime()
                time_slots_by_day_start_time[start_datetime] = 0

        return time_slots_by_day_start_time

    def _split_track_by_days(self, track, local_tz):
        """
        Function inherited and allow to manage slots tracks
        """
        if track.is_slot_management:
            time_slots_by_tracks = {}
            for slot in track.event_track_slot_ids:
                time_slots_by_tracks.update(self._split_track_slot_by_days(slot, local_tz))
            return time_slots_by_tracks

        else:
            return super(EventTrackController, self)._split_track_by_days(track, local_tz)
