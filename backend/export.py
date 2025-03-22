import base64
import json
import io
import logging
from typing import Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_to_pdf(research_data: Dict[str, Any]) -> str:
    """
    Export research data to PDF format and return as base64 encoded string
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Define custom styles
        styles.add(
            ParagraphStyle(name='Title',
                           fontSize=18,
                           spaceAfter=12,
                           textColor=colors.HexColor('#0A2540')))
        styles.add(
            ParagraphStyle(name='Subtitle',
                           fontSize=14,
                           spaceAfter=8,
                           textColor=colors.HexColor('#00A67E')))
        styles.add(ParagraphStyle(name='Normal', fontSize=10, spaceAfter=6))

        content = []
        content.append(
            Paragraph(
                f"Research Report: {research_data.get('query', 'Unknown')}",
                styles['Title']))
        content.append(Spacer(1, 12))
        content.append(
            Paragraph(f"Date: {research_data.get('timestamp', 'N/A')}",
                      styles['Normal']))
        content.append(Spacer(1, 20))

        for line in research_data.get('response', '').split('\n'):
            if line.startswith('# '):
                content.append(
                    Paragraph(line.replace('# ', ''), styles['Title']))
            elif line.startswith('## '):
                content.append(
                    Paragraph(line.replace('## ', ''), styles['Subtitle']))
            else:
                content.append(Paragraph(line, styles['Normal']))
            content.append(Spacer(1, 6))

        doc.build(content)
        pdf_content = buffer.getvalue()
        buffer.close()

        return base64.b64encode(pdf_content).decode('utf-8')
    except Exception as e:
        logger.error(f"Error exporting to PDF: {e}")
        return ""


def export_to_json(research_data: Dict[str, Any]) -> str:
    """ Export research data to JSON format """
    try:
        return json.dumps(research_data, indent=2)
    except Exception as e:
        logger.error(f"Error exporting to JSON: {e}")
        return "{}"


def export_to_txt(research_data: Dict[str, Any]) -> str:
    """ Export research data to plain text format """
    try:
        buffer = io.StringIO()
        buffer.write(f"RESEARCH REPORT\n{'=' * 50}\n\n")
        buffer.write(f"Query: {research_data.get('query', 'Unknown')}\n")
        buffer.write(f"Date: {research_data.get('timestamp', 'N/A')}\n\n")
        buffer.write(f"Findings:\n{'-' * 50}\n\n")
        buffer.write(research_data.get('response', 'No response available'))
        buffer.write("\n\nSources:\n")
        for source in research_data.get('sources', []):
            buffer.write(
                f"{source.get('id', '?')}. {source.get('title', 'No title')} - {source.get('url', 'No URL')}\n"
            )
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Error exporting to TXT: {e}")
        return ""


def export_to_markdown(research_data: Dict[str, Any]) -> str:
    """ Export research data to Markdown format """
    try:
        buffer = io.StringIO()
        buffer.write(
            f"# Research Report: {research_data.get('query', 'Unknown')}\n\n")
        buffer.write(
            f"*Generated on: {research_data.get('timestamp', 'N/A')}*\n\n")
        buffer.write(
            f"---\n\n{research_data.get('response', 'No response available')}\n\n"
        )
        buffer.write("## Sources\n\n")
        for source in research_data.get('sources', []):
            buffer.write(
                f"- [{source.get('title', 'No title')}]({source.get('url', 'No URL')})\n"
            )
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Error exporting to Markdown: {e}")
        return ""


def export_to_docx(research_data: Dict[str, Any]) -> str:
    """ Export research data to DOCX format and return as base64 encoded string """
    try:
        from docx import Document
        document = Document()
        document.add_heading(f"Research Report", 0)
        document.add_paragraph(
            f"Query: {research_data.get('query', 'Unknown')}")
        document.add_paragraph(
            f"Date: {research_data.get('timestamp', 'N/A')}")
        document.add_paragraph("\n---\n")
        document.add_paragraph(
            research_data.get('response', 'No response available'))

        document.add_heading("Sources", level=1)
        for source in research_data.get('sources', []):
            document.add_paragraph(
                f"{source.get('id', '?')}. {source.get('title', 'No title')} - {source.get('url', 'No URL')}"
            )

        buffer = io.BytesIO()
        document.save(buffer)
        docx_content = buffer.getvalue()
        buffer.close()

        return base64.b64encode(docx_content).decode('utf-8')
    except Exception as e:
        logger.error(f"Error exporting to DOCX: {e}")
        return ""
