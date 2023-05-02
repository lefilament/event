# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import uuid

from odoo import fields, models, _, api


class Event(models.Model):
    _inherit = 'event.event'
    # ------------------------------------------------------
    # Fields declaration
    # ------------------------------------------------------
    access_token = fields.Char("Security Token", copy=False)
    event_share_link = fields.Char(
        string="Lien de partage client",
        compute="_compute_event_share_link",
    )

    type_event = fields.Selection([
        ("public", "Public"),
        ("private", "Privé")
    ], string="Type d'évènements")
    # ------------------------------------------------------
    # SQL Constraints
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Default methods
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Computed fields / Search Fields
    # ------------------------------------------------------
    def _compute_event_share_link(self):
        for event in self:
            if event.id and event.access_token and event.type_event == "private":
                event.event_share_link = (
                    event.get_base_url()
                    + "/event/"
                    + str(event.id)
                    + "?access_token="
                    + event.access_token
                )
            else:
                event.event_share_link = ""
    # ------------------------------------------------------
    # Onchange / Constraints
    # ------------------------------------------------------

    # ------------------------------------------------------
    # CRUD methods (ORM overrides)
    # ------------------------------------------------------
    @api.model
    def create(self, vals):
        vals["access_token"] = str(uuid.uuid4())
        return super(Event, self).create(vals)

    # ------------------------------------------------------
    # Actions
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Business methods
    # ------------------------------------------------------
