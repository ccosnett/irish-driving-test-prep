#!/usr/bin/env python3
import csv
import math
import re
from collections import defaultdict
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
SAFE_TSV = ROOT / "irish_driving_test_2026_safe_anki.tsv"
EASY_TSV = ROOT / "irish_driving_test_easy_mode_core30.tsv"
WALL_MD = ROOT / "WALL_SHEET.md"
PRINTABLES_DIR = ROOT / "printables"
WALL_PDF = PRINTABLES_DIR / "irish-driving-test-wall-sheet.pdf"
FULL_PDF = PRINTABLES_DIR / "irish-driving-test-all-questions.pdf"

START_MARKER = "<!-- ALL_QUESTIONS_START -->"
END_MARKER = "<!-- ALL_QUESTIONS_END -->"

TOPIC_ORDER = [
    "speed_limits",
    "right_of_way",
    "junctions",
    "lights",
    "crossings",
    "markings",
    "parking",
    "signs",
    "overtaking",
    "motorway",
    "safe_driving",
    "technical_checks",
    "secondary_controls",
    "learner_rules",
    "safety_rules",
    "bus_lanes",
    "positioning",
    "manoeuvres",
    "dual_carriageway",
    "vehicle_control",
    "vehicle",
    "emergency",
    "awareness",
]

TOPIC_LABELS = {
    "speed_limits": "Speed Limits",
    "right_of_way": "Right Of Way",
    "junctions": "Junctions",
    "lights": "Traffic Lights",
    "crossings": "Crossings",
    "markings": "Road Markings",
    "parking": "Parking",
    "signs": "Signs",
    "overtaking": "Overtaking",
    "motorway": "Motorway",
    "safe_driving": "Safe Driving",
    "technical_checks": "Technical Checks",
    "secondary_controls": "Secondary Controls",
    "learner_rules": "Learner Rules",
    "safety_rules": "Safety Rules",
    "bus_lanes": "Bus Lanes",
    "positioning": "Positioning",
    "manoeuvres": "Manoeuvres",
    "dual_carriageway": "Dual Carriageway",
    "vehicle_control": "Vehicle Control",
    "vehicle": "Vehicle",
    "emergency": "Emergency",
    "awareness": "Awareness",
}

SKIP_TAGS = {
    "official_core",
    "stephen_reviewed",
    "corrected",
    "current_2026",
    "easy_mode",
    "core30",
    "numbers",
    "web_image",
    "web_remote",
    "practical_test",
}


