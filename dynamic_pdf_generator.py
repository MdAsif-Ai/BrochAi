"""
brochure_generator.py
─────────────────────
A dynamic, section-based PDF brochure generator.

The AI (or you) describes the brochure as a list of typed sections.
The renderer handles all layout, pagination, and styling automatically.

USAGE
─────
    from brochure_generator import generate_pdf

    generate_pdf(BROCHURE, "output.pdf")

SECTION TYPES
─────────────
    "cover"    — Full-bleed hero cover page
    "text"     — Heading + one or more paragraphs
    "stats"    — Row of metric tiles  (list of [value, label])
    "cards"    — Grid of cards        (list of {name, body, tag?})
    "table"    — Two-column key→value table
    "list"     — Bullet / numbered list
    "team"     — People cards         (list of {name, role, bio?})
    "quote"    — Pull-quote with optional author
    "awards"   — Styled award rows    (list of {title, year?, note?})
    "partners" — Inline partner tags  (list of strings)
    "cta"      — Full-width call-to-action banner
    "contact"  — Contact details      (dict of label→value)
    "divider"  — Horizontal rule / visual break
    "columns"  — Two independent text columns (left, right dicts with text/heading)

EXAMPLE (Reliance Industries)
──────────────────────────────
See EXAMPLE_BROCHURE at the bottom of this file.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import Flowable

# ══════════════════════════════════════════════════════════════════════════════
#  THEME — change colours here to match any brand
# ══════════════════════════════════════════════════════════════════════════════

class Theme:
    PRIMARY     = colors.HexColor("#1C2E4A")   # deep navy
    ACCENT      = colors.HexColor("#D4A843")   # warm gold
    ACCENT_PALE = colors.HexColor("#F5E9C6")   # light gold tint
    OFF_WHITE   = colors.HexColor("#F8F9FA")
    DARK        = colors.HexColor("#1A1A2E")
    BODY        = colors.HexColor("#4A5568")
    RULE        = colors.HexColor("#D8DEE4")
    WHITE       = colors.white


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE GEOMETRY
# ══════════════════════════════════════════════════════════════════════════════

PAGE_W, PAGE_H = A4
MARGIN      = 18 * mm
CONTENT_W   = PAGE_W - 2 * MARGIN
HEADER_H    = 9 * mm
FOOTER_H    = 8 * mm


# ══════════════════════════════════════════════════════════════════════════════
#  STYLE REGISTRY
# ══════════════════════════════════════════════════════════════════════════════

def _s(name, **kw) -> ParagraphStyle:
    return ParagraphStyle(name, **kw)


S = {
    # ── Cover ─────────────────────────────────────────────────────────────
    "cover_company":  _s("cc",  fontName="Helvetica-Bold",   fontSize=34, textColor=Theme.WHITE,       leading=40),
    "cover_headline": _s("ch",  fontName="Helvetica-Bold",   fontSize=22, textColor=Theme.ACCENT_PALE, leading=28, spaceAfter=4),
    "cover_sub":      _s("cs",  fontName="Helvetica",        fontSize=13, textColor=Theme.WHITE,       leading=20, spaceAfter=4),
    "cover_tag":      _s("ct",  fontName="Helvetica-Oblique",fontSize=10, textColor=Theme.ACCENT,      leading=14),

    # ── Section headings ──────────────────────────────────────────────────
    "label":   _s("lbl", fontName="Helvetica-Bold",   fontSize=8,  textColor=Theme.ACCENT,   leading=12, letterSpacing=1.5),
    "h2":      _s("h2",  fontName="Helvetica-Bold",   fontSize=22, textColor=Theme.PRIMARY,  leading=28, spaceAfter=4, spaceBefore=2),
    "h3":      _s("h3",  fontName="Helvetica-Bold",   fontSize=14, textColor=Theme.PRIMARY,  leading=20, spaceAfter=4, spaceBefore=8),
    "h4":      _s("h4",  fontName="Helvetica-Bold",   fontSize=11, textColor=Theme.PRIMARY,  leading=16, spaceAfter=3),

    # ── Body ──────────────────────────────────────────────────────────────
    "body":    _s("bd",  fontName="Helvetica",        fontSize=10, textColor=Theme.BODY,     leading=16, spaceAfter=5),
    "body_b":  _s("bdb", fontName="Helvetica-Bold",   fontSize=10, textColor=Theme.DARK,     leading=16, spaceAfter=4),
    "italic":  _s("it",  fontName="Helvetica-Oblique",fontSize=10, textColor=Theme.BODY,     leading=16, spaceAfter=5),
    "small":   _s("sm",  fontName="Helvetica",        fontSize=8,  textColor=Theme.BODY,     leading=12),
    "small_b": _s("smb", fontName="Helvetica-Bold",   fontSize=8,  textColor=Theme.BODY,     leading=12),
    "bullet":  _s("blt", fontName="Helvetica",        fontSize=10, textColor=Theme.BODY,     leading=16, spaceAfter=3, leftIndent=14),

    # ── Cards ─────────────────────────────────────────────────────────────
    "card_name": _s("cn",  fontName="Helvetica-Bold",   fontSize=11, textColor=Theme.PRIMARY, leading=15, spaceAfter=2),
    "card_tag":  _s("ctg", fontName="Helvetica-Bold",   fontSize=7.5,textColor=Theme.ACCENT,  leading=11, spaceAfter=2, letterSpacing=0.8),
    "card_body": _s("cb",  fontName="Helvetica",        fontSize=8.5,textColor=Theme.BODY,    leading=13),

    # ── Table ─────────────────────────────────────────────────────────────
    "tbl_key":  _s("tk",  fontName="Helvetica-Bold",   fontSize=9,  textColor=Theme.PRIMARY, leading=14),
    "tbl_val":  _s("tv",  fontName="Helvetica",        fontSize=9,  textColor=Theme.BODY,    leading=14, spaceAfter=3),

    # ── Quote ─────────────────────────────────────────────────────────────
    "quote":      _s("qt",  fontName="Helvetica-BoldOblique", fontSize=13, textColor=Theme.PRIMARY, leading=21, leftIndent=16),
    "quote_auth": _s("qta", fontName="Helvetica",             fontSize=9,  textColor=Theme.BODY,    leading=13, leftIndent=16),

    # ── CTA ───────────────────────────────────────────────────────────────
    "cta_heading": _s("ctah", fontName="Helvetica-Bold",    fontSize=18, textColor=Theme.ACCENT_PALE, leading=24, spaceAfter=6),
    "cta_body":    _s("ctab", fontName="Helvetica",         fontSize=11, textColor=Theme.WHITE,       leading=18),

    # ── Footer ────────────────────────────────────────────────────────────
    "footer": _s("ft", fontName="Helvetica", fontSize=7.5, textColor=Theme.BODY, leading=10),
}


# ══════════════════════════════════════════════════════════════════════════════
#  CUSTOM FLOWABLES
# ══════════════════════════════════════════════════════════════════════════════

class AccentRule(Flowable):
    """Two-tone decorative rule (primary + accent)."""
    def __init__(self, width=None, space_after=10):
        super().__init__()
        self.width    = width or CONTENT_W
        self.height   = 3
        self._space   = space_after

    def draw(self):
        c = self.canv
        c.setFillColor(Theme.PRIMARY)
        c.rect(0, 1, self.width * 0.55, 2, fill=1, stroke=0)
        c.setFillColor(Theme.ACCENT)
        c.rect(self.width * 0.55, 1, self.width * 0.45, 2, fill=1, stroke=0)

    def wrap(self, *_):
        return self.width, self.height + self._space


class StatTile(Flowable):
    """Single metric tile — value in large type, label below."""
    def __init__(self, value: str, label: str, width: float):
        super().__init__()
        self.value = value
        self.label = label
        self.width = width
        self.height = 58

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        # Background
        c.setFillColor(Theme.PRIMARY)
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)

        # Gold top strip
        c.setFillColor(Theme.ACCENT)
        c.rect(0, h - 3, w, 3, fill=1, stroke=0)

        # Value
        fs = 24 if len(self.value) <= 6 else 18
        c.setFillColor(Theme.WHITE)
        c.setFont("Helvetica-Bold", fs)
        vw = c.stringWidth(self.value, "Helvetica-Bold", fs)
        c.drawString((w - vw) / 2, h * 0.38, self.value)

        # Label
        c.setFillColor(Theme.ACCENT_PALE)
        c.setFont("Helvetica", 7.5)
        lw = c.stringWidth(self.label.upper(), "Helvetica", 7.5)
        c.drawString((w - lw) / 2, h * 0.14, self.label.upper())


class QuoteBar(Flowable):
    """Left accent bar for quote sections."""
    def __init__(self, height: float):
        super().__init__()
        self.width  = 4
        self.height = height

    def draw(self):
        c = self.canv
        c.setFillColor(Theme.ACCENT)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CALLBACKS  (header + footer drawn on the canvas, not in the story)
# ══════════════════════════════════════════════════════════════════════════════

def _draw_cover(canvas, brochure: dict):
    """Full-bleed geometric cover."""
    w, h = PAGE_W, PAGE_H
    theme = brochure.get("theme", {})
    primary = colors.HexColor(theme.get("primary", "#1C2E4A"))
    accent  = colors.HexColor(theme.get("accent",  "#D4A843"))

    # Background fill
    canvas.setFillColor(primary)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)

    # Gold triangle — top-right
    canvas.setFillColor(accent)
    p = canvas.beginPath()
    p.moveTo(w * 0.58, h); p.lineTo(w, h); p.lineTo(w, h * 0.60); p.close()
    canvas.drawPath(p, fill=1, stroke=0)

    # Subtle ghost triangle — bottom-left
    canvas.setFillColorRGB(1, 1, 1, alpha=0.06)
    p2 = canvas.beginPath()
    p2.moveTo(0, 0); p2.lineTo(w * 0.40, 0); p2.lineTo(0, h * 0.30); p2.close()
    canvas.drawPath(p2, fill=1, stroke=0)

    # Gold bottom bar
    canvas.setFillColor(accent)
    canvas.rect(0, 0, w, 7 * mm, fill=1, stroke=0)

    # Website bottom-right
    website = brochure.get("website") or brochure.get("company", "")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#F5E9C6"))
    canvas.drawRightString(w - MARGIN, 10, website)


def _draw_interior_header(canvas, brochure: dict, page: int):
    """Thin header bar on pages 2+."""
    w = PAGE_W
    h = HEADER_H
    y = PAGE_H - h

    theme   = brochure.get("theme", {})
    primary = colors.HexColor(theme.get("primary", "#1C2E4A"))
    accent  = colors.HexColor(theme.get("accent",  "#D4A843"))

    canvas.setFillColor(primary)
    canvas.rect(0, y, w, h, fill=1, stroke=0)

    # Left accent stripe
    canvas.setFillColor(accent)
    canvas.rect(0, y, 3, h, fill=1, stroke=0)

    # Company name
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(colors.white)
    canvas.drawString(MARGIN, y + 3 * mm, brochure.get("company", "").upper())

    # Tagline right
    tagline = brochure.get("tagline", "")
    if tagline:
        canvas.setFont("Helvetica-Oblique", 7.5)
        canvas.setFillColor(colors.HexColor("#F5E9C6"))
        canvas.drawRightString(w - MARGIN, y + 3 * mm, tagline)


def _draw_footer(canvas, brochure: dict, page: int):
    """Page footer with rule, company name, page number, website."""
    w = PAGE_W
    y = FOOTER_H

    canvas.setStrokeColor(colors.HexColor("#D8DEE4"))
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, y, w - MARGIN, y)

    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#4A5568"))
    canvas.drawString(MARGIN, y - 9, brochure.get("company", ""))
    canvas.drawCentredString(w / 2, y - 9, f"— {page} —")
    canvas.drawRightString(w - MARGIN, y - 9, brochure.get("website", ""))


def make_page_callback(brochure: dict):
    """Return the onPage function that ReportLab calls per page."""
    def on_page(canvas, doc):
        canvas.saveState()
        page = doc.page
        if page == 1:
            _draw_cover(canvas, brochure)
        else:
            _draw_interior_header(canvas, brochure, page)
            _draw_footer(canvas, brochure, page)
        canvas.restoreState()
    return on_page


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION RENDERERS  — each returns a list of Flowables
# ══════════════════════════════════════════════════════════════════════════════

def _section_header(label_text: str, title_text: str) -> list:
    """Standard labelled section heading with accent rule."""
    return [
        Paragraph(label_text.upper(), S["label"]),
        Paragraph(title_text, S["h2"]),
        AccentRule(),
        Spacer(1, 8),
    ]


def render_cover(sec: dict, _brochure: dict) -> list:
    """Cover page — content rendered over the canvas background."""
    story = []
    story.append(Spacer(1, 88))

    company = sec.get("company") or _brochure.get("company", "")
    story.append(Paragraph(company.upper(), S["cover_company"]))
    story.append(Spacer(1, 10))

    if sec.get("headline"):
        story.append(Paragraph(sec["headline"], S["cover_headline"]))
    if sec.get("sub"):
        story.append(Paragraph(sec["sub"], S["cover_sub"]))
    if sec.get("tag"):
        story.append(Spacer(1, 16))
        story.append(Paragraph(sec["tag"], S["cover_tag"]))

    story.append(PageBreak())
    return story


def render_text(sec: dict, _b: dict) -> list:
    """Heading + one or more paragraphs of body text."""
    story = []
    label = sec.get("label", "")
    title = sec.get("title", "")

    if label or title:
        story += _section_header(label, title) if label else [
            Paragraph(title, S["h3"]), Spacer(1, 6)
        ]

    content = sec.get("content", "")
    if isinstance(content, str):
        for para in content.split("\n\n"):
            para = para.strip()
            if para:
                story.append(Paragraph(para, S["body"]))
    elif isinstance(content, list):
        for para in content:
            story.append(Paragraph(str(para), S["body"]))

    return story


def render_stats(sec: dict, _b: dict) -> list:
    """Row of stat tiles. items = list of [value, label] or {value, label}."""
    items = sec.get("items", [])
    if not items:
        return []

    story = []
    if sec.get("title"):
        story.append(Paragraph(sec["title"].upper(), S["label"]))
        story.append(Spacer(1, 6))

    # Normalize items
    parsed = []
    for it in items:
        if isinstance(it, (list, tuple)) and len(it) >= 2:
            parsed.append((str(it[0]), str(it[1])))
        elif isinstance(it, dict):
            parsed.append((str(it.get("value", "")), str(it.get("label", ""))))
        else:
            parsed.append((str(it), ""))

    # Split into rows of max 6
    row_size = 6 if len(parsed) >= 5 else len(parsed)
    gap = 5
    cw  = (CONTENT_W - gap * (row_size - 1)) / row_size

    for chunk_start in range(0, len(parsed), row_size):
        chunk = parsed[chunk_start: chunk_start + row_size]
        n = len(chunk)
        _cw = (CONTENT_W - gap * (n - 1)) / n
        cells  = [StatTile(v, l, _cw) for v, l in chunk]
        widths = [_cw] * n
        t = Table([cells], colWidths=widths, rowHeights=[58])
        t.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0),(-1,-1), gap // 2),
            ("RIGHTPADDING", (0,0),(-1,-1), gap // 2),
            ("TOPPADDING",   (0,0),(-1,-1), 0),
            ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    return story


def render_cards(sec: dict, _b: dict) -> list:
    """
    Grid of cards. Automatically chooses 1, 2, or 3 columns.
    items = list of {name, body, tag?} or [name, body] or just strings
    """
    items = sec.get("items", [])
    if not items:
        return []

    story = []
    if sec.get("label") or sec.get("title"):
        story += _section_header(sec.get("label",""), sec.get("title",""))

    if sec.get("intro"):
        story.append(Paragraph(sec["intro"], S["body"]))
        story.append(Spacer(1, 6))

    # Normalize
    cards = []
    for it in items:
        if isinstance(it, dict):
            cards.append({
                "name": str(it.get("name", it.get("title", ""))),
                "body": str(it.get("body", it.get("description", it.get("desc", "")))),
                "tag":  str(it.get("tag",  it.get("highlight", it.get("subtitle", "")))),
            })
        elif isinstance(it, (list, tuple)) and len(it) >= 2:
            cards.append({"name": str(it[0]), "body": str(it[1]), "tag": ""})
        else:
            cards.append({"name": str(it), "body": "", "tag": ""})

    n = len(cards)
    cols = 3 if n >= 5 else (2 if n >= 3 else 1)
    gap  = 7
    cw   = (CONTENT_W - gap * (cols - 1)) / cols

    rows = []
    row  = []
    for i, card in enumerate(cards):
        cell = []
        if card["name"]:
            cell.append(Paragraph(card["name"], S["card_name"]))
        if card["tag"]:
            cell.append(Paragraph(card["tag"].upper(), S["card_tag"]))
        if card["body"]:
            cell.append(Spacer(1, 2))
            cell.append(Paragraph(card["body"], S["card_body"]))
        row.append(cell if cell else [Paragraph("", S["body"])])
        if len(row) == cols:
            rows.append(row); row = []

    if row:  # pad last row
        while len(row) < cols:
            row.append([Paragraph("", S["body"])])
        rows.append(row)

    tbl_style = [
        ("BACKGROUND",    (0,0),(-1,-1), Theme.OFF_WHITE),
        ("BOX",           (0,0),(-1,-1), 0.4, Theme.RULE),
        ("INNERGRID",     (0,0),(-1,-1), 0.4, Theme.RULE),
        ("LINEABOVE",     (0,0),(-1,-1), 2.5, Theme.ACCENT),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 11),
        ("RIGHTPADDING",  (0,0),(-1,-1), 11),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]

    t = Table(rows, colWidths=[cw]*cols)
    t.setStyle(TableStyle(tbl_style))
    story.append(t)
    return story


def render_table(sec: dict, _b: dict) -> list:
    """Two-column key→value table. rows = list of [key, value] or {key, value}."""
    story = []
    if sec.get("label") or sec.get("title"):
        story += _section_header(sec.get("label",""), sec.get("title",""))

    rows_raw = sec.get("rows", sec.get("items", []))
    if not rows_raw:
        return story

    key_w = sec.get("key_width", 42 * mm)
    val_w = CONTENT_W - key_w
    rows  = []

    for r in rows_raw:
        if isinstance(r, (list, tuple)) and len(r) >= 2:
            k, v = str(r[0]), str(r[1])
        elif isinstance(r, dict):
            k = str(r.get("key",   r.get("label",  list(r.keys())[0] if r else "")))
            v = str(r.get("value", r.get("content",list(r.values())[0] if r else "")))
        else:
            k, v = str(r), ""
        rows.append([Paragraph(k, S["tbl_key"]), Paragraph(v, S["tbl_val"])])

    t = Table(rows, colWidths=[key_w, val_w])
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("LINEBELOW",     (0,0),(-1,-1), 0.3, Theme.RULE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story.append(t)
    return story


def render_list(sec: dict, _b: dict) -> list:
    """Bullet or numbered list."""
    story = []
    if sec.get("label") or sec.get("title"):
        story += _section_header(sec.get("label",""), sec.get("title",""))

    items    = sec.get("items", [])
    numbered = sec.get("numbered", False)

    for i, item in enumerate(items, 1):
        text   = str(item.get("text", item) if isinstance(item, dict) else item)
        prefix = f"{i}." if numbered else "&#9679;"
        story.append(Paragraph(f"{prefix}&nbsp;&nbsp;{text}", S["bullet"]))

    return story


def render_team(sec: dict, _b: dict) -> list:
    """
    People cards. items = list of {name, role, bio?}
    or [name, role, bio] tuples.
    """
    items = sec.get("items", [])
    if not items:
        return []

    story = []
    if sec.get("label") or sec.get("title"):
        story += _section_header(sec.get("label",""), sec.get("title",""))

    people = []
    for it in items:
        if isinstance(it, dict):
            people.append((
                str(it.get("name",  "")),
                str(it.get("role",  it.get("title", ""))),
                str(it.get("bio",   it.get("description", ""))),
            ))
        elif isinstance(it, (list, tuple)):
            vals = list(it) + ["", "", ""]
            people.append((str(vals[0]), str(vals[1]), str(vals[2])))
        else:
            people.append((str(it), "", ""))

    cols = min(3, len(people))
    cw   = CONTENT_W / cols
    gap  = 0

    rows = []
    row  = []
    for i, (name, role, bio) in enumerate(people):
        cell = []
        if name: cell.append(Paragraph(name, S["card_name"]))
        if role: cell.append(Paragraph(role, S["card_tag"]))
        if bio:
            cell.append(Spacer(1, 3))
            cell.append(Paragraph(bio, S["card_body"]))
        row.append(cell if cell else [Paragraph("", S["body"])])
        if len(row) == cols:
            rows.append(row); row = []

    if row:
        while len(row) < cols:
            row.append([Paragraph("", S["body"])])
        rows.append(row)

    t = Table(rows, colWidths=[cw]*cols)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), Theme.OFF_WHITE),
        ("BOX",           (0,0),(-1,-1), 0.4, Theme.RULE),
        ("INNERGRID",     (0,0),(-1,-1), 0.4, Theme.RULE),
        ("LINEABOVE",     (0,0),(-1,-1), 2.5, Theme.ACCENT),
        ("TOPPADDING",    (0,0),(-1,-1), 11),
        ("BOTTOMPADDING", (0,0),(-1,-1), 11),
        ("LEFTPADDING",   (0,0),(-1,-1), 11),
        ("RIGHTPADDING",  (0,0),(-1,-1), 11),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story.append(t)
    return story


def render_quote(sec: dict, _b: dict) -> list:
    """Pull-quote with optional author."""
    story = []
    story.append(HRFlowable(width="100%", thickness=0.5, color=Theme.RULE,
                             spaceBefore=4, spaceAfter=10))

    quote  = sec.get("text", sec.get("quote", ""))
    author = sec.get("author", "")
    role   = sec.get("role", "")
    company= sec.get("company", "")

    if quote:
        story.append(Paragraph(f"\u201c{quote}\u201d", S["quote"]))
    if author:
        attribution = author
        if role:    attribution += f", {role}"
        if company: attribution += f", {company}"
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"\u2014 {attribution}", S["quote_auth"]))

    story.append(HRFlowable(width="100%", thickness=0.5, color=Theme.RULE,
                             spaceBefore=10, spaceAfter=6))
    return story


def render_awards(sec: dict, _b: dict) -> list:
    """Styled award list. items = list of {title, year?, note?} or strings."""
    items = sec.get("items", [])
    if not items:
        return []

    story = []
    if sec.get("label") or sec.get("title"):
        story += _section_header(sec.get("label",""), sec.get("title",""))

    rows = []
    for it in items:
        if isinstance(it, dict):
            title = str(it.get("title", ""))
            detail= " · ".join(filter(None, [
                str(it.get("year",   "")),
                str(it.get("note",   "")),
                str(it.get("issuer", "")),
            ]))
        elif isinstance(it, (list, tuple)) and len(it) >= 2:
            title, detail = str(it[0]), str(it[1])
        else:
            title, detail = str(it), ""

        rows.append([
            Paragraph("&#9733;", S["card_tag"]),
            Paragraph(f"<b>{title}</b>", S["body_b"]),
            Paragraph(detail, S["small"]),
        ])

    key_w  = 14
    note_w = CONTENT_W * 0.34
    name_w = CONTENT_W - key_w - note_w

    t = Table(rows, colWidths=[key_w, name_w, note_w])
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LINEBELOW",     (0,0),(-1,-1), 0.3, Theme.RULE),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(t)
    return story


def render_partners(sec: dict, _b: dict) -> list:
    """Inline partner/tag chips. items = list of strings."""
    items = sec.get("items", [])
    if not items:
        return []

    story = []
    if sec.get("title"):
        story.append(Paragraph(sec["title"], S["h3"]))

    joined = "   ·   ".join([str(p) for p in items])
    story.append(Paragraph(joined, S["body"]))
    return story


def render_cta(sec: dict, _b: dict) -> list:
    """Full-width call-to-action banner."""
    story = [Spacer(1, 10)]

    content = []
    if sec.get("heading"):
        content.append(Paragraph(sec["heading"], S["cta_heading"]))
    if sec.get("body") or sec.get("text"):
        txt = sec.get("body") or sec.get("text", "")
        content.append(Paragraph(txt, S["cta_body"]))
    if sec.get("action"):
        content.append(Spacer(1, 8))
        content.append(Paragraph(f"&#8594;  {sec['action']}", S["cta_heading"]))

    t = Table([[ content ]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), Theme.PRIMARY),
        ("LINEABOVE",     (0,0),(0,0), 4, Theme.ACCENT),
        ("TOPPADDING",    (0,0),(0,0), 22),
        ("BOTTOMPADDING", (0,0),(0,0), 22),
        ("LEFTPADDING",   (0,0),(0,0), 22),
        ("RIGHTPADDING",  (0,0),(0,0), 22),
    ]))
    story.append(t)
    return story


def render_contact(sec: dict, _b: dict) -> list:
    """Contact details from a dict of label→value."""
    story = []
    if sec.get("title"):
        story.append(Paragraph(sec["title"], S["h3"]))
        story.append(Spacer(1, 4))

    items_raw = sec.get("items", sec.get("details", {}))

    # Accept dict or list of [label, value]
    if isinstance(items_raw, dict):
        pairs = list(items_raw.items())
    else:
        pairs = []
        for it in items_raw:
            if isinstance(it, (list, tuple)) and len(it) >= 2:
                pairs.append((str(it[0]), str(it[1])))
            elif isinstance(it, dict):
                k = str(it.get("label", it.get("key",   "")))
                v = str(it.get("value", it.get("detail","")))
                pairs.append((k, v))

    rows = [
        [Paragraph(str(k), S["tbl_key"]), Paragraph(str(v), S["tbl_val"])]
        for k, v in pairs if v
    ]
    if not rows:
        return story

    key_w = 38 * mm
    t = Table(rows, colWidths=[key_w, CONTENT_W - key_w])
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("LINEBELOW",     (0,0),(-1,-1), 0.3, Theme.RULE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    story.append(t)
    return story


def render_columns(sec: dict, _b: dict) -> list:
    """Two independent columns (left, right), each with heading + text."""
    story = []
    if sec.get("label") or sec.get("title"):
        story += _section_header(sec.get("label",""), sec.get("title",""))

    cw = (CONTENT_W - 10) / 2

    def col_content(col: dict) -> list:
        cell = []
        if col.get("heading"):
            cell.append(Paragraph(col["heading"], S["h3"]))
        txt = col.get("text", col.get("content", ""))
        if isinstance(txt, str):
            for p in txt.split("\n\n"):
                p = p.strip()
                if p:
                    cell.append(Paragraph(p, S["body"]))
        elif isinstance(txt, list):
            for p in txt:
                cell.append(Paragraph(str(p), S["body"]))
        return cell or [Paragraph("", S["body"])]

    left  = col_content(sec.get("left",  {}))
    right = col_content(sec.get("right", {}))

    t = Table([[left, right]], colWidths=[cw, cw])
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(-1,-1), 0),
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("RIGHTPADDING", (0,0),(0,0),   14),  # gap between columns
    ]))
    story.append(t)
    return story


def render_divider(sec: dict, _b: dict) -> list:
    label = sec.get("text", "")
    story = [Spacer(1, 6)]
    if label:
        story.append(Paragraph(label.upper(), S["label"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=Theme.RULE,
                             spaceBefore=4, spaceAfter=8))
    return story


# ══════════════════════════════════════════════════════════════════════════════
#  RENDERER DISPATCH
# ══════════════════════════════════════════════════════════════════════════════

RENDERERS = {
    "cover":    render_cover,
    "text":     render_text,
    "stats":    render_stats,
    "cards":    render_cards,
    "table":    render_table,
    "list":     render_list,
    "team":     render_team,
    "quote":    render_quote,
    "awards":   render_awards,
    "partners": render_partners,
    "cta":      render_cta,
    "contact":  render_contact,
    "columns":  render_columns,
    "divider":  render_divider,
    "page_break": lambda *_: [PageBreak()],
}


def _build_story(brochure: dict) -> list:
    story = []
    sections = brochure.get("sections", [])

    for i, sec in enumerate(sections):
        sec_type = str(sec.get("type", "text")).lower()
        renderer = RENDERERS.get(sec_type)

        if renderer is None:
            print(f"  ⚠  Unknown section type '{sec_type}' — skipping.")
            continue

        flowables = renderer(sec, brochure)

        # Spacing between sections (except cover + page_break)
        if flowables and sec_type not in ("cover", "page_break", "divider"):
            story.append(Spacer(1, 8))

        story.extend(flowables)

    return story


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

def generate_pdf(brochure: dict, output_path: str = "brochure.pdf") -> str:
    """
    Generate a professional PDF brochure.

    Parameters
    ----------
    brochure : dict
        Brochure definition. Required keys:
            "company"  : str   — company name (shown on cover + every page)
        Optional keys:
            "website"  : str   — shown on cover bottom + footer
            "tagline"  : str   — shown in interior page header
            "theme"    : dict  — {"primary": "#hex", "accent": "#hex"}
            "sections" : list  — ordered list of section dicts

    output_path : str
        File path to write the PDF to.

    Returns
    -------
    str — the output_path
    """
    # Apply optional per-brochure theme overrides
    theme = brochure.get("theme", {})
    if theme.get("primary"): Theme.PRIMARY = colors.HexColor(theme["primary"])
    if theme.get("accent"):
        Theme.ACCENT      = colors.HexColor(theme["accent"])
        # Recompute pale accent (mix with white)
        r, g, b = Theme.ACCENT.red, Theme.ACCENT.green, Theme.ACCENT.blue
        Theme.ACCENT_PALE = colors.Color(
            r + (1-r)*0.65, g + (1-g)*0.65, b + (1-b)*0.65
        )

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + HEADER_H + 2*mm,
        bottomMargin=MARGIN + FOOTER_H + 2*mm,
        title=f"{brochure.get('company', '')} — Brochure",
        author=brochure.get("company", ""),
    )

    cb = make_page_callback(brochure)
    story = _build_story(brochure)
    doc.build(story, onFirstPage=cb, onLaterPages=cb)

    pdf_bytes = buf.getvalue()
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    size_kb = len(pdf_bytes) // 1024
    print(f"✓  PDF written to '{output_path}'  ({size_kb} KB, {len(brochure.get('sections',[]))} sections)")
    return output_path


# ══════════════════════════════════════════════════════════════════════════════
#  EXAMPLE  — swap DATA below for any company the AI has described
# ══════════════════════════════════════════════════════════════════════════════

# EXAMPLE_BROCHURE = {
#     "company": "Reliance Industries",
#     "website": "www.reliance.com",
#     "tagline": "Reimagining Horizons",
#     "theme": {
#         "primary": "#1C2E4A",
#         "accent":  "#D4A843",
#     },
#     "sections": [

#         # ── COVER ─────────────────────────────────────────────────────────
#         {
#             "type":     "cover",
#             "headline": "Reimagining Horizons Through Reliance",
#             "sub":      "178 Years of Heritage  ·  A Digital Future",
#             "tag":      "Energy · Retail · Telecom · Technology",
#         },

#         # ── WHO WE ARE ────────────────────────────────────────────────────
#         {
#             "type":  "text",
#             "label": "Who We Are",
#             "title": "Company Overview",
#             "content": (
#                 "Founded in 1845, Reliance has grown from a regional trading house into one of "
#                 "the world's most diversified conglomerates. Today we serve 400 million customers "
#                 "across 12 countries through integrated operations in energy, retail, telecom, "
#                 "and digital services.\n\n"
#                 "Our 178-year legacy is not merely heritage — it is the foundation on which "
#                 "we build tomorrow's industries, combining deep industrial expertise with "
#                 "world-class technology and a relentless commitment to sustainability."
#             ),
#         },

#         # ── MISSION + VISION ──────────────────────────────────────────────
#         {
#             "type":  "columns",
#             "left": {
#                 "heading": "Our Mission",
#                 "text": (
#                     "To create world-class businesses that generate sustained value for our "
#                     "shareholders, employees, customers, and the communities we serve — "
#                     "while advancing India's position as a global economic leader."
#                 ),
#             },
#             "right": {
#                 "heading": "Our Vision",
#                 "text": (
#                     "To be a global leader in every sector we operate in, powered by "
#                     "innovation, technology, and an unwavering commitment to inclusive "
#                     "growth and environmental sustainability."
#                 ),
#             },
#         },

#         # ── KEY METRICS ───────────────────────────────────────────────────
#         {
#             "type":  "stats",
#             "title": "Key Metrics",
#             "items": [
#                 ["$240B",  "Market Cap"],
#                 ["400M+",  "Customers"],
#                 ["12",     "Countries"],
#                 ["$500M",  "Annual R&D"],
#                 ["236K",   "Employees"],
#                 ["178 yrs","Legacy"],
#             ],
#         },

#         {"type": "page_break"},

#         # ── PRODUCTS ──────────────────────────────────────────────────────
#         {
#             "type":  "cards",
#             "label": "What We Offer",
#             "title": "Products & Solutions",
#             "intro": (
#                 "Our integrated portfolio spans telecom, retail, energy, and digital services — "
#                 "engineered to deliver measurable value at every touchpoint."
#             ),
#             "items": [
#                 {
#                     "name": "SynergyChain",
#                     "tag":  "Supply Chain · AI",
#                     "body": "Blockchain-powered supply chain platform with real-time AI analytics, cutting logistics costs by up to 32%.",
#                 },
#                 {
#                     "name": "Reliance Digital Nexus",
#                     "tag":  "Enterprise IoT",
#                     "body": "End-to-end IoT data synthesis for predictive maintenance, smart asset tracking, and workflow automation.",
#                 },
#                 {
#                     "name": "Jio 5G & AirFibre",
#                     "tag":  "Connectivity",
#                     "body": "India's #1 network — ultra-low latency 5G and fixed wireless broadband for 100M+ homes.",
#                 },
#                 {
#                     "name": "Green Energy Portfolio",
#                     "tag":  "Sustainability",
#                     "body": "2 GW of operational solar & wind capacity, with a validated roadmap to 100 GW net-zero by 2035.",
#                 },
#                 {
#                     "name": "Retail Commerce Cloud",
#                     "tag":  "Commerce",
#                     "body": "Omni-channel infrastructure serving 18,000+ stores and 200M+ digital shoppers across India.",
#                 },
#                 {
#                     "name": "Logistics AI Platform",
#                     "tag":  "Automation",
#                     "body": "Last-mile and warehouse automation driving a 40% reduction in delivery times.",
#                 },
#             ],
#         },

#         {"type": "page_break"},

#         # ── AWARDS ────────────────────────────────────────────────────────
#         {
#             "type":  "awards",
#             "label": "Trust & Recognition",
#             "title": "Awards & Certifications",
#             "items": [
#                 {"title": "Fortune Global 500",           "year": "2024", "issuer": "Fortune Magazine"},
#                 {"title": "Best ESG Corporation — Asia",  "year": "2023", "issuer": "ESG Global Awards"},
#                 {"title": "Innovation Leader of the Year","year": "2023", "issuer": "CII India"},
#                 {"title": "ISO 27001 Information Security","issuer": "BSI Group"},
#                 {"title": "SBTi Net-Zero Validated",      "issuer": "Science Based Targets initiative"},
#             ],
#         },

#         {"type": "divider"},

#         # ── PARTNERS ──────────────────────────────────────────────────────
#         {
#             "type":  "partners",
#             "title": "Strategic Partners",
#             "items": ["Google Cloud", "Microsoft Azure", "Saudi Aramco", "bp", "Meta", "Brookfield AM"],
#         },

#         {"type": "divider"},

#         # ── TEAM ──────────────────────────────────────────────────────────
#         {
#             "type":  "team",
#             "title": "Leadership",
#             "items": [
#                 {
#                     "name": "Mukesh D. Ambani",
#                     "role": "Chairman & Managing Director",
#                     "bio":  "Transformed Reliance into India's most valuable conglomerate over four decades of visionary leadership.",
#                 },
#                 {
#                     "name": "Isha Ambani",
#                     "role": "Director, Retail & Digital",
#                     "bio":  "Leads Reliance Retail and JioMart — India's fastest-growing omni-channel commerce ecosystem.",
#                 },
#                 {
#                     "name": "Akash Ambani",
#                     "role": "Chairman, Jio Platforms",
#                     "bio":  "Drives India's 5G revolution and enterprise digital transformation at JioMart and beyond.",
#                 },
#             ],
#         },

#         {"type": "divider"},

#         # ── TESTIMONIAL ───────────────────────────────────────────────────
#         {
#             "type":    "quote",
#             "text":    (
#                 "SynergyChain reduced our cross-border logistics overhead by 28% in the first year. "
#                 "The ROI case was undeniable within six months of go-live."
#             ),
#             "author":  "Priya Sharma",
#             "role":    "Chief Supply Chain Officer",
#             "company": "Global Agri Holdings",
#         },

#         {"type": "page_break"},

#         # ── IMPACT ────────────────────────────────────────────────────────
#         {
#             "type":  "text",
#             "label": "Market Impact",
#             "title": "Why Reliance",
#             "content": (
#                 "Our infrastructure underpins 20% of India's GDP and actively serves governments "
#                 "in four nations. We consistently exceed industry ESG benchmarks, making Reliance "
#                 "the partner of choice for sovereigns and enterprises navigating the green transition.\n\n"
#                 "By 2030, we will invest $75 billion in clean energy, 6G infrastructure, and "
#                 "AI-driven vertical solutions — cementing our role as Asia's foremost integrated "
#                 "technology and energy powerhouse."
#             ),
#         },

#         # ── KEY PROOF POINTS ──────────────────────────────────────────────
#         {
#             "type": "table",
#             "rows": [
#                 ["Outcome",      "Quantified Result"],
#                 ["Logistics",    "28 % cost reduction via SynergyChain (Year 1)"],
#                 ["Uptime",       "40 % downtime reduction with Digital Nexus"],
#                 ["ROI",          "Average payback period under 18 months"],
#                 ["Sustainability","20 % ESG benchmark outperformance, SBTi validated"],
#                 ["Network",      "99.9 % uptime on Jio 5G across 12,000+ towers"],
#             ],
#         },

#         # ── CLIENTS ───────────────────────────────────────────────────────
#         {
#             "type":  "partners",
#             "title": "Trusted By",
#             "items": ["Tata Motors", "Infosys", "HDFC Bank", "Govt. of India",
#                       "Amazon India", "Walmart India", "Mahindra Group"],
#         },

#         # ── CTA ───────────────────────────────────────────────────────────
#         {
#             "type":    "cta",
#             "heading": "Let's Build Together",
#             "body":    (
#                 "Partner with Reliance to architect your organisation's intelligent transformation. "
#                 "Our enterprise team is ready to co-design a bespoke roadmap for your sector."
#             ),
#             "action":  "Request a Solutions Consultation",
#         },

#         # ── CONTACT ───────────────────────────────────────────────────────
#         {
#             "type":  "contact",
#             "title": "Get In Touch",
#             "items": {
#                 "Email":    "enterprise@reliance.com",
#                 "Phone":    "+91 22 3555 5000",
#                 "Website":  "www.reliance.com",
#                 "LinkedIn": "linkedin.com/company/reliance-industries",
#                 "Address":  "Maker Chambers IV, 222 Nariman Point, Mumbai 400 021",
#             },
#         },
#     ],
# }


# if __name__ == "__main__":
#     generate_pdf(EXAMPLE_BROCHURE, "brochure.pdf")
    