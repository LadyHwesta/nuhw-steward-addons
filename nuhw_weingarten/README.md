# NUHW Steward Suite - Weingarten Meetings

Tracks investigatory interviews where an employee has invoked their right to
union representation (Article 7.1). Installable standalone - a Weingarten
meeting doesn't require a grievance to exist, and most won't ever become
one. Once `nuhw_grievance` is installed, a meeting can optionally be linked
to a grievance it led to (the link field lives in that module, so this one
stays usable alone).

## Fields worth knowing

- `release_requested_late` - computed, stored. True when the gap between
  `request_date` and `scheduled_date` is under 48 hours, per Article 7.3's
  advance-notice requirement for a steward's release (the same window
  Article 28.4 gives the Hospital for its own investigatory-meeting
  notice). Shown as a warning banner on the form and a red row in the list.
- `management_rep` is a plain Char, not a partner - Hospital management
  reps aren't union members and have no reason to be in this database.
- `notes` is a dedicated Text field in addition to the chatter log, for a
  longer write-up of what was actually said/decided - matches this
  ecosystem's existing convention (e.g. `paramedic.appointment`).

## Security

Everything here is gated to `nuhw_base`'s `group_nuhw_steward` - this data
can touch discipline investigations, so no other internal user (let alone
a portal user) gets any access by default.
