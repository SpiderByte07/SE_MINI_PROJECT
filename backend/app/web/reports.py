"""TTG-16 schedule exports as printable PDF and Excel workbook."""
from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .schedule import _ensure_schedule
from .security import current_user

router = APIRouter(prefix="/api/export", tags=["exports"])
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def _select(view, value):
    key = {"section": "section_id", "faculty": "faculty_id", "room": "room_id"}.get(view)
    if key is None:
        raise HTTPException(422, detail="view must be section, faculty or room.")
    return [e for e in _ensure_schedule() if value is None or e[key] == value]


def _rows(entries):
    return [["Day", "Period", "Course", "Section", "Faculty", "Room", "Length"]] + [
        [DAY_NAMES[e["day"]], e["period"] + 1, e["course_code"], e["section_id"],
         e["faculty_id"], e["room_id"], e["length"]] for e in sorted(entries, key=lambda x: (x["day"], x["period"]))]


@router.get("/pdf")
def export_pdf(view: str = "section", value: str | None = None, user=Depends(current_user)):
    output = BytesIO()
    entries = _select(view, value)
    doc = SimpleDocTemplate(output, pagesize=landscape(A4), title="College Timetable")
    styles = getSampleStyleSheet()
    title = Paragraph(f"College Timetable - {view.title()}: {value or 'All'}", styles["Title"])
    table = Table(_rows(entries), repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24345b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    doc.build([title, Spacer(1, 14), table])
    output.seek(0)
    return StreamingResponse(output, media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=timetable.pdf"})


@router.get("/xlsx")
def export_xlsx(view: str = "section", value: str | None = None, user=Depends(current_user)):
    book = Workbook()
    sheet = book.active
    sheet.title = "Timetable"
    for row in _rows(_select(view, value)):
        sheet.append(row)
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="24345B")
        cell.alignment = Alignment(horizontal="center")
    for column in sheet.columns:
        letter = column[0].column_letter
        sheet.column_dimensions[letter].width = min(max(max(len(str(c.value or "")) for c in column) + 2, 12), 32)
    sheet.freeze_panes = "A2"
    output = BytesIO()
    book.save(output)
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=timetable.xlsx"})
