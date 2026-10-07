from pathlib import Path
import html

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# ============================================================
# COLORS
# ============================================================

NAVY = colors.HexColor("#172554")

BLUE = colors.HexColor("#2563EB")
BLUE_SOFT = colors.HexColor("#EFF6FF")

GREEN = colors.HexColor("#16A34A")
GREEN_SOFT = colors.HexColor("#F0FDF4")

ORANGE = colors.HexColor("#EA580C")
ORANGE_SOFT = colors.HexColor("#FFF7ED")

PURPLE = colors.HexColor("#7C3AED")
PURPLE_SOFT = colors.HexColor("#F5F3FF")

DARK = colors.HexColor("#172033")
TEXT = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")

WHITE = colors.white
BORDER = colors.HexColor("#E2E8F0")


# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()


COVER_BRAND = ParagraphStyle(
    "CoverBrand",
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=14,
    textColor=colors.HexColor("#93C5FD"),
)


COVER_TITLE = ParagraphStyle(
    "CoverTitle",
    fontName="Helvetica-Bold",
    fontSize=29,
    leading=34,
    textColor=WHITE,
)


COVER_SUBTITLE = ParagraphStyle(
    "CoverSubtitle",
    fontName="Helvetica",
    fontSize=11,
    leading=17,
    textColor=colors.HexColor("#CBD5E1"),
)


PAGE_TITLE = ParagraphStyle(
    "PageTitle",
    fontName="Helvetica-Bold",
    fontSize=21,
    leading=25,
    textColor=NAVY,
    spaceAfter=5,
)


PAGE_SUBTITLE = ParagraphStyle(
    "PageSubtitle",
    fontName="Helvetica",
    fontSize=9.5,
    leading=14,
    textColor=MUTED,
)


SECTION_TITLE = ParagraphStyle(
    "SectionTitle",
    fontName="Helvetica-Bold",
    fontSize=15,
    leading=19,
    textColor=NAVY,
    spaceBefore=8,
    spaceAfter=8,
)


CARD_TITLE = ParagraphStyle(
    "CardTitle",
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=14,
    textColor=NAVY,
    spaceAfter=7,
)


BODY = ParagraphStyle(
    "Body",
    fontName="Helvetica",
    fontSize=9.5,
    leading=15,
    textColor=TEXT,
    spaceAfter=5,
)


BULLET = ParagraphStyle(
    "Bullet",
    fontName="Helvetica",
    fontSize=9.5,
    leading=15,
    textColor=TEXT,
    leftIndent=13,
    firstLineIndent=-8,
    spaceAfter=5,
)


SMALL = ParagraphStyle(
    "Small",
    fontName="Helvetica",
    fontSize=8,
    leading=11,
    textColor=MUTED,
)


STAT_NUMBER = ParagraphStyle(
    "StatNumber",
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=21,
    textColor=NAVY,
    alignment=TA_CENTER,
)


STAT_LABEL = ParagraphStyle(
    "StatLabel",
    fontName="Helvetica",
    fontSize=7.5,
    leading=10,
    textColor=MUTED,
    alignment=TA_CENTER,
)


ACTION_TEXT = ParagraphStyle(
    "ActionText",
    fontName="Helvetica",
    fontSize=9,
    leading=14,
    textColor=TEXT,
)


ACTION_STATUS = ParagraphStyle(
    "ActionStatus",
    fontName="Helvetica-Bold",
    fontSize=7.5,
    leading=10,
    textColor=ORANGE,
    alignment=TA_CENTER,
)


# ============================================================
# HELPERS
# ============================================================

def escape_text(text):

    return html.escape(text)


def clean_item(text):

    return text.lstrip(
        "-*• "
    ).strip()


