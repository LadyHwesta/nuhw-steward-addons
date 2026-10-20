# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models

# Article 7.3 / 28.4 - both sides get the same 48-hour advance-notice window
# (the steward's release request, and the Hospital's investigatory-meeting
# notice). Kept as one named constant so both reference the same number.
RELEASE_NOTICE_HOURS = 48


class NuhwWeingartenMeeting(models.Model):
    _name = "nuhw.weingarten_meeting"
    _description = "NUHW Weingarten Meeting"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "scheduled_date desc"

    partner_id = fields.Many2one(
        "res.partner", string="Employee", required=True, tracking=True,
        help="The employee being interviewed.")
    steward_ids = fields.Many2many(
        "res.partner", string="Steward(s) Representing",
        domain=[("is_steward", "=", True)], tracking=True)
    management_rep = fields.Char(
        string="Management Representative(s)",
        help="Name/title of whoever from Hospital management is present - "
             "not tracked as a partner since management reps aren't union "
             "members.")
    unit_id = fields.Many2one("nuhw.unit", string="Unit")
    subject = fields.Char(help="Reason for the interview.")
    request_date = fields.Datetime(
        string="Release Requested On",
        help="When the steward's release was requested (Article 7.3: at "
             "least 48 hours before the meeting).")
    scheduled_date = fields.Datetime(tracking=True)
    release_requested_late = fields.Boolean(
        compute="_compute_release_requested_late", store=True,
        help="True if the release request came less than 48 hours before "
             "the scheduled meeting (Article 7.3).")
    location = fields.Char()
    state = fields.Selection(
        [("requested", "Requested"),
         ("scheduled", "Scheduled"),
         ("completed", "Completed"),
         ("rescheduled", "Rescheduled"),
         ("cancelled", "Cancelled")],
        default="requested", tracking=True)
    notes = fields.Text(help="What actually happened - in addition to the "
                              "chatter log above, for a longer write-up.")

    @api.depends("request_date", "scheduled_date")
    def _compute_release_requested_late(self):
        for meeting in self:
            if meeting.request_date and meeting.scheduled_date:
                notice = meeting.scheduled_date - meeting.request_date
                meeting.release_requested_late = \
                    notice < timedelta(hours=RELEASE_NOTICE_HOURS)
            else:
                meeting.release_requested_late = False

    @api.onchange("partner_id")
    def _onchange_partner_id_default_unit(self):
        for meeting in self:
            if meeting.partner_id.nuhw_unit_id:
                meeting.unit_id = meeting.partner_id.nuhw_unit_id
