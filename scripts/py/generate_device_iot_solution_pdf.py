from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "商业化" / "设备信息采集与业务系统对接解决方案.md"
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUTS = [
    OUTPUT_DIR / "设备信息采集与业务系统对接解决方案.pdf",
    OUTPUT_DIR / "设备信息采集与业务系统对接解决方案-高对比深色版.pdf",
    OUTPUT_DIR / "device-iot-solution-high-contrast.pdf",
]
FONT_REGULAR = Path("C:/Windows/Fonts/simhei.ttf")


def register_fonts() -> str:
    if FONT_REGULAR.exists():
        pdfmetrics.registerFont(TTFont("SimHei", str(FONT_REGULAR)))
        return "SimHei"
    fallback = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
    if fallback.exists():
        pdfmetrics.registerFont(TTFont("NotoSansSC", str(fallback)))
        return "NotoSansSC"
    return "Helvetica"


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_markdown(text: str) -> str:
    text = xml_escape(text.strip())
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        if not is_table_separator(lines[i]):
            rows.append([inline_markdown(cell.strip()) for cell in lines[i].strip().strip("|").split("|")])
        i += 1
    return rows, i


def build_styles(font_name: str) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCN",
            parent=base["Title"],
            fontName=font_name,
            fontSize=22,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#000000"),
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCN",
            parent=base["Normal"],
            fontName=font_name,
            fontSize=10,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111111"),
            spaceAfter=16,
        ),
        "h2": ParagraphStyle(
            "H2CN",
            parent=base["Heading2"],
            fontName=font_name,
            fontSize=14,
            leading=20,
            textColor=colors.HexColor("#000000"),
            spaceBefore=10,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "H3CN",
            parent=base["Heading3"],
            fontName=font_name,
            fontSize=11.5,
            leading=17,
            textColor=colors.HexColor("#003A5D"),
            spaceBefore=7,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "BodyCN",
            parent=base["BodyText"],
            fontName=font_name,
            fontSize=9.8,
            leading=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#000000"),
            spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "BulletCN",
            parent=base["BodyText"],
            fontName=font_name,
            fontSize=9.6,
            leading=14.2,
            leftIndent=11,
            firstLineIndent=-7,
            textColor=colors.HexColor("#000000"),
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "SmallCN",
            parent=base["BodyText"],
            fontName=font_name,
            fontSize=8.6,
            leading=12,
            textColor=colors.HexColor("#000000"),
        ),
    }


def make_table(rows: list[list[str]], styles: dict[str, ParagraphStyle]) -> Table:
    col_count = max(len(row) for row in rows)
    normalized = [row + [""] * (col_count - len(row)) for row in rows]
    data = [[Paragraph(cell, styles["small"]) for cell in row] for row in normalized]
    width = 170 * mm
    col_widths = [width / col_count] * col_count
    table = Table(data, colWidths=col_widths, hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2EAF1")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#000000")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C6D1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5DD"))
    canvas.setLineWidth(0.4)
    canvas.line(20 * mm, 282 * mm, 190 * mm, 282 * mm)
    canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    canvas.setFillColor(colors.HexColor("#000000"))
    canvas.setFont(doc.font_name, 7.5)
    canvas.drawString(20 * mm, 286 * mm, "设备信息采集与业务系统对接解决方案")
    canvas.drawRightString(190 * mm, 10 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def build_story(markdown: str, styles: dict[str, ParagraphStyle]) -> list:
    lines = markdown.splitlines()
    story: list = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line.startswith("# "):
            story.append(Spacer(1, 30 * mm))
            story.append(Paragraph(inline_markdown(line[2:]), styles["title"]))
            i += 1
            meta: list[str] = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("## "):
                meta.append(lines[i].strip())
                i += 1
            if meta:
                story.append(Paragraph("<br/>".join(inline_markdown(item) for item in meta), styles["subtitle"]))
            story.append(Spacer(1, 12 * mm))
            story.append(Paragraph("面向制造企业设备全生命周期、维修保养巡检、IoT 健康监测与生产计划联动", styles["subtitle"]))
            cover_rows = [
                ["可行性结论", "项目可做，建议分三阶段交付，先管理闭环，再设备采集，最后生产计划联动。"],
                ["一期重点", "设备台账、扫码报修、维修工单、保养计划、移动巡检、基础报表。"],
                ["后续扩展", "OPC UA/MQTT 接入、健康评分、预警、ERP/PLM/MES 数据同步。"],
            ]
            story.append(Spacer(1, 8 * mm))
            story.append(make_table(cover_rows, styles))
            story.append(PageBreak())
            continue
        if line.startswith("## "):
            story.append(Paragraph(inline_markdown(line[3:]), styles["h2"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline_markdown(line[4:]), styles["h3"]))
        elif line.startswith("|"):
            rows, i = parse_table(lines, i)
            if rows:
                story.append(make_table(rows, styles))
                story.append(Spacer(1, 5))
            continue
        elif line.startswith("- "):
            story.append(Paragraph("- " + inline_markdown(line[2:]), styles["bullet"]))
        elif re.match(r"^\d+\.\s+", line):
            story.append(Paragraph(inline_markdown(line), styles["bullet"]))
        else:
            story.append(Paragraph(inline_markdown(line), styles["body"]))
        i += 1
    return story


def build_pdf(output: Path, font_name: str, styles: dict[str, ParagraphStyle], markdown: str) -> None:
    story = build_story(markdown, styles)
    doc = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    doc.font_name = font_name
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="solution", frames=[frame], onPage=header_footer)])
    doc.build(story)
    print(output)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    font_name = register_fonts()
    styles = build_styles(font_name)
    markdown = SOURCE.read_text(encoding="utf-8")
    for output in OUTPUTS:
        build_pdf(output, font_name, styles, markdown)


if __name__ == "__main__":
    main()
