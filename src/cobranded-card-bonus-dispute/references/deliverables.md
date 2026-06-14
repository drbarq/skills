# Deliverables — Templates, Scripts, and Field Rules

Everything the dispute packet contains besides the PDFs. Adapt names, numbers, and the specific
missing component to the case. Keep all messages professional and factual.

---

## Message to the LOYALTY PROGRAM (they credit status points / merge accounts)

Use when the missing piece is status points, or after a merge to confirm a backfill. Lead with
the offer name (programs key off it), then the dated facts.

> Subject: [Program] — [missing component] from [Card] welcome offer has not posted
>
> Hi [name],
>
> Thank you. The promotion is the **[Card] new cardmember welcome offer**: [bonus amount] +
> [status-points amount] after spending [spend req] in the first [window]. The offer is
> documented on [issuer]'s own page ([offer URL]) under "NEW CARDMEMBER OFFER," verified live at
> the time of my account opening via a Wayback Machine snapshot dated [date].
>
> Key facts:
> - Account opened [date] ([Card], ending [last4]).
> - Spend goal met during the [month] statement cycle; [issuer] posted "[bonus trigger line]" on
>   the [date] statement.
> - [Loyalty]'s own system confirmed earning on [date]: "[in-app confirmation text]."
> - The [bonus miles] have posted to [member number] ([date]).
> - The [status points] have NOT posted. My [program-year] status-points view shows
>   [spend earn] with Bonus 0 / Promo 0.
>
> We are past the 6–8 week window (spend goal met [month]; the miles half posted [date]).
>
> Please credit the [status-points amount] to [member number] for the [program-year] program
> year. This is time-sensitive, as [program-year] status points apply to [year+1] status
> qualification. I have attached a status document with the full timeline and evidence.
>
> [Member number] · Card ending [last4] · Account-open date [date]
>
> Thank you, [name]

---

## Message to the ISSUER (confirm trigger / correct a false "it posted" claim)

Use to keep the issuer from closing the case as resolved, and to correct reps who wrongly claim
the status-points half posted. Open by acknowledging what *is* correct so it doesn't read as
combative, then correct the record with the loyalty program's own data.

> Subject: [Card] — [status-points component] has not posted (please reopen)
>
> Hi [name],
>
> Thank you for the response. The [bonus miles] have posted to [member number] — confirmed on my
> end. The [status points], however, have not posted, and this is verifiable in [loyalty]'s own
> system:
> - My [loyalty] [program-year] dashboard shows status points of [spend earn], with Bonus 0 and
>   Promo 0. The welcome-bonus status points would appear in the Bonus row if credited.
> - My loyalty activity export shows no entry for a welcome-bonus status-points credit. The
>   [date] "[bonus trigger line]" entry that credited the miles shows status points = 0.
>
> The offer I qualified for is the [Card] new cardmember welcome offer: [bonus amount] AND
> [status-points amount] after spending [spend req] in the first [window], advertised on your own
> page at [offer URL] (verified live at my application via a Wayback snapshot dated [date]). The
> miles half is resolved; the status-points half is not.
>
> Please reopen this case. I have attached a status document walking through the evidence,
> including screenshots of the loyalty dashboard showing the status points at zero.
>
> Card ending [last4] · [Member number] · Account-open date [date]
>
> Thank you, [name]

---

## ASCII-safe variant (for issuer secure-message forms)

Some issuer secure-message inputs reject typographic characters. A known-restrictive set blocks:
`} > { ÷ ×` and the **curly quotes** `" " ' '` (plus other symbols like a rupee sign). When a
message targets such a form, also produce a plain-ASCII version:

- Replace curly quotes with **straight** `"` and `'` (or drop quotes entirely).
- Replace em dashes `—` with commas, colons, or hyphens.
- Drop service marks (℠), trademark (™), and other special symbols.
- Avoid `< > { }`.

**Copy-paste warning to relay to the user:** browsers and forms frequently auto-convert straight
quotes into curly ones on paste, which then get rejected. Advise **paste-as-plain-text**
(Cmd+Shift+V / Ctrl+Shift+V), or pasting through a plain-text editor first. If a form still
rejects the text, the usual culprit is an autocorrected apostrophe — search for the curly `'`
and replace with the straight `'`.

---

## Phone scripts

**Loyalty program (status-points credit):**
> "I'm calling about the [Card] new cardmember welcome offer — [bonus amount] plus
> [status-points amount] after [spend req]. I opened the card [date], met the spend goal in
> [month], and the [bonus miles] have posted to [member number]. The [status-points amount] has
> not. Your own dashboard shows my status points with Bonus and Promo at zero. The offer is
> documented on [issuer]'s page and archived from my application date. I'd like the
> [status-points amount] credited to [member number] for the [program-year] program year."

If front-line can't: "Can this go to the team that handles promotional status-point postings?
What's the case/reference number, and when should I expect the posting?"

**Issuer (confirm trigger / reopen):**
> "I'm not disputing the miles — those posted. The status-points half of the welcome offer never
> posted to my loyalty account, and the loyalty dashboard shows it at zero. I need this reopened.
> Can you confirm the spend-goal trigger date on file and that the full welcome offer was sent?"

If a rep claims it all posted: "Please tell me the specific loyalty activity-log entry or
dashboard line where the status points appear — I can pull either right now."

---

## Follow-up tracker (give the user this table to maintain)

The thing that kills disputes is losing the thread across calls/messages. Provide a simple log:

| Date | Channel (loyalty/issuer) | Rep name / ID | Case # | What they said | Promised action | Follow-up by |
|------|--------------------------|---------------|--------|----------------|-----------------|--------------|
| | | | | | | |

Encourage: get a case/reference number every contact; note the promised posting date; if it
passes, reference the prior case number in the next contact rather than starting over.
