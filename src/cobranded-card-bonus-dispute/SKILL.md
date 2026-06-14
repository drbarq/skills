---
name: cobranded-card-bonus-dispute
description: >-
  Diagnose and resolve a co-branded airline or hotel credit card welcome-bonus dispute end to
  end — when bonus miles, points, or status-qualifying points (United PQP, Delta MQD, etc.)
  fail to post after the spend requirement was met. Use this whenever someone says their
  sign-up bonus did not post, miles or points are missing, status points were not credited,
  the issuer says rewards were sent but the loyalty program has no record, a loyalty account
  number changed or duplicated, or only part of a bonus posted. It reconciles card statements
  against the loyalty activity export, diagnoses the failure mode, corroborates the original
  offer (including via the Wayback Machine), and generates a full dispute packet:
  timeline/reconciliation PDF, status document, secure-message drafts for both the issuer and
  the loyalty program, phone scripts, and a follow-up tracker. Covers United/Chase, Delta/Amex,
  American/Citi, Southwest/Chase, Marriott, Hilton, and similar co-brands.
---

# Co-branded Card Bonus Dispute

Help someone recover a co-branded credit card welcome bonus that did not post correctly, and
hand them an evidence-backed packet routed to whoever can actually fix it. The output is real
files (PDFs, message drafts), not just advice.

## The mental model (read this first — it drives everything)

A co-branded card welcome bonus is fulfilled across **two separate systems** that must agree:

