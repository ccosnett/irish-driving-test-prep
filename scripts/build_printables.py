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
LADYBIRD_MD = ROOT / "LADYBIRD_47_CLEAN.md"
PRACTICAL_TSV = ROOT / "ladybird_47_clean.tsv"
EASY_TSV = ROOT / "irish_driving_test_easy_mode_core30.tsv"
WALL_MD = ROOT / "WALL_SHEET.md"
PRINTABLES_DIR = ROOT / "printables"
WALL_PDF = PRINTABLES_DIR / "irish-driving-test-wall-sheet.pdf"
PRACTICAL_PDF = PRINTABLES_DIR / "irish-driving-test-ladybird-47.pdf"

START_MARKER = "<!-- ALL_QUESTIONS_START -->"
END_MARKER = "<!-- ALL_QUESTIONS_END -->"

TOPIC_ORDER = [
    "overtaking",
    "markings",
    "junctions",
    "right_of_way",
    "lights",
    "crossings",
    "speed_limits",
    "technical_checks",
    "bus_lanes",
    "parking",
    "positioning",
    "dual_carriageway",
    "motorway",
    "awareness",
    "manoeuvres",
    "safe_driving",
    "vehicle_control",
    "safety_rules",
    "signals",
]

TOPIC_LABELS = {
    "overtaking": "Overtaking",
    "markings": "Road Markings",
    "junctions": "Junctions",
    "right_of_way": "Right Of Way",
    "lights": "Traffic Lights And Visibility",
    "crossings": "Crossings",
    "speed_limits": "Speed Limits",
    "technical_checks": "Technical Checks",
    "bus_lanes": "Bus Lanes",
    "parking": "Parking",
    "positioning": "Positioning",
    "dual_carriageway": "Dual Carriageway",
    "motorway": "Motorway",
    "awareness": "Country Roads And Awareness",
    "manoeuvres": "Manoeuvres",
    "safe_driving": "Safe Driving",
    "vehicle_control": "Vehicle Control",
    "safety_rules": "Safety Rules",
    "signals": "Signals",
}


def parse_tsv(path: Path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 3:
                continue
            question, answer, topic = row[:3]
            rows.append({"question": question, "answer": answer, "topic": topic})
    return rows


def parse_easy_tsv(path: Path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 3:
                continue
            question, answer, tags = row[:3]
            rows.append({"question": question, "answer": answer, "tags": tags.split()})
    return rows


def parse_easy_answer(answer):
    text = answer.replace("<br>", " ").strip()
    match = re.match(r"Memory cue:\s*(.*?)\.\s*Test answer:\s*(.*)", text)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", text


def build_ladybird_markdown(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["topic"]].append(row)

    lines = []
    lines.append("This file is generated from `ladybird_47_clean.tsv`.")
    lines.append("")

    count = 1
    for topic in TOPIC_ORDER:
        items = grouped.get(topic)
        if not items:
            continue
        lines.append(f"### {TOPIC_LABELS.get(topic, topic.replace('_', ' ').title())}")
        lines.append("")
        for row in items:
            lines.append(f"{count}. **{row['question']}**")
            lines.append(f"   Answer: {row['answer']}")
            count += 1
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def update_marker_file(path: Path, body: str):
    text = path.read_text(encoding="utf-8")
    replacement = f"{START_MARKER}\n\n{body}\n{END_MARKER}"
    updated = re.sub(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        replacement,
        text,
        flags=re.S,
    )
    path.write_text(updated, encoding="utf-8")


def build_wall_sheet_markdown(rows):
    lines = []
    lines.append("# Irish Driving Test Wall Sheet")
    lines.append("")
    lines.append("Fast recall sheet built from `irish_driving_test_easy_mode_core30.tsv`.")
    lines.append("")
    lines.append("Use the memory cue first. Then say the short answer out loud.")
    lines.append("")

    for row in rows:
        memory, test_answer = parse_easy_answer(row["answer"])
        lines.append(f"- **{row['question']}**")
        lines.append(f"  Memory cue: {memory}")
        lines.append(f"  Test answer: {test_answer}")
    lines.append("")
    return "\n".join(lines)


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


def build_practical_pdf(rows):
    PRINTABLES_DIR.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(
        str(PRACTICAL_PDF),
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
        grouped[row["topic"]].append(row)

    story = [
        Paragraph("Ladybird 47 Clean Practical Questions", title),
        Spacer(1, 3 * mm),
        Paragraph("Cleaned practical-study version based on the Ladybird page.", subtitle),
        Spacer(1, 6 * mm),
    ]

    count = 1
    for topic in TOPIC_ORDER:
        items = grouped.get(topic)
        if not items:
            continue
        story.append(Paragraph(TOPIC_LABELS.get(topic, topic.replace("_", " ").title()), heading))
        for row in items:
            story.append(Paragraph(f"<b>{count}. Q:</b> {row['question']}<br/><b>A:</b> {row['answer']}", qa))
            count += 1

    doc.build(story)


def main():
    practical_rows = parse_tsv(PRACTICAL_TSV)
    easy_rows = parse_easy_tsv(EASY_TSV)

    appendix = build_ladybird_markdown(practical_rows)
    update_marker_file(README_PATH, appendix)
    update_marker_file(LADYBIRD_MD, appendix)

    wall_md = build_wall_sheet_markdown(easy_rows)
    WALL_MD.write_text(wall_md, encoding="utf-8")

    build_wall_pdf(easy_rows)
    build_practical_pdf(practical_rows)


if __name__ == "__main__":
    main()
