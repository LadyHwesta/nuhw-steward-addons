# -*- coding: utf-8 -*-
{
    "name": "NUHW Steward Suite - Hardship Fund",
    "version": "19.0.1.0.0",
    "category": "Association",
    "summary": "Member hardship-fund requests with a real, GL-backed fund "
               "balance",
    "description": """
NUHW Steward Suite - Hardship Fund
=====================================

Nothing in this CBA governs the hardship fund - it's the Union's own,
internally-run program, not a contractual benefit - so its design is free
to mirror this ecosystem's already-proven non-profit fund-accounting
*pattern* instead: one dedicated ``account.analytic.account`` ("NUHW
Hardship Fund") that every contribution and disbursement gets tagged to,
so the fund's balance is a real, auditable accounting number instead of a
hand-tracked total. This module doesn't depend on the ``nonprofit-addons``
repo - it reuses the shape, not the code.

* **Contributions in** - entered the normal way, through Accounting's own
  journal entries, tagged 100% to the fund's analytic account. Nothing
  new to learn for whoever already keeps the union's books.
* **Requests** - a member submits a request (amount, reason); one or more
  reviewing stewards approve/deny/mark it paid.
* **Disbursement** - marking a request paid posts a real ``account.move``
  (configure the disbursement expense account and the payable/cash
  account to use in Settings first), debited against the fund's analytic
  account, so the running balance always reflects actual GL activity.
* The request form shows the fund's current balance live, so a steward
  can see what's actually available before approving an amount.
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/nuhw-steward-addons",
    "depends": ["nuhw_base", "account"],
    "data": [
        "security/ir.model.access.csv",
        "data/nuhw_hardship_fund_data.xml",
        "views/res_config_settings_views.xml",
        "views/nuhw_hardship_request_views.xml",
        "views/nuhw_menus.xml",
    ],
    "installable": True,
    "application": False,
}
