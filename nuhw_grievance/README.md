# NUHW Steward Suite - Grievances

A grievance model built for this CBA's actual Article 30 procedure, not a
generic ticket/helpdesk framework.

## Two deadline tracks

`grievance_type` picks which real deadline schedule applies:

| Step | Contract interpretation (30.3) | Discipline & discharge (30.4) |
| --- | --- | --- |
| HR Manager | file within **21 days** | file within **7 days** |
| Area Director | **20 days** after HR Manager's response | **7 days** after HR Manager's response |
| Arbitration | **30 days** after Area Director's response | **30 days** after Area Director's response |

(30.1: "Days shall mean calendar days" - these are calendar days, not
business days. The discipline track has no Step 3/Informal Review per
30.4.) `response_deadline_date` suggests itself from `grievance_type` +
`step` + `date_filed` using this table, but stays a plain editable field -
real deadlines key off actual meeting dates, which this suite doesn't try
to track automatically.

## Two different ways a deadline miss plays out (30.2)

Missing a deadline isn't one generic "overdue" state - the CBA treats the
two directions differently:

- The **grieving party** (usually the Union) missing one **dismisses the
  grievance with prejudice** - set `outcome` to *Dismissed - Missed
  Deadline*.
- The **Hospital** missing its own response **auto-advances the grievance
  to the next step** - just move `step` forward; there's no special
  `outcome` for this since the grievance itself keeps going.

## Hospital Grievances (30.5)

The Hospital can file a grievance against the Union too, starting at the
Area Director level - `filed_by` covers this; don't assume the Union is
always the filer.

## Deadline reminders

Whenever `response_deadline_date` is set (on create or a later write), a
native Odoo activity (`mail.mail_activity_data_todo`) gets scheduled on the
handling steward's user - no custom cron. Closing the grievance (`state =
closed`) removes it. If the steward has no linked `res.users` account yet,
it falls back to whichever user made the change.

## Weingarten meetings

`nuhw_weingarten` stays fully standalone - this module adds the
`grievance_id` field onto `nuhw.weingarten_meeting` itself, so a meeting
can optionally point at the grievance it led to without that module ever
needing to know grievances exist.
