from __future__ import annotations

import argparse
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def clean_inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    return text


def table_from_lines(lines: list[str], styles) -> Table:
    rows = []
    for line in lines:
        cells = [clean_inline(cell.strip()) for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells):
            continue
        rows.append([Paragraph(cell, styles["TableCell"]) for cell in cells])
    table = Table(rows, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EEF5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172033")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B8C2D1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def markdown_to_story(markdown: str):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Title2", parent=styles["Title"], fontSize=22, leading=26, spaceAfter=14))
    styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontSize=18, leading=22, spaceBefore=10, spaceAfter=8))
    styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontSize=14, leading=18, spaceBefore=8, spaceAfter=6))
    styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.5, leading=13, spaceAfter=6))
    styles.add(ParagraphStyle(name="Bulletx", parent=styles["BodyText"], fontSize=9.5, leading=13, leftIndent=14, firstLineIndent=-8, spaceAfter=4))
    styles.add(ParagraphStyle(name="TableCell", parent=styles["BodyText"], fontSize=7.5, leading=9))
    story = []
    table_buffer: list[str] = []
    in_code = False

    def flush_table():
        nonlocal table_buffer
        if table_buffer:
            story.append(table_from_lines(table_buffer, styles))
            story.append(Spacer(1, 0.12 * inch))
            table_buffer = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            flush_table()
            in_code = not in_code
            continue
        if in_code:
            if line.strip():
                story.append(Paragraph(clean_inline(line), styles["Bodyx"]))
            continue
        if line.startswith("|") and line.endswith("|"):
            table_buffer.append(line)
            continue
        flush_table()
        if not line.strip():
            story.append(Spacer(1, 0.04 * inch))
        elif line.startswith("# "):
            story.append(Paragraph(clean_inline(line[2:]), styles["Title2"]))
        elif line.startswith("## "):
            story.append(Paragraph(clean_inline(line[3:]), styles["H1x"]))
        elif line.startswith("### "):
            story.append(Paragraph(clean_inline(line[4:]), styles["H2x"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + clean_inline(line[2:]), styles["Bulletx"]))
        elif re.match(r"^\d+\.\s", line):
            story.append(Paragraph(clean_inline(line), styles["Bulletx"]))
        else:
            story.append(Paragraph(clean_inline(line), styles["Bodyx"]))
    flush_table()
    return story


def build_pdf(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )
    story = markdown_to_story(input_path.read_text(encoding="utf-8"))
    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PDF deliverables from project markdown files.")
    parser.add_argument("--only", default=None, help="Optional markdown file path to render.")
    args = parser.parse_args()
    if args.only:
        path = Path(args.only)
        build_pdf(path, Path("reports") / f"{path.stem}.pdf")
        return
    for path in [
        Path("docs/concept_brief.md"),
        Path("docs/labeling_codebook.md"),
        Path("docs/data_source_plan.md"),
        Path("docs/evaluation_plan.md"),
        Path("docs/technical_appendix_outline.md"),
        Path("docs/executive_memo_draft.md"),
    ]:
        build_pdf(path, Path("reports") / f"{path.stem}.pdf")
        print(f"Wrote reports/{path.stem}.pdf")


if __name__ == "__main__":
    main()