1. **The issuer** (Chase, Amex, Citi, Barclays). Tracks the cardholder's spend, decides when
   the spend goal is met, and transfers **miles/points** to the loyalty program. The
   bonus-miles trigger shows up as a line on a **credit card statement** (e.g. Chase's "New
   Cardmember Bonus 80,000").

2. **The loyalty program** (United MileagePlus, Delta SkyMiles, AAdvantage, Marriott Bonvoy,
   Hilton Honors). Receives the miles/points AND separately awards any **status-qualifying
   points** component (United **PQP**, Delta **MQD**, etc.).

The single most important fact: **status-qualifying points are never on a credit card
statement.** They are a loyalty-program concept. The issuer does not "send" PQP/MQD line by
line — the loyalty program awards them when the issuer signals the spend goal was met. So if a
welcome offer is "80,000 miles + 3,000 PQP," the statement will only ever show the miles half.
The PQP half lives exclusively in the loyalty account. This is normal and is **not** evidence
the PQP was not earned.

Almost every dispute traces to the seam between these two systems:
- one half posts and the other does not (very common: miles land, status points do not),
- the issuer says "we sent it" and the loyalty program says "we have no record,"
- the **link** between the systems — the loyalty member number tied to the card — is wrong,
  duplicated, or got changed, so transfers route to the wrong account.

The job: pinpoint exactly **which half failed and why**, prove the offer existed, and route the
ask to the party that can actually credit it.

## Workflow overview

Phase 0 Intake → Phase 1 Gather evidence → Phase 2 Reconcile → Phase 3 Diagnose failure mode →
Phase 4 Corroborate the offer → Phase 5 Generate the dispute packet → Phase 6 Escalation guidance.

Move through the phases in order, but skip what's already established and don't re-ask for
things the user already gave. Keep the user oriented with short summaries, not a play-by-play.

---

## Phase 0 — Intake

Establish these, asking only for what isn't already known or inferable from uploaded files:

- **Issuer + card** (e.g. Chase United Quest), and the **loyalty program + member number**.
- **The exact offer**: bonus miles/points amount, any **status-points component** and amount,
  the **spend requirement**, and the **time window** (e.g. $4,000 in first 3 months).
- **Account-open date.**
- **What's believed missing**, and **when the spend goal was met** (which statement cycle).
- **What evidence the user has** on hand (statements, loyalty export, screenshots).

If the user only has a fragment ("I think my bonus didn't post"), that's fine — proceed and
fill gaps as evidence comes in.

## Phase 1 — Gather evidence

Ask the user to provide / locate:

- **Credit card statements (PDF)** covering the full qualifying window **and** the cycle where
  the bonus should have appeared. The bonus-miles trigger line is the keystone evidence.
- **Loyalty activity export** — a CSV is ideal (most programs offer an activity download);
  screenshots of the activity feed work too.
- **Any in-app bonus-confirmation screenshot** — e.g. "Congrats! You earned 80,000 bonus miles
  and 3,000 PQP." This is gold: it is the loyalty program's own UI confirming the debt.
- **The offer terms** (we corroborate these in Phase 4 — the user need not have them).

**Privacy:** statements contain full card numbers and addresses. Do not echo full card numbers
back; refer to the card by last 4. If generating files, redact where practical. Process locally
and avoid persisting sensitive data.

To read PDFs/CSVs, use the available file tools. If a statement is a scanned image, OCR it.

## Phase 2 — Reconcile

Build the factual spine: a **cycle-by-cycle comparison of what the issuer reported transferring
vs. what actually landed in the loyalty account.**

1. From each **statement**, pull the issuer's reported miles/points transferred for that cycle
   (and note the bonus-trigger line when it appears, e.g. "New Cardmember Bonus 80,000").
2. From the **loyalty export**, pull what actually posted, by date.
3. Lay them side by side per cycle. Reconcile the everyday earn first (it usually matches and
   proves the pipeline works), then isolate exactly **which component is missing** — and on
   which date/cycle.
4. State the gap precisely in both currencies: e.g. "90,191 miles + 3,000 PQP stranded," or
   "miles fully posted; only the 3,000 PQP status-points component is missing."

Show the reconciliation as a compact table. The goal is a single unambiguous sentence naming
the missing component, the amount, and the cycle it should have posted in.

## Phase 3 — Diagnose the failure mode

**Read `references/failure-modes.md`** and match the reconciliation against the known patterns.
Determine which one (or combination) applies, because the fix differs by mode:

- **Name mismatch → duplicate / changed loyalty account** (transfers route to a second member
  number; the merge/relink is the fix).
- **Status-points half missing** (miles posted, PQP/MQD did not — the most common, and
  loyalty-side only).
- **Partial post** (base miles posted, the *bonus delta* did not).
- **Nothing posted yet** (still inside the posting window vs. genuinely overdue — check the
  clock before escalating).
- **Wrong-account routing** (correct member, but a stale number on file at the issuer).

Name the diagnosis explicitly and tie it to the evidence (e.g. "the early-cycle transfers
routed to a second member number that was created because the card name did not match the
loyalty profile").

## Phase 4 — Corroborate the offer

The user's own screenshots prove what posted; **independent corroboration proves what was
promised.** This matters because reps sometimes claim the offer was smaller than it was.

1. **Web search** for the public offer terms for that card around the application date (card
   blogs like AwardWallet, One Mile at a Time, Upgraded Points, The Points Guy document these
   with dates). A third-party article dated within a day or two of the account-open date is
   strong evidence the offer was live when the user applied.
2. **Wayback Machine** — find an archived snapshot of the issuer's own offer page near the
   application date. This is the strongest single artifact: the issuer's own page, timestamped,
   showing the exact offer. Construct/browse:
   `https://web.archive.org/web/<YYYYMMDD>000000*/<issuer offer page URL>` (calendar view), or
   a direct snapshot `https://web.archive.org/web/<YYYYMMDD>000000/<URL>`. Capture the snapshot
   URL — the timestamp in it is what makes it tamper-proof.

   Note: the web-fetch tool may refuse URLs that did not come from a prior search result, and
   search engines index archive snapshots poorly. If a snapshot can't be fetched directly, give
   the user the exact Wayback URLs to open themselves and tell them to screenshot the page
   **including the URL bar** (the timestamp).

3. **Caution:** do NOT cite the issuer's *current live* offer page if the offer has since
   changed — a rep glancing at a different current number gets confused. Use dated/archived
   evidence that matches the application period.

## Phase 5 — Generate the dispute packet

**Read `references/deliverables.md`** for the message templates, call scripts, and tracker.
Then assemble the case JSON and generate the documents.

1. **Build a case JSON** describing the dispute (cardholder, card last-4, loyalty member,
   offer, reconciliation rows, failure mode, evidence list, the ask). Schema and an example are
   in `references/case-schema.md`.
2. **Generate the PDFs** with the bundled scripts (they read the case JSON):
   - `python scripts/make_timeline_pdf.py case.json timeline.pdf` — the timeline +
     reconciliation table (miles and status-points columns).
   - `python scripts/make_status_pdf.py case.json status.pdf` — the status document:
     resolved-vs-outstanding summary, the offer evidence (embed the offer screenshot + Wayback
     citation if available), the activity-log evidence, loyalty-dashboard evidence, a
     "why this matters" explainer, and the specific ask.
   Pass screenshot paths in the case JSON to embed them. Both scripts depend on `reportlab`
   (`pip install reportlab --break-system-packages` if missing).
3. **Draft the messages** from the templates in `references/deliverables.md`:
   - one to the **loyalty program** (they credit status points),
   - one to the **issuer** (confirm the trigger / correct any false "it posted" claim).
   Produce them as ready-to-send text. If a tool for composing messages is available, use it;
   otherwise output the text inline.
4. **Honor input-field character limits.** Some issuer secure-message forms reject typographic
   characters (curly quotes, em dashes, angle brackets, math symbols, `{ }`). When a message is
   destined for such a form, also produce an **ASCII-safe version**: straight quotes only, no em
   dashes, no special symbols. Warn the user that copy-paste often auto-converts straight quotes
   to curly ones, and suggest paste-as-plain-text. Details in `references/deliverables.md`.
5. **Provide phone scripts and a follow-up tracker** (templates in `references/deliverables.md`).

Present the finished files to the user (use the file-presentation tool if available).

## Phase 6 — Escalation guidance

**Read `references/domain-knowledge.md`** for the full reference, but the essentials:

- **Route to the right party.** The issuer generally **cannot credit status-qualifying points**
  — the loyalty program does. The issuer's role is to confirm the spend goal/trigger. If the
  missing piece is status points, the loyalty program is the primary channel; if it's
  miles/points the issuer transferred but the loyalty side never received, both are in play.
- **Correct false "it posted" claims with their own data.** If a rep insists the bonus posted,
  the unanswerable reply is: "Please tell me the specific loyalty activity-log entry or
  dashboard line where it appears." They cannot, if it didn't.
- **Mind the posting window vs. genuine lateness.** Most programs say allow 6–8 weeks after the
  spend goal is met. Calculate from the trigger cycle, and point out when that window has clearly
  passed.
- **Status points are time-sensitive.** Status-qualifying points (PQP/MQD) usually apply to a
  specific program year and reset annually; flag urgency so a credit lands in the correct year.
- **Lead with the evidence stack, not another investigation.** When the case is airtight (offer
  proof + trigger + one half posted + the other demonstrably did not), the ask is to *credit it*,
  not to re-investigate.

## Boundaries

This skill provides **analysis and self-advocacy tools, not legal services**. It does not
manufacture wins: if the reconciliation shows the spend goal wasn't actually met, or the offer
terms had a genuine exclusion, say so plainly. Keep written messages to companies professional
and factual — profanity or threats in the record never help. Don't fabricate offer terms,
dates, or quotes; if a fact can't be corroborated, leave it out.
