from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

def create_interview_kit_pdf(candidate_data: dict):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2)
    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph("Interview Kit", styles['h1']))
    story.append(Spacer(1, 0.2*inch))

    # Candidate Info
    story.append(Paragraph(f"<b>Candidate:</b> {candidate_data.get('candidate_email', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>Fit Score:</b> {candidate_data.get('fit_score', 'N/A')}%", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Matched Skills
    story.append(Paragraph("Matched Skills:", styles['h3']))
    for skill in candidate_data.get('matched_skills', []):
        story.append(Paragraph(f"• {skill}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Missing Skills
    story.append(Paragraph("Skills to Assess:", styles['h3']))
    for skill in candidate_data.get('missing_skills', []):
        story.append(Paragraph(f"• {skill}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # AI-Generated Questions
    story.append(Paragraph("Suggested Interview Questions:", styles['h3']))
    for i, q in enumerate(candidate_data.get('questions', []), 1):
        question_text = f"<b>{i}. {q.get('question')}</b> ({q.get('difficulty')} / {q.get('category')})"
        story.append(Paragraph(question_text, styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

    doc.build(story)
    buffer.seek(0)
    return buffer