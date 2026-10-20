# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unit = cls.env.ref("nuhw_base.unit_service_technical")
        cls.member = cls.env["res.partner"].create({
            "name": "Alex Rivera",
            "nuhw_unit_id": cls.unit.id,
            "shift": "night",
        })

    def test_unit_member_count(self):
        self.assertIn(self.member, self.unit.member_ids)
        self.assertEqual(self.unit.member_count, len(self.unit.member_ids))

    def test_mark_dues_current_creates_a_paid_line_with_no_invoice(self):
        self.member.action_mark_dues_current()
        line = self.member.member_line_ids
        self.assertEqual(len(line), 1)
        self.assertEqual(line.state, "paid")
        self.assertFalse(line.account_invoice_id)
        self.assertEqual(self.member.membership_state, "paid")

    def test_mark_dues_current_refreshes_the_existing_line_not_a_new_one(self):
        self.member.action_mark_dues_current()
        first_date_to = self.member.member_line_ids.date_to
        self.member.action_mark_dues_current()
        self.assertEqual(len(self.member.member_line_ids), 1)
        self.assertGreaterEqual(
            self.member.member_line_ids.date_to, first_date_to)