def parse_analysis(text):
    """
    Parse the AI analysis into the five expected sections.

    Supports headings such as:
    **1. MEETING SUMMARY**
    1. MEETING SUMMARY
    ### 1. MEETING SUMMARY
    """

    section_names = [
        "1. MEETING SUMMARY",
        "2. KEY POINTS",
        "3. DECISIONS",
        "4. ACTION ITEMS",
        "5. IMPORTANT DETAILS",
    ]

    sections = {
        name: []
        for name in section_names
    }

    current_section = None

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # Remove Markdown formatting
        clean_line = line.replace("**", "").strip()

        # Remove Markdown heading markers
        clean_line = clean_line.lstrip("#").strip()

        # Check whether this line is a section heading
        found_section = None

        for section_name in section_names:

            if clean_line.upper() == section_name.upper():

                found_section = section_name
                break

        if found_section:

            current_section = found_section
            continue

        # Add content to the current section
        if current_section:

            # Remove Markdown bold from individual content
            clean_content = line.replace("**", "").strip()

            if clean_content:
                sections[current_section].append(
                    clean_content
                )

    return sections

# ============================================================
# FOOTER
# ============================================================

def draw_footer(
    canvas,
    document
):

    canvas.saveState()

    width, height = A4

    canvas.setStrokeColor(
        BORDER
    )

    canvas.setLineWidth(
        0.5
    )

    canvas.line(
        2 * cm,
        1.35 * cm,
        width - 2 * cm,
        1.35 * cm,
    )

    canvas.setFont(
        "Helvetica",
        7.5
    )

    canvas.setFillColor(
        MUTED
    )

    canvas.drawString(
        2 * cm,
        0.85 * cm,
        "Meet-AI  •  Meeting Summary",
    )

    canvas.drawRightString(
        width - 2 * cm,
        0.85 * cm,
        f"{document.page}",
    )

    canvas.restoreState()


# ============================================================
# COVER
# ============================================================

def create_cover():

    elements = []

    elements.append(
        Spacer(
            1,
            1 * cm
        )
    )

    hero_content = [

        Paragraph(
            "MEET-AI",
            COVER_BRAND,
        ),

        Spacer(
            1,
            0.3 * cm
        ),

        Paragraph(
            "Meeting<br/>Summary",
            COVER_TITLE,
        ),

        Spacer(
            1,
            0.35 * cm
        ),

        Paragraph(
            "A clear and structured recap of what was "
            "discussed, decided and agreed during the meeting.",
            COVER_SUBTITLE,
        ),
    ]

    hero = Table(
        [[hero_content]],
        colWidths=[
            16.8 * cm
        ],
    )

    hero.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    NAVY,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    1.2 * cm,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    1 * cm,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    1 * cm,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    1 * cm,
                ),
            ]
        )
    )

    elements.append(
        hero
    )

    elements.append(
        Spacer(
            1,
            0.65 * cm
        )
    )

    elements.append(
        Paragraph(
            "Meeting at a glance",
            SECTION_TITLE,
        )
    )

    elements.append(
        Paragraph(
            "The essentials, in one place.",
            PAGE_SUBTITLE,
        )
    )

    elements.append(
        Spacer(
            1,
            0.25 * cm
        )
    )

    stats = Table(
        [
            [
                [
                    Paragraph(
                        "01",
                        STAT_NUMBER,
                    ),
                    Paragraph(
                        "MEETING SUMMARY",
                        STAT_LABEL,
                    ),
                ],

                [
                    Paragraph(
                        "05",
                        STAT_NUMBER,
                    ),
                    Paragraph(
                        "KEY SECTIONS",
                        STAT_LABEL,
                    ),
                ],

                [
                    Paragraph(
                        "AI",
                        STAT_NUMBER,
                    ),
                    Paragraph(
                        "ASSISTED ANALYSIS",
                        STAT_LABEL,
                    ),
                ],
            ]
        ],
        colWidths=[
            5.6 * cm,
            5.6 * cm,
            5.6 * cm,
        ],
    )

    stats.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    WHITE,
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    BORDER,
                ),

                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    BORDER,
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0.55 * cm,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0.55 * cm,
                ),
            ]
        )
    )

    elements.append(
        stats
    )

    elements.append(
        Spacer(
            1,
            0.8 * cm
        )
    )

    intro = Table(
        [
            [
                Paragraph(
                    "<b>What you'll find inside</b><br/><br/>"
                    "A concise overview of the conversation, "
                    "the main ideas that came up, the decisions "
                    "that were made and the next steps to follow.",
                    BODY,
                )
            ]
        ],
        colWidths=[
            16.8 * cm
        ],
    )

    intro.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    BLUE_SOFT,
                ),

                (
                    "LINEBEFORE",
                    (0, 0),
                    (0, -1),
                    4,
                    BLUE,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0.6 * cm,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0.6 * cm,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0.45 * cm,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0.45 * cm,
                ),
            ]
        )
    )

    elements.append(
        intro
    )

    elements.append(
        Spacer(
            1,
            0.6 * cm
        )
    )

    elements.append(
        Paragraph(
            "Prepared by Meet-AI",
            SMALL,
        )
    )

    elements.append(
        PageBreak()
    )

    return elements


