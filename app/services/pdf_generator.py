from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def create_interview_kit_pdf(kit_data: dict):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, rightMargin=inch / 2, leftMargin=inch / 2, topMargin=inch / 2,
                            bottomMargin=inch / 2)
    styles = getSampleStyleSheet()

    story = []
    analysis = kit_data.get("analysis", {})

    # Title and basic info
    story.append(Paragraph("Interview Kit", styles['h1']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"<b>Candidate:</b> {kit_data.get('candidate_email', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"<b>AI Fit Score:</b> {analysis.get('fit_score_percent', 'N/A')}%", styles['Normal']))
    story.append(Paragraph(f"<b>AI Verdict:</b> {analysis.get('verdict', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Strengths
    story.append(Paragraph("Key Strengths (AI Analysis):", styles['h3']))
    for strength in analysis.get('strengths', []):
        story.append(Paragraph(f"• {strength}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Weaknesses
    story.append(Paragraph("Areas to Probe (AI Analysis):", styles['h3']))
    for weakness in analysis.get('weaknesses', []):
        story.append(Paragraph(f"• {weakness}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Suggested Questions
    story.append(Paragraph("Suggested Interview Questions:", styles['h3']))
    for i, q in enumerate(kit_data.get('questions', []), 1):
        question_text = f"<b>{i}. {q.get('question')}</b> ({q.get('difficulty')} / {q.get('category')})"
        story.append(Paragraph(question_text, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    buffer.seek(0)
    return buffer