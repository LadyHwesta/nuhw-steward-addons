# -*- coding: utf-8 -*-
from odoo import fields, models


class NuhwDirectAction(models.Model):
    _name = "nuhw.direct_action"
    _description = "NUHW Direct Action"
    _inherit = ["mail.thread"]
    _order = "date desc"

    name = fields.Char(required=True)
    action_type = fields.Selection(
        [("informational_picket", "Informational Picket"),
         ("rally", "Rally"),
         ("petition", "Petition"),
         ("button_day", "Button Day"),
         ("know_your_rights", "Know-Your-Rights Training"),
         ("press", "Press Action"),
         ("other", "Other")],
        required=True, tracking=True)
    date = fields.Datetime(tracking=True)
    unit_ids = fields.Many2many("nuhw.unit", string="Units")
    organizer_id = fields.Many2one(
        "res.partner", string="Organizer",
        domain=[("is_steward", "=", True)])
    participant_ids = fields.Many2many(
        "res.partner", "nuhw_direct_action_participant_rel",
        "action_id", "partner_id", string="Participants")
    state = fields.Selection(
        [("planned", "Planned"),
         ("completed", "Completed"),
         ("cancelled", "Cancelled")],
        default="planned", tracking=True)
    notes = fields.Text()
