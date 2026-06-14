# Case JSON Schema

Both PDF scripts read a single case JSON describing the dispute. Build it from the
reconciliation and diagnosis, then pass it to the scripts. Optional fields can be omitted —
the scripts degrade gracefully (e.g. skip a screenshot panel if no path is given). Dates are
free-form strings; use whatever the user's documents show.

All values below are illustrative placeholders — replace every field with the actual user's
details. Do not ship real account numbers, card numbers, or member IDs anywhere.

## Fields

```jsonc
{
  "cardholder": "Full name as on the loyalty account",
  "issuer": "Chase",
  "card": "United Quest Card",
  "card_last4": "0000",
  "loyalty_program": "United MileagePlus",
  "member_number": "AB1234567",
  "member_status": "Premier Gold",          // optional
  "account_open_date": "01/15/2026",

  "offer": {
    "miles": 80000,
    "status_points": 3000,                   // 0 or omit if none
    "status_points_label": "PQP",            // "PQP" | "MQD" | ...
    "spend_requirement": "$4,000",
    "window": "first 3 months",
    "offer_url": "creditcards.example.com/path-to-offer-page",   // optional
    "wayback_url": "https://web.archive.org/web/<YYYYMMDDhhmmss>/<offer-page-URL>", // optional
    "wayback_date": "MM/DD/YYYY"             // optional
  },

  "program_year": "2026",
  "failure_mode": "Short human-readable diagnosis",
  "summary": "One-sentence statement of what's resolved and what's outstanding.",
  "spend_goal_met_cycle": "March 2026 statement",
  "bonus_trigger_line": "New Cardmember Bonus 80,000",
  "in_app_confirmation": "Congrats! You earned 80,000 bonus miles and 3,000 PQP ...",  // optional
  "in_app_confirmation_date": "MM/DD/YYYY",  // optional

  // Cycle-by-cycle reconciliation (issuer-reported vs loyalty-received)
  "reconciliation": [
    {"cycle": "Month 1", "issuer_reported_miles": 2500, "loyalty_received_miles": 0,
     "note": "routed to a duplicate member number"},
    {"cycle": "Month 2", "issuer_reported_miles": 87500, "loyalty_received_miles": 0,
     "note": "incl. 80,000 welcome bonus; routed to duplicate"},
    {"cycle": "Month 3", "issuer_reported_miles": 2250, "loyalty_received_miles": 2250,
     "note": "posted correctly after name fix"},
    {"cycle": "Month 4", "issuer_reported_miles": 4900, "loyalty_received_miles": 4900,
     "note": "posted correctly"}
  ],

  "resolved": [
    "80,000 award miles posted to the loyalty account, backdated to the original statement date.",
    "Stranded everyday-spend miles from the early cycles also posted after the merge."
  ],
  "outstanding": [
    "3,000 PQP welcome bonus has not posted. Status-points view shows Bonus 0 / Promo 0."
  ],

  // Rows for the activity-log evidence table (status_points usually 0 on the bonus line)
  "evidence_rows": [
    {"date": "MM/DD/YYYY", "description": "Card Bonus Miles", "miles": 80000,
     "status_points": 0, "highlight": true},
    {"date": "MM/DD/YYYY", "description": "Card 1 Mile All Purchases", "miles": 4889,
     "status_points": 0}
  ],

  "screenshots": {                            // all optional; only embedded if path exists
    "offer": "/path/offer.png",
    "confirmation": "/path/confirm.png",
    "dashboard_miles": "/path/dash_miles.png",
    "dashboard_status": "/path/dash_status.png"
  },

  "ask": "Credit 3,000 PQP to the loyalty account for the 2026 program year."
}
```

## Worked example (fictional)

A representative status-points case — a cardholder whose name on the card did not match their
loyalty profile, which routed the early transfers (including the welcome bonus) to a duplicate
member number. After a merge the miles posted, but the status-points half did not. **All names
and numbers here are made up.**

```jsonc
{
  "cardholder": "Jordan Avery",
  "issuer": "Chase",
  "card": "United Quest Card",
  "card_last4": "0000",
  "loyalty_program": "United MileagePlus",
  "member_number": "AB1234567",
  "member_status": "Premier Gold",
  "account_open_date": "01/15/2026",
  "offer": {
    "miles": 80000, "status_points": 3000, "status_points_label": "PQP",
    "spend_requirement": "$4,000", "window": "first 3 months",
    "offer_url": "creditcards.example.com/united-quest",
    "wayback_url": "https://web.archive.org/web/<YYYYMMDDhhmmss>/<offer-page-URL>",
    "wayback_date": "02/07/2026"
  },
  "program_year": "2026",
  "failure_mode": "Card name did not match the loyalty profile, creating a duplicate member number; early transfers (incl. the 80,000 welcome bonus) routed there. After merge the miles posted (backdated), but the 3,000 PQP welcome component was never awarded.",
  "summary": "80,000 miles have posted. The 3,000 PQP have not. Follow-up isolating the remaining issue.",
  "spend_goal_met_cycle": "third statement cycle",
  "bonus_trigger_line": "New Cardmember Bonus 80,000",
  "in_app_confirmation": "Congrats! You earned 80,000 bonus miles and 3,000 PQP by reaching your spend goal.",
  "outstanding": ["3,000 PQP welcome bonus has not posted. Status-points view shows Spend earn, Bonus 0, Promo 0."],
  "evidence_rows": [
    {"date": "MM/DD/YYYY", "description": "Card Bonus Miles", "miles": 80000, "status_points": 0, "highlight": true}
  ],
  "ask": "Credit 3,000 PQP to the loyalty account for the 2026 program year."
}
```

## Notes

- **`status_points` / `status_points_label`** generalize PQP. For a miles-only dispute, set
  `status_points` to 0 and the documents adapt (no status-points columns/sections emphasized).
- **`highlight: true`** on an `evidence_rows` entry shades that row (use it for the bonus line
  showing status points = 0 — the keystone of a status-points dispute).
- **Screenshots** are embedded at sensible widths; if a path is missing or the file isn't found,
  that panel is simply skipped. Stage screenshots to local paths before running the scripts.
- Keep the JSON in the working directory (e.g. `case.json`) and pass it as the first script arg.
- **Never commit or ship a real user's case JSON** — it contains personal financial identifiers.
