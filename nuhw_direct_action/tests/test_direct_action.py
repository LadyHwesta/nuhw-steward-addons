# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDirectAction(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unit = cls.env.ref("nuhw_base.unit_service_technical")
        cls.steward = cls.env["res.partner"].create({
            "name": "Alex Rivera", "is_steward": True,
        })
        cls.member = cls.env["res.partner"].create({"name": "Jamie Chen"})

    def test_create_and_default_state(self):
        action = self.env["nuhw.direct_action"].create({
            "name": "Informational Picket - Shift Change",
            "action_type": "informational_picket",
            "unit_ids": [(6, 0, [self.unit.id])],
            "organizer_id": self.steward.id,
            "participant_ids": [(6, 0, [self.member.id])],
        })
        self.assertEqual(action.state, "planned")
        self.assertIn(self.member, action.participant_ids)
        self.assertIn(self.unit, action.unit_ids)

    def test_required_fields_enforced(self):
        with self.assertRaises(Exception):
            self.env["nuhw.direct_action"].create({"name": "No type set"})
