# NUHW Steward Suite - Hardship Fund

Nothing in this CBA governs the hardship fund - it's the Union's own,
internally-run member-assistance program, not a contractual benefit. Its
design mirrors this ecosystem's already-proven non-profit fund-accounting
*pattern* (one analytic account that every contribution and disbursement
gets tagged to, so the balance is a real GL number) without depending on
the `nonprofit-addons` repo itself.

## Setup

Before marking any request paid, set both accounts in **Settings >
Hardship Fund**: the disbursement (expense) account and the payable/cash
account. Nothing is created automatically - pick whatever your own books
already use.

## How contributions get in

This module doesn't add a "record a contribution" screen. Contributions
(dues-funded, fundraised, whatever) are entered the normal way, through
Accounting's own journal entries, tagged **100%** to the *NUHW Hardship
Fund* analytic account (Configuration or Accounting > Analytic Accounts).
Nothing new to learn for whoever already keeps the union's books.

## Requests

`nuhw.hardship_request`: a member's amount/reason, reviewing steward(s),
and a submitted -> under_review -> approved/denied -> paid flow. Approving
defaults `amount_approved` to `amount_requested` (override it for a
partial grant). **Mark Paid** posts a real `account.move` - debiting the
disbursement account (tagged 100% to the fund's analytic account) and
crediting the payable/cash account - so the fund's balance actually moves.
The request form shows the fund's **current balance live** (not stored,
always current) so a steward can see what's actually available before
approving an amount.
