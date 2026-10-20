# -*- coding: utf-8 -*-
{
    "name": "NUHW Steward Suite - Weingarten Meetings",
    "version": "19.0.1.0.0",
    "category": "Association",
    "summary": "Track investigatory interviews and steward representation "
               "requests (Weingarten rights)",
    "description": """
NUHW Steward Suite - Weingarten Meetings
=========================================

A Weingarten meeting is an employee's right to union representation during
an investigatory interview that could lead to discipline (Article 7.1 lists
"to service as a Union representative for Weingarten meetings" among a
Steward's authorities). Not every one of these leads to a grievance, and a
grievance can exist without one, so this is its own standalone model -
optionally linked to a grievance once ``nuhw_grievance`` is installed.

* Who's being interviewed, which steward(s) are representing them, the
  Hospital's own representative, the unit, and a dedicated notes field
  (alongside chatter) for what actually happened.
* A computed flag for whether the steward's release was requested less
  than 48 hours before the meeting - Article 7.3 requires a Steward to
  "request release at least forty-eight (48) hours in advance", the same
  window Article 28.4 gives the Hospital for investigatory-interview
  notice, so a late request is a real contractual fact worth surfacing,
  not just a courtesy.
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/nuhw-steward-addons",
    "depends": ["nuhw_base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/nuhw_weingarten_meeting_views.xml",
        "views/nuhw_menus.xml",
    ],
    "installable": True,
    "application": False,
}
