# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestNuhwSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unit = cls.env.ref("nuhw_base.unit_service_technical")
        cls.plain_internal_user = cls.env["res.users"].create({
            "name": "Front Desk (no steward access)", "login": "nuhw_front_desk",
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id])],
        })

    def test_plain_internal_user_can_read_units(self):
        self.unit.with_user(self.plain_internal_user).name

    def test_plain_internal_user_cannot_write_units(self):
        with self.assertRaises(AccessError):
            self.unit.with_user(self.plain_internal_user).write(
                {"name": "Renamed"})

    def test_plain_internal_user_cannot_create_units(self):
        with self.assertRaises(AccessError):
            self.env["nuhw.unit"].with_user(
                self.plain_internal_user).create({"name": "New Unit"})
