# NUHW Steward Addons

Odoo 19 **Community** modules for a NUHW hospital local - built against the
real collective bargaining agreement between NUHW and Providence Santa Rosa
Memorial Hospital, not a generic union template. Members, stewards,
bargaining units, Weingarten meetings, grievances, direct actions, and a
hardship fund.

## Modules

- [`nuhw_base/`](nuhw_base/) - members (via vendored OCA `membership`'s own
  "Members" menu, distinct from core Customers - see this repo's
  `VENDORED.md`), bargaining units (`nuhw.unit`, seeded with this CBA's
  real "Service and Technical Unit" and "Professionals Unit"), shift
  (day/evening/night, quoting the real differential zones), and stewards
  (a flag, which unit(s) they represent, when they were designated).
- [`nuhw_weingarten/`](nuhw_weingarten/) - investigatory-interview /
  Weingarten-rights meetings: who's being interviewed, which steward(s)
  are representing them, a computed flag for whether the steward's release
  was requested less than the CBA's required 48 hours in advance.
  Installable standalone.
- [`nuhw_grievance/`](nuhw_grievance/) - a grievance model built for this
  CBA's actual Article 30 procedure: two different deadline tracks
  (contract interpretation vs. discipline & discharge), the asymmetric
  consequence of missing a deadline (dismissal with prejudice vs.
  auto-advancing a step), Hospital-filed grievances, and a native Odoo
  activity reminder on the handling steward whenever the deadline is set.
  Optionally links back to Weingarten meetings.
- [`nuhw_direct_action/`](nuhw_direct_action/) - lightweight tracking for
  informational pickets, rallies, petitions, button days, and similar
  organizing activity.
- [`nuhw_hardship_fund/`](nuhw_hardship_fund/) - member hardship-fund
  requests with a real, GL-backed running balance (one analytic account
  every contribution/disbursement gets tagged to - the same pattern this
  ecosystem's non-profit suite uses, not a dependency on it).

## Testing

See [`testing/`](testing/) for a self-contained local Odoo 19 + Postgres
instance to try these modules against.

## Vendored code

See [`VENDORED.md`](VENDORED.md).