# ============================================================
# CARD
# ============================================================

def create_card(
    icon,
    title,
    content,
    background,
    accent,
):

    card_content = []

    card_content.append(
        Paragraph(
            f"{icon}  {title}",
            CARD_TITLE,
        )
    )

    for line in content:

        line = line.strip()

        if not line:
            continue

        if (
            line.startswith("-")
            or line.startswith("*")
            or line.startswith("•")
        ):

            card_content.append(
                Paragraph(
                    f"• {escape_text(clean_item(line))}",
                    BULLET,
                )
            )

        else:

            card_content.append(
                Paragraph(
                    escape_text(line),
                    BODY,
                )
            )

    card = Table(
        [[card_content]],
        colWidths=[
            16.8 * cm
        ],
    )

    card.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    background,
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    BORDER,
                ),

                (
                    "LINEBEFORE",
                    (0, 0),
                    (0, -1),
                    4,
                    accent,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0.6 * cm,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0.6 * cm,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0.45 * cm,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0.35 * cm,
                ),
            ]
        )
    )

    return card


# ============================================================
# ACTION ITEMS
# ============================================================

def create_action_items(
    actions
):

    rows = []

    for index, action in enumerate(
        actions,
        start=1
    ):

        action = clean_item(
            action
        )

        rows.append(
            [
                Paragraph(
                    f"<b>{index:02d}</b>",
                    ParagraphStyle(
                        f"Num{index}",
                        fontName="Helvetica-Bold",
                        fontSize=10,
                        textColor=BLUE,
                        alignment=TA_CENTER,
                    ),
                ),

                Paragraph(
                    escape_text(action),
                    ACTION_TEXT,
                ),

                Paragraph(
                    "NEXT STEP",
                    ACTION_STATUS,
                ),
            ]
        )

    if not rows:

        rows.append(
            [
                Paragraph(
                    "—",
                    BODY,
                ),

                Paragraph(
                    "No action items were identified.",
                    BODY,
                ),

                Paragraph(
                    "",
                    BODY,
                ),
            ]
        )

    table = Table(
        rows,
        colWidths=[
            1.1 * cm,
            11.9 * cm,
            3.8 * cm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    WHITE,
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    BORDER,
                ),

                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, -2),
                    0.5,
                    BORDER,
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )

    return table


# ============================================================
# CREATE REPORT
# ============================================================

