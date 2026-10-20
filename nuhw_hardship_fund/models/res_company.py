# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    nuhw_hardship_disbursement_account_id = fields.Many2one(
        "account.account", string="Hardship Fund Disbursement Account",
        help="Expense account debited when a hardship request is marked "
             "paid. Pick whatever account your own books already use for "
             "this - nothing is created automatically.")
    nuhw_hardship_payable_account_id = fields.Many2one(
        "account.account", string="Hardship Fund Payable/Cash Account",
        help="Account credited on the same disbursement entry - typically "
             "whichever payable or cash/bank account your books use.")
