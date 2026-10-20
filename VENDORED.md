# Vendored OCA modules

One module in this repo comes from the **Odoo Community Association**, not
from us: `membership/`. It's vendored because `nuhw_base` depends on its
"Members" menu/action (a real, distinct action from core Customers - see
`membership/views/res_partner_views.xml`'s `action_membership_members`) and
Odoo 19 dropped the core Membership app entirely. Same copy already vendored
once in `LadyHwesta/odoo-addons` for its amateur radio club suite - pulled
from there rather than re-derived.

It keeps **its own upstream licence** (see its `__manifest__.py`) - it is
*not* covered by this repo's top-level LGPL-3.

It sits at the repo root next to our own modules (not under a `vendor/`
subdir - that breaks Bootstrap's own SCSS import resolution). Nothing extra
to add to `addons_path` - the repo root is enough.

## Contents

Source: <https://github.com/OCA/vertical-association>

| Module | Upstream | Status |
| --- | --- | --- |
| `membership` | `19.0` @ `8153173` (2026-08-11) | **verbatim.** Odoo removed the classic Membership app in 19.0; this is OCA's re-port. LGPL-3. |

`readme/` fragment dirs, `pyproject.toml` packaging files, and `i18n/`
translation catalogues were stripped from the copy, same as in `odoo-addons`.
Nothing else was touched.

### A real-world fit note

This CBA's union dues are deducted via payroll check-off (Article 8), not
invoiced through Odoo - `membership`'s own fee/invoice-driven renewal
workflow (`membership.membership_line`, membership products) doesn't map to
that. `nuhw_base` uses this module only for its "Members" menu and
`membership_state` field; nothing here assumes dues are ever actually
invoiced through this database. See `nuhw_base`'s own README for how
`membership_state` gets set manually instead.
