from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def clean_text(text):
    # Remove markdown symbols
    text = text.replace("**", "")
    text = text.replace("* ", "• ")
    return text

def create_pdf(text, filename="output.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    text = clean_text(text)

    content = []

    paragraphs = text.split("\n")

    for para in paragraphs:
        if para.strip():
            content.append(Paragraph(para, styles["Normal"]))
            content.append(Spacer(1, 10))

    doc.build(content)