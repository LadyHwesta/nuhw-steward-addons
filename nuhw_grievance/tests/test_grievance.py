# -*- coding: utf-8 -*-
from datetime import date

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestGrievance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unit = cls.env.ref("nuhw_base.unit_service_technical")
        cls.grievant = cls.env["res.partner"].create({
            "name": "Jamie Chen", "nuhw_unit_id": cls.unit.id,
        })
        cls.steward = cls.env["res.partner"].create({"name": "Alex Rivera"})
        cls.steward_user = cls.env["res.users"].create({
            "name": "Alex Rivera", "login": "alex_rivera_steward",
            "partner_id": cls.steward.id,
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id,
                                   cls.env.ref("nuhw_base.group_nuhw_steward").id])],
        })

    def _create_grievance(self, **kwargs):
        values = {
            "partner_id": self.grievant.id,
            "steward_id": self.steward.id,
            "grievance_type": "contract_interpretation",
            "step": "hr_manager",
            "date_filed": date(2027, 1, 1),
        }
        values.update(kwargs)
        return self.env["nuhw.grievance"].create(values)

    def test_deadline_suggestion_contract_interpretation_hr_manager(self):
        grievance = self._create_grievance()
        grievance._onchange_deadline_suggestion()
        self.assertEqual(grievance.response_deadline_date, date(2027, 1, 22))

    def test_deadline_suggestion_discipline_discharge_hr_manager(self):
        grievance = self._create_grievance(
            grievance_type="discipline_discharge")
        grievance._onchange_deadline_suggestion()
        self.assertEqual(grievance.response_deadline_date, date(2027, 1, 8))

    def test_deadline_suggestion_arbitration_is_30_days_both_tracks(self):
        for grievance_type in ("contract_interpretation", "discipline_discharge"):
            grievance = self._create_grievance(
                grievance_type=grievance_type, step="arbitration")
            grievance._onchange_deadline_suggestion()
            self.assertEqual(
                grievance.response_deadline_date, date(2027, 1, 31))

    def test_deadline_suggestion_informal_step_has_no_default(self):
        grievance = self._create_grievance(step="informal_step1")
        grievance._onchange_deadline_suggestion()
        self.assertFalse(grievance.response_deadline_date)

    def test_is_overdue_when_deadline_passed_and_open(self):
        grievance = self._create_grievance(
            response_deadline_date=date(2000, 1, 1))
        self.assertTrue(grievance.is_overdue)

    def test_is_overdue_false_once_closed(self):
        grievance = self._create_grievance(
            response_deadline_date=date(2000, 1, 1), state="closed")
        self.assertFalse(grievance.is_overdue)

    def test_create_schedules_a_deadline_activity_on_the_steward(self):
        grievance = self._create_grievance(
            response_deadline_date=date(2027, 2, 1))
        todo = self.env.ref("mail.mail_activity_data_todo")
        activities = grievance.activity_ids.filtered(
            lambda act: act.activity_type_id == todo)
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities.date_deadline, date(2027, 2, 1))
        self.assertEqual(activities.user_id, self.steward_user)

    def test_closing_the_grievance_removes_the_deadline_activity(self):
        grievance = self._create_grievance(
            response_deadline_date=date(2027, 2, 1))
        grievance.write({"state": "closed"})
        todo = self.env.ref("mail.mail_activity_data_todo")
        self.assertFalse(grievance.activity_ids.filtered(
            lambda act: act.activity_type_id == todo))

    def test_weingarten_meeting_links_back_to_grievance(self):
        grievance = self._create_grievance()
        meeting = self.env["nuhw.weingarten_meeting"].create({
            "partner_id": self.grievant.id,
            "grievance_id": grievance.id,
        })
        self.assertIn(meeting, grievance.weingarten_meeting_ids)
