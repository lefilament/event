# Copyright 2023 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class EventTicket(models.Model):
    _inherit = "event.event.ticket"

    max_ticket = fields.Integer(string="Max by order", default=0)

    # ------------------------------------------------------
    # Computed fields / Search Fields
    # ------------------------------------------------------
