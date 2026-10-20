# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

# Article 30 - Grievance and Arbitration. Days to the next required action,
# keyed by (grievance_type, step) - quoted section in each comment. 30.1:
# "Days shall mean calendar days." None means the CBA sets no fixed
# deadline for that step (e.g. Step 1 Informal Review).
DEADLINE_DAYS = {
    # 30.3 - Contract Interpretation track
    ("contract_interpretation", "informal_step1"): None,
    ("contract_interpretation", "hr_manager"): 21,
    ("contract_interpretation", "area_director"): 20,
    ("contract_interpretation", "arbitration"): 30,
    # 30.4 - Discipline & Discharge track (no Step 3 before arbitration)
    ("discipline_discharge", "informal_step1"): None,
    ("discipline_discharge", "hr_manager"): 7,
    ("discipline_discharge", "area_director"): 7,
    ("discipline_discharge", "arbitration"): 30,
}

STEP_HELP = (
    "Contract interpretation track (30.3): Informal Review -> HR Manager "
    "-> Area Director -> Arbitration.\n"
    "Discipline & discharge track (30.4) has no informal step: HR Manager "
    "-> Area Director -> Arbitration.")


class NuhwGrievance(models.Model):
    _name = "nuhw.grievance"
    _description = "NUHW Grievance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_filed desc"

    partner_id = fields.Many2one(
        "res.partner", string="Grievant", required=True, tracking=True)
    steward_id = fields.Many2one(
        "res.partner", string="Handling Steward",
        domain=[("is_steward", "=", True)], tracking=True)
    unit_id = fields.Many2one("nuhw.unit", string="Unit")
    filed_by = fields.Selection(
        [("union", "Union"), ("hospital", "Hospital")],
        default="union", required=True, tracking=True,
        help="30.5 - Hospital Grievances are real: the Hospital can file "
             "against the Union too, starting at the Area Director level.")
    grievance_type = fields.Selection(
        [("contract_interpretation", "Contract Interpretation"),
         ("discipline_discharge", "Discipline & Discharge")],
        required=True, tracking=True,
        help="Picks which deadline track applies (30.3 vs 30.4).")
    incident_date = fields.Date()
    step = fields.Selection(
        [("informal_step1", "Step 1 - Informal Review"),
         ("hr_manager", "HR Manager"),
         ("area_director", "Area Director"),
         ("arbitration", "Arbitration"),
         ("resolved", "Resolved"),
         ("withdrawn", "Withdrawn")],
        default="informal_step1", required=True, tracking=True,
        help=STEP_HELP)
    date_filed = fields.Date(
        string="Date of Current Step",
        default=fields.Date.context_today,
        help="When the current step's filing/meeting happened - the "
             "response_deadline_date default is computed from this date.")
    response_deadline_date = fields.Date(
        tracking=True,
        help="Smart-defaulted from the grievance type and step using this "
             "CBA's real day-counts (Article 30) - stays editable since "
             "real deadlines key off actual meeting dates, not just the "
             "filing date.")
    description = fields.Text()
    cba_article = fields.Char(
        string="CBA Article/Section",
        help="Which Article/section is alleged to have been violated, "
             "e.g. \"12.5\".")
    weingarten_meeting_ids = fields.One2many(
        "nuhw.weingarten_meeting", "grievance_id",
        string="Related Weingarten Meetings")
    outcome = fields.Selection(
        [("pending", "Pending"),
         ("granted", "Granted"),
         ("denied", "Denied"),
         ("settled", "Settled"),
         ("withdrawn", "Withdrawn"),
         ("dismissed_missed_deadline", "Dismissed - Missed Deadline")],
        default="pending", tracking=True,
        help="30.2 - missing a deadline dismisses the grieving party's "
             "grievance with prejudice; the Hospital missing its own "
             "response instead auto-advances the grievance to the next "
             "step (reflected by moving 'step' forward, not by an outcome "
             "here).")
    notes = fields.Text()
    state = fields.Selection(
        [("open", "Open"), ("closed", "Closed")],
        default="open", tracking=True)
    is_overdue = fields.Boolean(
        compute="_compute_is_overdue",
        help="The response deadline has passed and the grievance is still "
             "open. Computed live (not stored) since it depends on "
             "today's date, not just this record's own fields - a search "
             "filter for this uses a plain date comparison instead (see "
             "the search view), which stays correct as days pass.")

    @api.depends("response_deadline_date", "state")
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for grievance in self:
            grievance.is_overdue = bool(
                grievance.response_deadline_date
                and grievance.response_deadline_date < today
                and grievance.state == "open")

    @api.onchange("grievance_type", "step", "date_filed")
    def _onchange_deadline_suggestion(self):
        for grievance in self:
            days = DEADLINE_DAYS.get(
                (grievance.grievance_type, grievance.step))
            if grievance.date_filed and days is not None:
                grievance.response_deadline_date = \
                    grievance.date_filed + relativedelta(days=days)

    @api.onchange("partner_id")
    def _onchange_partner_id_default_unit(self):
        for grievance in self:
            if grievance.partner_id.nuhw_unit_id:
                grievance.unit_id = grievance.partner_id.nuhw_unit_id

    def _activity_user_id(self):
        self.ensure_one()
        return self.steward_id.user_ids[:1].id or self.env.user.id

    def _sync_deadline_activity(self):
        activity_type = self.env.ref("mail.mail_activity_data_todo")
        for grievance in self:
            existing = grievance.activity_ids.filtered(
                lambda act: act.activity_type_id == activity_type)
            if not grievance.response_deadline_date \
                    or grievance.state == "closed":
                existing.unlink()
                continue
            if existing:
                existing.write({
                    "date_deadline": grievance.response_deadline_date,
                    "user_id": grievance._activity_user_id(),
                })
            else:
                grievance.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=grievance.response_deadline_date,
                    user_id=grievance._activity_user_id(),
                    summary="Grievance deadline",
                    note=f"Next action due for grievance "
                         f"\"{grievance.display_name}\".")

    @api.model_create_multi
    def create(self, vals_list):
        grievances = super().create(vals_list)
        grievances._sync_deadline_activity()
        return grievances

    def write(self, vals):
        result = super().write(vals)
        if {"response_deadline_date", "steward_id", "state"} & set(vals):
            self._sync_deadline_activity()
        return result
