#!/usr/bin/env python3
"""
make_timeline_pdf.py — Generate a timeline + reconciliation PDF for a co-branded
card bonus dispute.

Usage:
    python make_timeline_pdf.py case.json timeline.pdf

Reads the case JSON (see references/case-schema.md) and produces a professional
2-section PDF: a chronological narrative and a cycle-by-cycle reconciliation table
with miles and (when present) status-points columns.

Depends on reportlab:  pip install reportlab --break-system-packages
"""
import json
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

NAVY = colors.HexColor("#1a3a5c")
ACCENT = colors.HexColor("#1a4b8c")
LIGHT = colors.HexColor("#eef3f8")
GREY = colors.HexColor("#5a6b7b")


def g(d, *keys, default=""):
    """Safe nested get."""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def fmt(n):
    try:
        return f"{int(n):,}"
    except (ValueError, TypeError):
        return str(n)


def build(case, out_path):
    doc = SimpleDocTemplate(out_path, pagesize=letter,
                            topMargin=0.7 * inch, bottomMargin=0.7 * inch,
                            leftMargin=0.8 * inch, rightMargin=0.8 * inch)
    ss = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=ss["Title"], fontSize=20, textColor=NAVY,
                        spaceAfter=4, alignment=TA_LEFT)
    SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontSize=10.5, textColor=GREY,
                         spaceAfter=14, leading=14)
    H = ParagraphStyle("H", parent=ss["Heading2"], fontSize=13, textColor=ACCENT,
                       spaceBefore=14, spaceAfter=6)
    BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontSize=10, leading=14,
                          spaceAfter=6)
    label = g(case, "offer", "status_points_label", default="status points")
    sp_amt = g(case, "offer", "status_points", default=0)
    has_sp = bool(sp_amt)

    S = []
    S.append(Paragraph(f"{g(case,'card')} Welcome Bonus — Timeline & Reconciliation", H1))
    summary = g(case, "summary") or "Reconciliation of issuer transfers against loyalty-account postings."
    S.append(Paragraph(summary, SUB))

    # Reference block
    ref = [
        ["Cardholder", g(case, "cardholder")],
        [f"{g(case,'issuer')} card", f"{g(case,'card')} (ending {g(case,'card_last4')})"],
        [f"{g(case,'loyalty_program')} account", g(case, "member_number") +
         (f" ({g(case,'member_status')})" if g(case, "member_status") else "")],
        ["Account opened", g(case, "account_open_date")],
        ["Offer", _offer_line(case)],
    ]
    t = Table(ref, colWidths=[1.7 * inch, 5.0 * inch])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT]),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cdd8e3")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e3eaf1")),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
    ]))
    S.append(t)

    # Diagnosis
    if g(case, "failure_mode"):
        S.append(Paragraph("Diagnosis", H))
        S.append(Paragraph(g(case, "failure_mode"), BODY))

    # Timeline narrative
    S.append(Paragraph("Timeline", H))
    for line in _timeline_lines(case):
        S.append(Paragraph(line, BODY))

    # Reconciliation table
    rows = g(case, "reconciliation", default=[])
    if rows:
        S.append(Paragraph("Reconciliation — issuer reported vs. loyalty received", H))
        header = ["Cycle", "Issuer reported (mi)", "Loyalty received (mi)", "Note"]
        data = [header]
        tot_rep = tot_rec = 0
        for r in rows:
            rep = r.get("issuer_reported_miles", 0) or 0
            rec = r.get("loyalty_received_miles", 0) or 0
            tot_rep += rep if isinstance(rep, (int, float)) else 0
            tot_rec += rec if isinstance(rec, (int, float)) else 0
            data.append([r.get("cycle", ""), fmt(rep), fmt(rec),
                         Paragraph(r.get("note", ""),
                                   ParagraphStyle("n", fontSize=8.5, leading=11))])
        data.append(["Total", fmt(tot_rep), fmt(tot_rec), ""])
        rt = Table(data, colWidths=[1.0 * inch, 1.5 * inch, 1.5 * inch, 2.7 * inch])
        rt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 0), (2, -1), "RIGHT"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, LIGHT]),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#dde7f1")),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("LINEABOVE", (0, -1), (-1, -1), 0.7, NAVY),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cdd8e3")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        S.append(rt)

    # Outstanding callout (status points)
    outstanding = g(case, "outstanding", default=[])
    if outstanding:
        S.append(Spacer(1, 10))
        body = "<b>Outstanding:</b> " + " ".join(outstanding)
        if has_sp:
            body += (f"<br/><br/>Note: {label} never appears on a credit card statement — it is "
                     f"a loyalty-program currency. Its absence from statements is expected and is "
                     f"not evidence it was not earned; it must be verified in the loyalty account.")
        call = Table([[Paragraph(body, ParagraphStyle("c", fontSize=9.5, leading=13,
                                                      textColor=colors.HexColor("#7a2a2a")))]],
                     colWidths=[6.7 * inch])
        call.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fbeaea")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#d98c8c")),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        S.append(call)

    if g(case, "ask"):
        S.append(Paragraph("Requested resolution", H))
        S.append(Paragraph(g(case, "ask"), BODY))

    doc.build(S)
    print(f"Wrote {out_path}")


def _offer_line(case):
    o = case.get("offer", {})
    parts = []
    if o.get("miles"):
        parts.append(f"{fmt(o['miles'])} miles")
    if o.get("status_points"):
        parts.append(f"{fmt(o['status_points'])} {o.get('status_points_label','status points')}")
    base = " + ".join(parts) if parts else "welcome bonus"
    tail = ""
    if o.get("spend_requirement") or o.get("window"):
        tail = f" after {o.get('spend_requirement','')}".rstrip()
        if o.get("window"):
            tail += f" in the {o['window']}"
    return base + tail


def _timeline_lines(case):
    """Assemble narrative lines from available fields."""
    lines = []
    if case.get("account_open_date"):
        lines.append(f"<b>{case['account_open_date']}</b> — {case.get('card','Card')} opened "
                     f"(account ending {case.get('card_last4','')}).")
    if case.get("spend_goal_met_cycle"):
        trig = f' Issuer posted "{case["bonus_trigger_line"]}".' if case.get("bonus_trigger_line") else ""
        lines.append(f"<b>{case['spend_goal_met_cycle']}</b> — spend goal met.{trig}")
    if case.get("in_app_confirmation"):
        d = case.get("in_app_confirmation_date", "")
        lines.append(f"<b>{d}</b> — loyalty program confirmed earning in its own UI: "
                     f"\u201c{case['in_app_confirmation']}\u201d")
    for r in case.get("resolved", []):
        lines.append(f"\u2713 {r}")
    for o in case.get("outstanding", []):
        lines.append(f"\u2717 <b>Outstanding:</b> {o}")
    if not lines:
        lines.append("Timeline details not provided.")
    return lines


def main():
    if len(sys.argv) < 3:
        print("Usage: python make_timeline_pdf.py <case.json> <out.pdf>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        case = json.load(f)
    build(case, sys.argv[2])


if __name__ == "__main__":
    main()
