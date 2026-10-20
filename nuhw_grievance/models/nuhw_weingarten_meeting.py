# -*- coding: utf-8 -*-
from odoo import fields, models


class NuhwWeingartenMeeting(models.Model):
    _inherit = "nuhw.weingarten_meeting"

    grievance_id = fields.Many2one(
        "nuhw.grievance", string="Related Grievance",
        help="Set this if a grievance was (or will be) filed as a result "
             "of this meeting. Left blank for a meeting that never became "
             "one - most don't.")