def create_pdf_report(
    meeting_dir
):

    meeting_dir = Path(meeting_dir)

    analysis_file = (
        meeting_dir
        / "analysis"
        / "analysis.txt"
    )

    output_directory = (
        meeting_dir
        / "reports"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory
        / "meeting_report.pdf"
    )

    if not analysis_file.exists():

        raise FileNotFoundError(
            f"Analysis not found: "
            f"{analysis_file}"
        )

    analysis = analysis_file.read_text(
        encoding="utf-8"
    )

    if not analysis.strip():

        raise ValueError(
            "Analysis file is empty."
        )

    sections = parse_analysis(
        analysis
    )

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.7 * cm,
        title="Meeting Summary",
        author="Meet-AI",
    )

    story = []

    # --------------------------------------------------------
    # COVER
    # --------------------------------------------------------

    story.extend(
        create_cover()
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Meeting Summary",
            PAGE_TITLE,
        )
    )

    story.append(
        Paragraph(
            "Here is the important information from the meeting, "
            "organized so you can quickly understand what happened "
            "and what comes next.",
            PAGE_SUBTITLE,
        )
    )

    story.append(
        Spacer(
            1,
            0.45 * cm
        )
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary = sections.get(
        "1. MEETING SUMMARY",
        []
    )

    if not summary:
        summary = [
            "No meeting summary was identified."
        ]

    story.append(
        Paragraph(
            "The big picture",
            SECTION_TITLE,
        )
    )

    story.append(
        create_card(
            "●",
            "MEETING SUMMARY",
            summary,
            BLUE_SOFT,
            BLUE,
        )
    )

    story.append(
        Spacer(
            1,
            0.45 * cm
        )
    )

    # --------------------------------------------------------
    # KEY POINTS
    # --------------------------------------------------------

    key_points = sections.get(
        "2. KEY POINTS",
        []
    )

    if not key_points:
        key_points = [
            "No key points were identified."
        ]

    story.append(
        Paragraph(
            "What stood out",
            SECTION_TITLE,
        )
    )

    story.append(
        create_card(
            "◆",
            "KEY POINTS",
            key_points,
            PURPLE_SOFT,
            PURPLE,
        )
    )

    story.append(
        Spacer(
            1,
            0.45 * cm
        )
    )

    # --------------------------------------------------------
    # DECISIONS
    # --------------------------------------------------------

    decisions = sections.get(
        "3. DECISIONS",
        []
    )

    if not decisions:
        decisions = [
            "None identified."
        ]

    story.append(
        Paragraph(
            "What was decided",
            SECTION_TITLE,
        )
    )

    story.append(
        create_card(
            "✓",
            "DECISIONS",
            decisions,
            GREEN_SOFT,
            GREEN,
        )
    )

    story.append(
        Spacer(
            1,
            0.45 * cm
        )
    )

    # --------------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------------

    actions = sections.get(
        "4. ACTION ITEMS",
        []
    )

    story.append(
        Paragraph(
            "What happens next",
            SECTION_TITLE,
        )
    )

    story.append(
        Paragraph(
            "The follow-up items identified during the meeting.",
            PAGE_SUBTITLE,
        )
    )

    story.append(
        Spacer(
            1,
            0.2 * cm
        )
    )

    story.append(
        create_action_items(
            actions
        )
    )

    story.append(
        Spacer(
            1,
            0.5 * cm
        )
    )

    # --------------------------------------------------------
    # IMPORTANT DETAILS
    # --------------------------------------------------------

    details = sections.get(
        "5. IMPORTANT DETAILS",
        []
    )

    if not details:
        details = [
            "None identified."
        ]

    story.append(
        Paragraph(
            "Worth remembering",
            SECTION_TITLE,
        )
    )

    story.append(
        create_card(
            "i",
            "IMPORTANT DETAILS",
            details,
            ORANGE_SOFT,
            ORANGE,
        )
    )

    # --------------------------------------------------------
    # FINAL NOTE
    # --------------------------------------------------------

    story.append(
        Spacer(
            1,
            0.6 * cm
        )
    )

    final_note = Table(
        [
            [
                Paragraph(
                    "<b>Meeting recap complete.</b><br/>"
                    "This summary was prepared from the available "
                    "meeting transcript. It focuses on information "
                    "that was actually discussed and avoids adding "
                    "details that were not present.",
                    BODY,
                )
            ]
        ],
        colWidths=[
            16.8 * cm
        ],
    )

    final_note.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F1F5F9"),
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    BORDER,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0.55 * cm,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0.55 * cm,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0.4 * cm,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0.4 * cm,
                ),
            ]
        )
    )

    story.append(
        final_note
    )

    # --------------------------------------------------------
    # BUILD
    # --------------------------------------------------------

    document.build(
        story,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer,
    )

    return output_file


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("================================")
    print("       MEETING REPORT")
    print("================================")
    print()

    # Temporary test folder.
    # Replace this with the folder created
    # by meeting_manager.py.

    meeting_dir = Path(
        "meetings/2026-10-07_11-30-25"
    )

    try:

        report = create_pdf_report(
            meeting_dir
        )

        print(
            "✅ PDF generated successfully!"
        )

        print(
            f"📄 {report}"
        )

    except Exception as e:

        print(
            "❌ PDF generation failed:"
        )

        print(e)