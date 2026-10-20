# NUHW Steward Suite - Base

Members, stewards, bargaining units, and shift on top of `res.partner`.
Everything else in this suite depends on this module.

## Members

Depends on OCA's `membership` module (vendored - see this repo's own
`VENDORED.md`) for its "Members" menu, a real action distinct from core
Customers rather than a rename of it (same pattern as this ecosystem's
amateur radio club suite).

**This CBA's union dues are deducted via payroll check-off (Article 8),
never invoiced through Odoo** - so `membership`'s own invoice-driven
renewal workflow doesn't apply here. Use the **Mark Dues Current** button
on a member's form instead: it creates (or refreshes) one year of a `paid`
membership line directly, with no invoice attached. `membership_state`
still reflects it correctly (`paid`) since `membership`'s own compute
preserves an explicitly-set state when there's no invoice to derive it
from.

## Bargaining units

`nuhw.unit` - seeded with this CBA's real two units (Article 2 -
Recognition): **Service and Technical Unit** and **Professionals Unit**.
Kept as records (Configuration > Bargaining Units), not a hardcoded
Selection, in case more granular tracking is wanted later.

## Shift

A plain `day`/`evening`/`night` field on every partner. The three zones
come straight from Article 12.5 (Shift Differential) and are quoted in the
field's own help text - Day 0700-1530/1730 (no differential), Evening
1500-2330 (9%), Night 2300-0730 (25%); the Professionals Unit has its own
flat differential amounts instead of a percentage.

## Stewards

A boolean flag, which unit(s) they're designated to represent
(`steward_unit_ids`), and when they were designated
(`steward_designated_date`) - Article 7.1 requires the Union to inform the
Hospital in writing of each Steward's name. A dedicated **Stewards** menu
(Settings-gated to the `group_nuhw_steward` group) lists just these
partners.

## Security

One group, `group_nuhw_steward`: full read/write on `nuhw.unit` and
(once the other modules in this suite are installed) every grievance/
Weingarten/hardship-fund model. Every other internal user gets read-only
access to the unit list and none at all to the sensitive models - grant
`group_nuhw_steward` only to actual stewards.
