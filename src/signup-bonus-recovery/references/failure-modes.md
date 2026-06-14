# Failure Modes — Diagnostic Playbook

Match the reconciliation (Phase 2) against these patterns. Real cases are often a combination
(e.g. a name mismatch that *also* left the status-points half unposted). Name the mode(s)
explicitly and tie each to specific evidence.

---

## 1. Name mismatch → duplicate or changed loyalty account

**Signature:** The issuer reports miles/points transferred on the statement, but they do not
appear in the loyalty account the user is looking at. A second loyalty member number exists,
or the issuer says the member number "was changed." Often some cycles post correctly (after a
name fix) while earlier cycles vanished.

**Why it happens:** The card is issued under one name spelling (e.g. first + last name only)
while the loyalty profile is under another (e.g. full legal name including a middle name). The
transfer routes to a newly-created or alternate member number that matches the card name,
stranding the miles —
including the welcome bonus — in an account the user never checks.

**The fix:** Identify both member numbers. The loyalty program **merges** the duplicate into the
primary account (or relinks the card to the correct number). After a merge, stranded miles —
and often the bonus — post to the surviving account, frequently **backdated** to the original
statement date. Confirm the surviving number and verify each previously-missing component lands.

**Tell from evidence:** statement shows transfer; loyalty export of the *primary* account shows
nothing for those dates; later cycles (post-fix) reconcile cleanly. The split between
"vanished" early cycles and "clean" later cycles pinpoints when the name/link was corrected.

---

## 2. Status-points half missing (miles posted, PQP/MQD did not)

**Signature:** The bonus *miles/points* are present in the loyalty account, but the
**status-qualifying points** component of the welcome offer is absent. The loyalty dashboard's
status-points view shows the spend-based earn but **Bonus = 0 / Promo = 0**.

**Why it happens:** Miles and status points are awarded by **different mechanisms**. Miles
transfer with the issuer pipeline; status points are a separate promotional award the loyalty
program posts when signaled. The miles half can succeed while the status-points award is never
triggered or gets dropped — especially after a merge that backfilled miles but not the promo.

**The fix:** This is **loyalty-side only** — the issuer cannot credit status points. Ask the
loyalty program to post the status-points welcome component to the correct member number for the
correct program year. Provide the offer proof (the status-points amount is in the published
terms) and the in-app confirmation screenshot if one exists.

**Tell from evidence:** miles reconcile; the status-points dashboard shows spend-earn only with
Bonus/Promo at zero; no activity-log entry for a status-points bonus credit. Remember the
statement *never* shows status points — their absence from statements is expected, not proof.

---

## 3. Partial post (base posted, bonus delta did not)

**Signature:** Some miles posted, but fewer than owed — the shortfall equals a specific bonus
component (e.g. the category multiplier bonus, or the welcome-bonus delta).

**Why it happens:** Multi-component awards (base + category bonus + welcome bonus) can post in
pieces; one piece lands and another is dropped, often during a systems hiccup or account relink.

**The fix:** Compute the exact delta and identify which component it maps to. Ask the party that
owns that component to post the remainder. If it's a transferred-miles delta, the issuer is in
play; if it's a loyalty promo, the loyalty program is.

**Tell from evidence:** "due 48k, received 37k — the 11k delta is exactly the category bonus."
The clean arithmetic of the shortfall identifies the missing piece.

---

## 4. Nothing posted yet — window vs. genuine lateness

**Signature:** No bonus visible at all.

**Decision before escalating:** Determine whether the **posting window** has actually elapsed.
Most programs say allow **6–8 weeks after the spend goal is met** (calculate from the cycle in
which the bonus-trigger line appeared, not from account opening). If still inside the window,
the right move is usually to wait and set a reminder — escalating early just gets a boilerplate
"please allow 6–8 weeks" reply. If clearly past it, escalate with the trigger date documented.

**Tell from evidence:** locate the trigger cycle on the statement; count forward. State plainly
whether the window has passed.

---

## 5. Wrong-account routing (stale member number on file)

**Signature:** Correct, single loyalty account, but transfers land somewhere else or not at all
because the issuer has an outdated/typo'd member number saved on the card.

**The fix:** Correct the member number on file with the issuer, then have mis-routed transfers
re-credited. Verify the number on the card profile matches the loyalty account exactly.

---

## Cross-cutting tells

- **"Issuer says sent, loyalty says no record."** Classic seam failure — pull both sides and
  show where the chain breaks. Don't accept either party's word over the documents.
- **Backdating after a fix.** Merges/relinks often post missing items backdated to the original
  date. Re-pull the loyalty export after any account change before concluding something is still
  missing — it may have quietly posted.
- **Status points are invisible on statements.** Never treat their absence from a credit card
  statement as evidence they weren't earned. Verify status points only in the loyalty account.
