#!/usr/bin/env python3
"""
make_status_pdf.py — Generate a status document for a co-branded card bonus dispute.

Usage:
    python make_status_pdf.py case.json status.pdf

Reads the case JSON (see references/case-schema.md) and produces a status document:
resolved-vs-outstanding summary, the offer evidence (embeds the offer screenshot +
Wayback citation when provided), an activity-log evidence table, loyalty-dashboard
evidence (embeds screenshots when provided), a "why this matters" explainer, and the
specific ask. Screenshot panels are skipped automatically if a path is missing or the
file does not exist.

Depends on reportlab + pillow:
    pip install reportlab pillow --break-system-packages
"""
import json
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image, KeepTogether, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

NAVY = colors.HexColor("#1a3a5c")
ACCENT = colors.HexColor("#1a4b8c")
LIGHT = colors.HexColor("#eef3f8")
GREY = colors.HexColor("#5a6b7b")
GREEN = colors.HexColor("#1f6b3a")
RED = colors.HexColor("#7a2a2a")


def g(d, *keys, default=""):
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


def img_dims(path, target_w):
    """Return (w, h) scaled to target_w preserving aspect; fallback if PIL missing."""
    try:
        from PIL import Image as PILImage
        w, h = PILImage.open(path).size
        return target_w, target_w * h / w
    except Exception:
        return target_w, target_w * 0.6


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
    BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontSize=10, leading=14, spaceAfter=6)
    SMALL = ParagraphStyle("SMALL", parent=ss["Normal"], fontSize=9, leading=12, textColor=GREY)
    CAP = ParagraphStyle("CAP", parent=ss["Normal"], fontSize=8.5, leading=11,
                         textColor=GREY, alignment=TA_CENTER, spaceAfter=2)
    MONO = "Courier"

    label = g(case, "offer", "status_points_label", default="status points")
    has_sp = bool(g(case, "offer", "status_points", default=0))
    shots = case.get("screenshots", {}) or {}

    S = []
    S.append(Paragraph(f"{g(case,'card')} Welcome Bonus — Status Update", H1))
    S.append(Paragraph(g(case, "summary") or "Status of the welcome-bonus posting.", SUB))

    # Reference block
    ref = [
        ["Cardholder", g(case, "cardholder")],
        [f"{g(case,'issuer')} card", f"{g(case,'card')} (ending {g(case,'card_last4')})"],
        [f"{g(case,'loyalty_program')} account", g(case, "member_number") +
         (f" ({g(case,'member_status')})" if g(case, "member_status") else "")],
        ["Outstanding item", _outstanding_short(case)],
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
    S.append(Spacer(1, 8))

    # Two-column resolved / outstanding
    resolved = case.get("resolved", []) or []
    outstanding = case.get("outstanding", []) or []
    res_html = "<b>\u2713 RESOLVED</b><br/><br/>" + "<br/><br/>".join(resolved) if resolved else \
        "<b>\u2713 RESOLVED</b><br/><br/>(none recorded)"
    out_html = "<b>\u2717 STILL OUTSTANDING</b><br/><br/>" + "<br/><br/>".join(outstanding) if outstanding else \
        "<b>\u2717 STILL OUTSTANDING</b><br/><br/>(none recorded)"
    gstyle = ParagraphStyle("g", fontSize=9.5, leading=13, textColor=GREEN)
    rstyle = ParagraphStyle("r", fontSize=9.5, leading=13, textColor=RED)
    two = Table([[Paragraph(res_html, gstyle), Paragraph(out_html, rstyle)]],
                colWidths=[3.25 * inch, 3.25 * inch])
    two.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#eaf5ee")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#fbeaea")),
        ("BOX", (0, 0), (0, 0), 1, colors.HexColor("#9ccbad")),
        ("BOX", (1, 0), (1, 0), 1, colors.HexColor("#d98c8c")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    S.append(two)

    # The offer you applied for
    S.append(Paragraph("The offer you applied for", H))
    offer_txt = (f"The issuer advertised the {g(case,'card')} welcome offer as "
                 f"<b>{_offer_line(case)}</b>")
    if g(case, "offer", "offer_url"):
        offer_txt += " on the issuer's own page. "
    else:
        offer_txt += ". "
    if g(case, "offer", "wayback_date"):
        offer_txt += "It is verifiable as live at the time of account opening via the archived snapshot cited below."
    S.append(Paragraph(offer_txt, BODY))

    offer_shot = shots.get("offer")
    if offer_shot and os.path.exists(offer_shot):
        w, h = img_dims(offer_shot, 6.0 * inch)
        panel = [Image(offer_shot, width=w, height=h)]
        if g(case, "offer", "offer_url"):
            panel.append(Paragraph(f'Source: issuer offer page, '
                                   f'<font name="{MONO}" size="8">{g(case,"offer","offer_url")}</font>', CAP))
        if g(case, "offer", "wayback_url"):
            panel.append(Paragraph(
                f'Verified live at account opening via Wayback Machine snapshot '
                f'dated <b>{g(case,"offer","wayback_date")}</b>:<br/>'
                f'<font name="{MONO}" size="7" color="#1a4b8c">{g(case,"offer","wayback_url")}</font>', CAP))
        S.append(KeepTogether(panel))
    elif g(case, "offer", "wayback_url"):
        S.append(Paragraph(
            f'Archived offer page (issuer&rsquo;s own page, timestamped), dated '
            f'<b>{g(case,"offer","wayback_date")}</b>:<br/>'
            f'<font name="{MONO}" size="8" color="#1a4b8c">{g(case,"offer","wayback_url")}</font>', SMALL))

    # Activity-log evidence
    ev = case.get("evidence_rows", []) or []
    if ev:
        S.append(Paragraph(f"Evidence from {g(case,'loyalty_program')} activity log", H))
        note = ("Lines from the loyalty activity export confirming what posted."
                + (f" Note the {label} column on the bonus credit is zero." if has_sp else ""))
        S.append(Paragraph(note, BODY))
        header = ["Date", "Description", "Miles", label if has_sp else "—"]
        data = [header]
        hl_rows = []
        for i, r in enumerate(ev, start=1):
            data.append([r.get("date", ""), r.get("description", ""),
                         fmt(r.get("miles", 0)), fmt(r.get("status_points", 0))])
            if r.get("highlight"):
                hl_rows.append(i)
        et = Table(data, colWidths=[1.0 * inch, 3.3 * inch, 1.1 * inch, 1.1 * inch])
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("FONTNAME", (0, 1), (0, -1), MONO),
            ("ALIGN", (2, 0), (3, -1), "RIGHT"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cdd8e3")),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
        for hr in hl_rows:
            style.append(("BACKGROUND", (0, hr), (-1, hr), colors.HexColor("#fdeeee")))
            style.append(("FONTNAME", (1, hr), (1, hr), "Helvetica-Bold"))
            style.append(("TEXTCOLOR", (3, hr), (3, hr), RED))
            style.append(("FONTNAME", (3, hr), (3, hr), "Helvetica-Bold"))
        et.setStyle(TableStyle(style))
        S.append(et)

    # Dashboard screenshots
    dash_panels = []
    if shots.get("dashboard_miles") and os.path.exists(shots["dashboard_miles"]):
        w, h = img_dims(shots["dashboard_miles"], 4.2 * inch)
        dash_panels += [Paragraph("Loyalty dashboard — miles", CAP),
                        Image(shots["dashboard_miles"], width=w, height=h), Spacer(1, 6)]
    if shots.get("dashboard_status") and os.path.exists(shots["dashboard_status"]):
        w, h = img_dims(shots["dashboard_status"], 4.2 * inch)
        dash_panels += [Paragraph(f"Loyalty dashboard — {label}", CAP),
                        Image(shots["dashboard_status"], width=w, height=h)]
    if shots.get("confirmation") and os.path.exists(shots["confirmation"]):
        w, h = img_dims(shots["confirmation"], 4.6 * inch)
        dash_panels += [Spacer(1, 6), Paragraph("In-app earning confirmation", CAP),
                        Image(shots["confirmation"], width=w, height=h)]
    if dash_panels:
        S.append(Paragraph(f"Confirmed by {g(case,'loyalty_program')}'s own account views", H))
        if has_sp:
            S.append(Paragraph(
                f"The miles correction is visible; the {label} correction is not. "
                f"Same account, same session: the miles row updated, the {label} row did not. "
                f"That asymmetry is the remaining issue.", BODY))
        S.append(KeepTogether(dash_panels))

    # Why this matters
    if has_sp:
        S.append(Paragraph(f"Why the {label} matters", H))
        S.append(Paragraph(
            f"{label} is a separate loyalty currency from redeemable miles, used to qualify for "
            f"elite status. It is awarded by the loyalty program (not the card issuer) and never "
            f"appears on a credit card statement. {label} typically applies to a specific program "
            f"year and resets annually, so a credit is time-sensitive and must land in the correct "
            f"program year.", BODY))

    # The ask
    if g(case, "ask"):
        S.append(Paragraph("Requested resolution", H))
        S.append(Paragraph(f"<b>{g(case,'ask')}</b>", BODY))

    doc.build(S)
    print(f"Wrote {out_path}")


def _offer_line(case):
    o = case.get("offer", {})
    parts = []
    if o.get("miles"):
        parts.append(f"{fmt(o['miles'])} bonus miles")
    if o.get("status_points"):
        parts.append(f"{fmt(o['status_points'])} {o.get('status_points_label','status points')}")
    base = " + ".join(parts) if parts else "welcome bonus"
    tail = ""
    if o.get("spend_requirement") or o.get("window"):
        tail = f" after spending {o.get('spend_requirement','')}".rstrip()
        if o.get("window"):
            tail += f" in the {o['window']}"
    return base + tail


def _outstanding_short(case):
    out = case.get("outstanding", []) or []
    if out:
        return out[0]
    o = case.get("offer", {})
    if o.get("status_points"):
        return f"{fmt(o['status_points'])} {o.get('status_points_label','status points')} welcome bonus"
    return "welcome bonus"


def main():
    if len(sys.argv) < 3:
        print("Usage: python make_status_pdf.py <case.json> <out.pdf>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        case = json.load(f)
    build(case, sys.argv[2])


if __name__ == "__main__":
    main()
