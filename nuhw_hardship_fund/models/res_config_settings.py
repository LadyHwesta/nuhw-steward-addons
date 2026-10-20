# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nuhw_hardship_disbursement_account_id = fields.Many2one(
        related="company_id.nuhw_hardship_disbursement_account_id",
        readonly=False)
    nuhw_hardship_payable_account_id = fields.Many2one(
        related="company_id.nuhw_hardship_payable_account_id",
        readonly=False)
