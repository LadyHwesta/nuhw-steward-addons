# -*- coding: utf-8 -*-
from odoo import fields, models


class NuhwUnit(models.Model):
    _name = "nuhw.unit"
    _description = "NUHW Bargaining Unit"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(help="Short code, e.g. the unit abbreviation used on "
                            "grievance forms.")
    description = fields.Text()
    member_ids = fields.One2many(
        "res.partner", "nuhw_unit_id", string="Members")
    member_count = fields.Integer(compute="_compute_member_count")

    def _compute_member_count(self):
        for unit in self:
            unit.member_count = len(unit.member_ids)
