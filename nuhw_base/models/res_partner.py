# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

# Article 12.5 - Shift Differential. Zones quoted from the real CBA; shown
# in the field's own help text so they stay traceable to the contract.
SHIFT_HELP = (
    "Day: 0700-1530 (10/12hr) or 0700-1730 (8hr) - no differential.\n"
    "Evening: 1500-2330 - 9% of base hourly rate.\n"
    "Night: 2300-0730 - 25% of base hourly rate.\n"
    "(Article 12.5, Service and Technical Unit zones; Professionals Unit "
    "has its own flat differential amounts - see the CBA.)")


class ResPartner(models.Model):
    _inherit = "res.partner"

    nuhw_unit_id = fields.Many2one(
        "nuhw.unit", string="Bargaining Unit",
        help="Service and Technical Unit or Professionals Unit (Article 2 "
             "- Recognition).")
    job_classification = fields.Char(
        help="The person's actual job title/classification (Article 2.4 "
             "lists the Professionals Unit's; Service and Technical Unit's "
             "are in Appendix I). Free text since the Hospital can add or "
             "rename job titles over time (2.3/5.2).")
    shift = fields.Selection(
        [("day", "Day"), ("evening", "Evening"), ("night", "Night")],
        help=SHIFT_HELP)
    hire_date = fields.Date(help="Used for seniority (Article 17).")
    is_steward = fields.Boolean(string="Is a Union Steward")
    steward_unit_ids = fields.Many2many(
        "nuhw.unit", string="Units Represented as Steward",
        help="Which bargaining unit(s) this person is designated to "
             "represent as steward. Defaults to their own unit.")
    steward_designated_date = fields.Date(
        help="Article 7.1 - the Union must inform the Hospital in writing "
             "of each designated Steward's name.")

    @api.onchange("is_steward")
    def _onchange_is_steward_default_unit(self):
        for partner in self:
            if partner.is_steward and partner.nuhw_unit_id \
                    and partner.nuhw_unit_id not in partner.steward_unit_ids:
                partner.steward_unit_ids = [(4, partner.nuhw_unit_id.id)]

    def action_mark_dues_current(self):
        """Create/refresh one year of a 'paid' membership line without
        going through membership's invoice-driven renewal workflow - this
        CBA's dues are deducted via payroll check-off (Article 8), not
        invoiced through this database, so there's never an invoice to
        drive membership_state's own compute off of.
        """
        today = fields.Date.context_today(self)
        dues_product = self.env.ref(
            "nuhw_base.product_template_nuhw_dues").product_variant_id
        for partner in self:
            line = partner.member_line_ids.filtered(
                lambda line: not line.date_to or line.date_to >= today)[:1]
            values = {
                "partner_id": partner.id,
                "membership_id": dues_product.id,
                "member_price": dues_product.list_price,
                "date_from": today,
                "date_to": today + relativedelta(years=1),
                "state": "paid",
            }
            if line:
                line.write(values)
            else:
                self.env["membership.membership_line"].create(values)
