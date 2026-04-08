"""
exporter.py
-----------
Optional expansion: PDF Export.
Takes the revamped resume text and renders it as a downloadable PDF
using the fpdf2 library.
"""

from fpdf import FPDF


class ResumePDF(FPDF):
    """
    Custom FPDF subclass with a styled header and footer.
    """

    def header(self):
        """Render a slim accent bar at the top of each page."""
        self.set_fill_color(30, 80, 160)   # Deep blue accent
        self.rect(0, 0, 210, 4, style="F")
        self.ln(6)

    def footer(self):
        """Render a page number at the bottom of each page."""
        self.set_y(-15)
        self.set_font("Helvetica", style="I", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def save_as_pdf(revamped_text: str) -> bytes:
    """
    Convert a plain text resume into a formatted PDF document.

    Args:
        revamped_text: The AI-rewritten resume as a plain string.

    Returns:
        The PDF file as a bytes object, ready for Streamlit's download_button.

    Raises:
        ValueError: If the input text is empty.
    """
    if not revamped_text.strip():
        raise ValueError("Cannot export an empty resume. Please revamp the resume first.")

    pdf = ResumePDF()
    pdf.set_margins(left=20, top=15, right=20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Process and render each line of the resume text
    for line in revamped_text.split("\n"):
        stripped = line.strip()

        if not stripped:
            # Blank line — add vertical spacing
            pdf.ln(3)

        elif stripped.startswith("# "):
            # H1-style heading (candidate name or main title)
            pdf.set_font("Helvetica", style="B", size=16)
            pdf.set_text_color(30, 80, 160)
            pdf.multi_cell(0, 8, stripped[2:].strip())
            pdf.ln(1)

        elif stripped.startswith("## "):
            # H2-style section heading (Experience, Education, Skills, etc.)
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.set_text_color(30, 80, 160)
            pdf.multi_cell(0, 7, stripped[3:].strip())
            # Underline effect via a thin line
            pdf.set_draw_color(30, 80, 160)
            pdf.set_line_width(0.3)
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.line(20, y, 190, y)
            pdf.ln(2)

        elif stripped.startswith("**") and stripped.endswith("**"):
            # Bold inline text (job titles, company names)
            pdf.set_font("Helvetica", style="B", size=11)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 6, stripped.strip("*").strip())

        elif stripped.startswith("- ") or stripped.startswith("• "):
            # Bullet point
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(60, 60, 60)
            bullet_text = stripped[2:].strip()
            pdf.set_x(25)
            pdf.cell(5, 6, "•")
            pdf.set_x(30)
            pdf.multi_cell(0, 6, bullet_text)

        else:
            # Regular body text
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 6, stripped)

    # Return PDF as bytes (latin-1 encoding required by fpdf2)
    return bytes(pdf.output())