def parse_tsv(path: Path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 3:
                continue
            question, answer, tags = row[:3]
            rows.append({"question": question, "answer": answer, "tags": tags.split()})
    return rows


def topic_for(tags):
    for topic in TOPIC_ORDER:
        if topic in tags:
            return topic
    for tag in tags:
        if tag not in SKIP_TAGS:
            return tag
    return "misc"


def clean_answer(text):
    return text.replace("<br>", " ").strip()


def parse_easy_answer(answer):
    text = clean_answer(answer)
    match = re.match(r"Memory cue:\s*(.*?)\.\s*Test answer:\s*(.*)", text)
    if match:
        memory = match.group(1).strip()
        test_answer = match.group(2).strip()
        return memory, test_answer
    return "", text


def build_all_questions_markdown(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[topic_for(row["tags"])].append(row)

    lines = []
    lines.append("Generated from `irish_driving_test_2026_safe_anki.tsv`.")
    lines.append("")
    lines.append("This is the full cleaned 2026-safe question set grouped by topic.")
    lines.append("")

    for topic in TOPIC_ORDER:
        items = grouped.get(topic)
        if not items:
            continue
        lines.append(f"### {TOPIC_LABELS.get(topic, topic.title())}")
        lines.append("")
        for row in items:
            lines.append(f"- **{row['question']}**")
            lines.append(f"  Answer: {clean_answer(row['answer'])}")
        lines.append("")

    extras = [k for k in grouped.keys() if k not in TOPIC_ORDER]
    for topic in sorted(extras):
        items = grouped[topic]
        lines.append(f"### {TOPIC_LABELS.get(topic, topic.replace('_', ' ').title())}")
        lines.append("")
        for row in items:
            lines.append(f"- **{row['question']}**")
            lines.append(f"  Answer: {clean_answer(row['answer'])}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def update_readme(all_questions_md):
    readme = README_PATH.read_text(encoding="utf-8")
    replacement = f"{START_MARKER}\n\n{all_questions_md}\n{END_MARKER}"
    updated = re.sub(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        replacement,
        readme,
        flags=re.S,
    )
    README_PATH.write_text(updated, encoding="utf-8")


def build_wall_sheet_markdown(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[topic_for(row["tags"])].append(row)

    lines = []
    lines.append("# Irish Driving Test Wall Sheet")
    lines.append("")
    lines.append("Fast recall sheet built from `irish_driving_test_easy_mode_core30.tsv`.")
    lines.append("")
    lines.append("Use the memory cue first, then say the short test answer out loud.")
    lines.append("")

    for topic in TOPIC_ORDER:
        items = grouped.get(topic)
        if not items:
            continue
        lines.append(f"## {TOPIC_LABELS.get(topic, topic.title())}")
        lines.append("")
        for row in items:
            memory, test_answer = parse_easy_answer(row["answer"])
            lines.append(f"- **{row['question']}**")
            lines.append(f"  Memory cue: {memory}")
            lines.append(f"  Test answer: {test_answer}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_wall_pdf(rows):
    PRINTABLES_DIR.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(
        str(WALL_PDF),
        pagesize=landscape(A4),
        topMargin=10 * mm,
        bottomMargin=10 * mm,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle("WallTitle", parent=styles["Title"], alignment=TA_CENTER, fontSize=20, leading=24)
    subtitle = ParagraphStyle("WallSubtitle", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10, leading=12)
    card = ParagraphStyle("Card", parent=styles["BodyText"], fontSize=10, leading=12)

    story = [
        Paragraph("Irish Driving Test Wall Sheet", title),
        Spacer(1, 4 * mm),
        Paragraph("Memory cue first. Then say the short answer out loud.", subtitle),
        Spacer(1, 6 * mm),
    ]

    cards = []
    for row in rows:
        memory, test_answer = parse_easy_answer(row["answer"])
        cards.append(
            Paragraph(
                f"<b>{row['question']}</b><br/>"
                f"<font color='#666666'>Memory cue:</font> {memory}<br/>"
                f"<font color='#111111'><b>Answer:</b> {test_answer}</font>",
                card,
            )
        )

    columns = 2
    row_count = math.ceil(len(cards) / columns)
    data = []
    for i in range(row_count):
        left = cards[i]
        right_index = i + row_count
        right = cards[right_index] if right_index < len(cards) else ""
        data.append([left, right])

    table = Table(data, colWidths=[133 * mm, 133 * mm], repeatRows=0)
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)
    doc.build(story)


def build_full_pdf(rows):
    PRINTABLES_DIR.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(
        str(FULL_PDF),
        pagesize=A4,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle("FullTitle", parent=styles["Title"], alignment=TA_CENTER, fontSize=18, leading=22)
    subtitle = ParagraphStyle("FullSubtitle", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10, leading=12)
    heading = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=13, leading=16, spaceBefore=6, spaceAfter=4)
    qa = ParagraphStyle("QA", parent=styles["BodyText"], fontSize=10, leading=13, spaceAfter=5)

    grouped = defaultdict(list)
    for row in rows:
        grouped[topic_for(row["tags"])].append(row)

    story = [
        Paragraph("Irish Driving Test Full Question Set", title),
        Spacer(1, 3 * mm),
        Paragraph("Generated from the cleaned 2026-safe deck.", subtitle),
        Spacer(1, 6 * mm),
    ]

    for topic in TOPIC_ORDER:
        items = grouped.get(topic)
        if not items:
            continue
        story.append(Paragraph(TOPIC_LABELS.get(topic, topic.title()), heading))
        for row in items:
            story.append(Paragraph(f"<b>Q:</b> {row['question']}<br/><b>A:</b> {clean_answer(row['answer'])}", qa))

    doc.build(story)


def main():
    safe_rows = parse_tsv(SAFE_TSV)
    easy_rows = parse_tsv(EASY_TSV)

    all_questions_md = build_all_questions_markdown(safe_rows)
    update_readme(all_questions_md)

    wall_md = build_wall_sheet_markdown(easy_rows)
    WALL_MD.write_text(wall_md, encoding="utf-8")

    build_wall_pdf(easy_rows)
    build_full_pdf(safe_rows)


if __name__ == "__main__":
    main()
