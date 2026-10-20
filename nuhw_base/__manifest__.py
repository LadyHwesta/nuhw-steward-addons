# -*- coding: utf-8 -*-
{
    "name": "NUHW Steward Suite - Base",
    "version": "19.0.1.0.0",
    "category": "Association",
    "summary": "Members, stewards, bargaining units, and shifts for a NUHW "
               "hospital local",
    "description": """
NUHW Steward Suite - Base
==========================

The foundation the rest of the steward/grievance suite builds on, scoped
against the real Santa Rosa Memorial Hospital CBA rather than a generic
template.

* **Members** - depends on OCA's ``membership`` module for its "Members"
  menu/action, distinct from core Customers. This CBA's dues are deducted
  via payroll check-off (Article 8), not invoiced through Odoo, so this
  module doesn't use ``membership``'s invoice-driven renewal workflow -
  see this module's own README for the one-click "mark dues current"
  alternative.
* **Bargaining units** - a small ``nuhw.unit`` model seeded with this CBA's
  two real units (Article 2): Service and Technical Unit, and Professionals
  Unit. A separate free-text job classification field holds the person's
  actual title underneath their unit, since the Hospital can add/rename job
  titles over time (2.3/5.2).
* **Shift** - a plain day/evening/night field on every member, with help
  text quoting this CBA's real shift-differential zones (Article 12.5):
  Day 0700-1530/1730 (no differential), Evening 1500-2330 (9%), Night
  2300-0730 (25%).
* **Stewards** - a flag plus which unit(s) they're designated to represent
  (Article 7.1 requires written designation to the Hospital) and when they
  were designated, with a dedicated Stewards menu filtered to them.
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/nuhw-steward-addons",
    "depends": ["membership", "contacts"],
    "data": [
        "security/nuhw_security.xml",
        "security/ir.model.access.csv",
        "data/nuhw_unit_data.xml",
        "views/nuhw_unit_views.xml",
        "views/res_partner_views.xml",
        "views/nuhw_menus.xml",
    ],
    "installable": True,
    "application": True,
}
