# -*- coding: utf-8 -*-
{
    "name": "NUHW Steward Suite - Grievances",
    "version": "19.0.1.0.0",
    "category": "Association",
    "summary": "Grievance tracking built for this CBA's real Article 30 "
               "procedure and deadlines",
    "description": """
NUHW Steward Suite - Grievances
=================================

A plain, domain-named grievance model instead of a generic ticket/
helpdesk framework - this CBA's grievance procedure (Article 30) has an
exact, non-generic shape worth naming directly in the data model:

* **Two different deadline tracks**, picked via ``grievance_type``:
  *contract interpretation* (30.3 - Step 2 HR Manager filing within 21
  days, Step 3 Area Director within 20 days of the Step 2 response,
  arbitration within 30 days of the Step 3 response) and *discipline &
  discharge* (30.4 - Step 1 HR Manager within 7 days of the discipline,
  Step 2 Area Director within 7 days of the Step 1 response, arbitration
  within 30 days - this track has no Step 3). ``response_deadline_date``
  defaults itself from whichever track/step is picked, but stays editable
  since real deadlines key off actual meeting dates, not just the
  defaults.
* **Hospital Grievances** (30.5) are real - a ``filed_by`` field covers
  the Hospital filing against the Union, not just the usual direction.
* **Missing a deadline has two different, asymmetric consequences**
  (30.2): the grieving party missing one gets the grievance *dismissed
  with prejudice*; the Hospital missing a response *auto-advances* the
  grievance to the next step. Both are real options on ``outcome``, not
  folded into one generic "overdue" status.
* A native Odoo activity gets scheduled against ``response_deadline_date``
  on the assigned steward's user whenever it's set or changes - no custom
  cron, just ``mail.activity.mixin``.
* Optionally links back to one or more Weingarten meetings that led to it
  (``nuhw_weingarten`` stays fully standalone - this module owns the link
  by adding the ``grievance_id`` field onto that model).
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/nuhw-steward-addons",
    "depends": ["nuhw_weingarten"],
    "data": [
        "security/ir.model.access.csv",
        "views/nuhw_grievance_views.xml",
        "views/nuhw_weingarten_meeting_views.xml",
        "views/nuhw_menus.xml",
    ],
    "installable": True,
    "application": False,
}
