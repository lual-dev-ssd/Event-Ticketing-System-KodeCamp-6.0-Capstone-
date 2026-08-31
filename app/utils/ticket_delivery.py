import io
import smtplib
import traceback
import qrcode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.utils.email import _send_smtp_message

from app.core.config import settings

def generate_qr_code_buffer(payload:str)-> bytes:
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1E293B", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

def generate_ticket_pdf_bytes(
    ticket_id:str,
    event_title:str,
    event_date:str = "Date & Time: See Event Details",
    location:str = "General Admission",
    price:str = "Paid"
)-> bytes:
    pdf_buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=(6.5 * inch, 3.8 * inch),
        rightMargin=12,
        leftMargin=12,
        topMargin=12,
        bottomMargin=12
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TicketTitke",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=colors.HexColor("#ffffff"),
        alignment=0,
        spaceAfter=0
    )

    meta_style = ParagraphStyle(
        "TicketMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    id_style = ParagraphStyle(
        "TicketID",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor = colors.HexColor('#64748B')
    )

    header_data = [[Paragraph(f"<b>ADMIT ONE: {event_title.upper()}</b>", title_style)]]
    header_table = Table(header_data, colWidths=[6.1 * inch], rowHeights=[35])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#4F46E5")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),

    ]))

    qr_buff = generate_qr_code_buffer(f"TICKET: {ticket_id}")
    qr_img = Image(qr_buff, width=1.4 * inch, height=1.4 * inch)

    details_text = f"""
    <b>Event:</b> {event_title}<br/><br/>
    <b>Date & Time:</b> {event_date}<br/><br/>
    <b>Location:</b> {location}<br/><br/>
    <b>Ticket Price:</b>{price}

    """

    body_data = [
        [Paragraph(details_text, meta_style), qr_img]
    ]

    body_table = Table(body_data, colWidths=[4.3 * inch, 1.8 * inch])
    body_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    footer_text = f"TICKET ID: {ticket_id} | VALID FOR SINGLE ENTRY"
    footer_data = [[Paragraph(footer_text, id_style)]]
    footer_table = Table(footer_data, colWidths=[6.1 * inch])
    footer_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))

    elements = [
        header_table,
        Spacer(1, 4),
        body_table,
        Spacer(1, 4),
        footer_table
    ]

    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()

def send_ticket_email_task(
    recipient_email:str,
    ticket_id:str,
    event_title:str
) -> None:
    qr_bytes = generate_ticket_pdf_bytes(
        ticket_id=ticket_id,
        event_title=event_title
    )

    msg = MIMEMultipart("related")
    msg["Subject"] = f"your Ticket for {event_title}"

    sender_email = getattr(settings, "EMAILS_FROM_EMAIL", settings.SMTP_USER) or settings.SMTP_USER
    msg["From"] = f"{getattr(settings, 'EMAILS_FROM_NAME','Event Ticketing')}<{sender_email}>"

    msg["Subject"] = f"Your Ticket for {event_title}"
    msg["From"] = f"{settings.EMAILS_FROM_NAME}<{settings.EMAILS_FROM_EMAIL}>"
    msg["To"] = recipient_email

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color:#333;">
    <h2>Your Ticket is Ready!</h2>
    <p>Thank you for  your booking for<strong>{event_title}</strong>.</p>
    <p>We have attached your official PDF ticket to this email. Please download it and present the embedded QR at the venue entrance.</p>
    <p><strong>Ticket ID:</strong> <code>{ticket_id}</code></p>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    pdf_attachment = MIMEApplication(qr_bytes, _subtype="pdf")
    pdf_attachment.add_header("Content-Disposition", "attachment", filename=f"Ticket_{ticket_id[:8]}.pdf")
    msg.attach(pdf_attachment)

    
    try:
        _send_smtp_message(msg)
        print(f"[Ticket Success] sent ticket PDF to {recipient_email}")
    except Exception as exc:
        print(f"Failed to deliver ticket email: {exc}")
        traceback.print_exc()