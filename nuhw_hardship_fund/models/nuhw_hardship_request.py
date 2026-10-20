# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class NuhwHardshipRequest(models.Model):
    _name = "nuhw.hardship_request"
    _description = "NUHW Hardship Fund Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc"

    partner_id = fields.Many2one(
        "res.partner", string="Member", required=True, tracking=True)
    date_requested = fields.Date(
        default=fields.Date.context_today, tracking=True)
    amount_requested = fields.Monetary(tracking=True)
    reason = fields.Text()
    reviewer_ids = fields.Many2many(
        "res.partner", string="Reviewing Steward(s)",
        domain=[("is_steward", "=", True)])
    state = fields.Selection(
        [("submitted", "Submitted"),
         ("under_review", "Under Review"),
         ("approved", "Approved"),
         ("denied", "Denied"),
         ("paid", "Paid")],
        default="submitted", tracking=True)
    amount_approved = fields.Monetary(tracking=True)
    denial_reason = fields.Text()
    disbursement_move_id = fields.Many2one(
        "account.move", string="Disbursement Entry", readonly=True)
    notes = fields.Text()
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id)
    fund_balance = fields.Monetary(
        compute="_compute_fund_balance",
        help="The fund's current balance, live - not stored, so it's "
             "always up to date.")

    def _compute_fund_balance(self):
        balance = self._fund_balance()
        for request in self:
            request.fund_balance = balance

    def _fund_balance(self):
        fund_account = self.env.ref(
            "nuhw_hardship_fund.analytic_account_hardship_fund")
        lines = self.env["account.analytic.line"].search(
            [("auto_account_id", "=", fund_account.id)])
        return sum(lines.mapped("amount"))

    def action_approve(self):
        for request in self:
            if not request.amount_approved:
                request.amount_approved = request.amount_requested
            request.state = "approved"

    def action_deny(self):
        self.write({"state": "denied"})

    def action_mark_paid(self):
        for request in self:
            if request.state != "approved":
                raise UserError(
                    "Only an approved request can be marked paid.")
            request.disbursement_move_id = request._post_disbursement()
            request.state = "paid"

    def _post_disbursement(self):
        self.ensure_one()
        company = self.env.company
        disbursement_account = company.nuhw_hardship_disbursement_account_id
        payable_account = company.nuhw_hardship_payable_account_id
        if not (disbursement_account and payable_account):
            raise UserError(
                "Set the Hardship Fund Disbursement and Payable/Cash "
                "accounts in Settings before marking a request paid.")
        fund_account = self.env.ref(
            "nuhw_hardship_fund.analytic_account_hardship_fund")
        journal = self.env["account.journal"].search(
            [("type", "=", "general"), ("company_id", "=", company.id)],
            limit=1)
        if not journal:
            raise UserError(
                "No miscellaneous-operations journal found for %s."
                % company.display_name)
        move = self.env["account.move"].create({
            "move_type": "entry",
            "journal_id": journal.id,
            "date": fields.Date.context_today(self),
            "partner_id": self.partner_id.id,
            "line_ids": [
                (0, 0, {
                    "account_id": disbursement_account.id,
                    "partner_id": self.partner_id.id,
                    "debit": self.amount_approved, "credit": 0.0,
                    "analytic_distribution": {
                        str(fund_account.id): 100.0},
                }),
                (0, 0, {
                    "account_id": payable_account.id,
                    "partner_id": self.partner_id.id,
                    "debit": 0.0, "credit": self.amount_approved,
                }),
            ],
        })
        move.action_post()
        return move.id
