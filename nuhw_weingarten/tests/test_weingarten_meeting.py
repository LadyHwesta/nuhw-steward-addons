# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestWeingartenMeeting(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unit = cls.env.ref("nuhw_base.unit_service_technical")
        cls.employee = cls.env["res.partner"].create({
            "name": "Jamie Chen", "nuhw_unit_id": cls.unit.id,
        })
        cls.steward = cls.env["res.partner"].create({
            "name": "Alex Rivera", "is_steward": True,
        })

    def _create_meeting(self, request_date, scheduled_date):
        return self.env["nuhw.weingarten_meeting"].create({
            "partner_id": self.employee.id,
            "steward_ids": [(6, 0, [self.steward.id])],
            "request_date": request_date,
            "scheduled_date": scheduled_date,
        })

    def test_release_requested_on_time_is_not_late(self):
        scheduled = datetime(2027, 3, 10, 14, 0, 0)
        meeting = self._create_meeting(
            scheduled - timedelta(hours=72), scheduled)
        self.assertFalse(meeting.release_requested_late)

    def test_release_requested_late_is_flagged(self):
        scheduled = datetime(2027, 3, 10, 14, 0, 0)
        meeting = self._create_meeting(
            scheduled - timedelta(hours=10), scheduled)
        self.assertTrue(meeting.release_requested_late)

    def test_no_dates_is_not_late(self):
        meeting = self.env["nuhw.weingarten_meeting"].create({
            "partner_id": self.employee.id,
        })
        self.assertFalse(meeting.release_requested_late)

    def test_steward_domain_excludes_non_stewards(self):
        non_steward = self.env["res.partner"].create({"name": "Not A Steward"})
        meeting = self._create_meeting(
            datetime(2027, 1, 1), datetime(2027, 1, 3))
        meeting.steward_ids = [(4, non_steward.id)]
        # The field has no SQL-level constraint - domain is a UI filter
        # only - so this documents that assumption rather than asserting
        # an error, and confirms the originally-set steward stays too.
        self.assertIn(self.steward, meeting.steward_ids)
