# -*- coding: utf-8 -*-
from odoo import Command
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHardshipRequest(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.company_data["company"]
        cls.misc_journal = cls.company_data["default_journal_misc"]
        cls.receivable_account = cls.company_data["default_account_receivable"]
        cls.revenue_account = cls.company_data["default_account_revenue"]
        cls.expense_account = cls.company_data["default_account_expense"]
        cls.payable_account = cls.company_data["default_account_payable"]
        cls.fund_account = cls.env.ref(
            "nuhw_hardship_fund.analytic_account_hardship_fund")
        cls.member = cls.env["res.partner"].create({"name": "Jamie Chen"})
        cls.env.user.write({"group_ids": [
            Command.link(cls.env.ref("nuhw_base.group_nuhw_steward").id)]})

    def _contribute(self, amount, date="2027-01-01"):
        """Mirrors how a bookkeeper would enter a real contribution: a
        normal journal entry tagged 100% to the fund's analytic account -
        no model in this module creates these, they come from Accounting
        itself."""
        move = self.env["account.move"].create({
            "move_type": "entry",
            "journal_id": self.misc_journal.id,
            "date": date,
            "line_ids": [
                Command.create({
                    "account_id": self.receivable_account.id,
                    "debit": amount, "credit": 0.0,
                }),
                Command.create({
                    "account_id": self.revenue_account.id,
                    "debit": 0.0, "credit": amount,
                    "analytic_distribution": {str(self.fund_account.id): 100.0},
                }),
            ],
        })
        move.action_post()
        return move

    def _create_request(self, amount_requested=500.0):
        return self.env["nuhw.hardship_request"].create({
            "partner_id": self.member.id,
            "amount_requested": amount_requested,
        })

    def test_fund_balance_reflects_a_real_contribution(self):
        self._contribute(1000.0)
        request = self._create_request()
        self.assertEqual(request.fund_balance, 1000.0)

    def test_approve_defaults_amount_approved_to_amount_requested(self):
        request = self._create_request(amount_requested=250.0)
        request.action_approve()
        self.assertEqual(request.state, "approved")
        self.assertEqual(request.amount_approved, 250.0)

    def test_mark_paid_without_accounts_configured_raises(self):
        request = self._create_request()
        request.action_approve()
        with self.assertRaises(UserError):
            request.with_company(self.company).action_mark_paid()

    def test_mark_paid_posts_a_real_move_and_reduces_the_balance(self):
        self._contribute(1000.0)
        self.company.write({
            "nuhw_hardship_disbursement_account_id": self.expense_account.id,
            "nuhw_hardship_payable_account_id": self.payable_account.id,
        })
        request = self._create_request(amount_requested=300.0)
        request.action_approve()
        request.with_company(self.company).action_mark_paid()
        self.assertEqual(request.state, "paid")
        self.assertTrue(request.disbursement_move_id)
        self.assertEqual(request.disbursement_move_id.state, "posted")
        self.assertEqual(request.fund_balance, 1000.0 - 300.0)

    def test_mark_paid_only_allowed_from_approved(self):
        request = self._create_request()
        with self.assertRaises(UserError):
            request.action_mark_paid()
