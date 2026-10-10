from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

DARK = colors.HexColor("#262626")
YELLOW = colors.HexColor("#F2C94C")
LIGHT_GREY = colors.HexColor("#F6F6F6")
BORDER = colors.HexColor("#DDDDDD")
TEXT_GREY = colors.HexColor("#666666")


def _safe_text(value):
    """Safely display database text inside ReportLab Paragraphs."""
    if value is None or value == "":
        return "-"
    return escape(str(value))


def _money(value):
    """Format an amount stored in the order."""
    try:
        return f"Rs. {float(value):,.2f}"
    except (TypeError, ValueError):
        return "Rs. 0.00"


def _format_order_date(value):
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y, %I:%M %p")

    if value:
        return str(value)

    return "Not available"


def generate_invoice_pdf(order):
    """
    Generate an A4 invoice PDF from a verified order dictionary.

    Returns:
        BytesIO: A seeked PDF buffer ready for Flask send_file().
    """
    if not isinstance(order, dict):
        raise ValueError("Order must be a dictionary.")

    if not order.get("order_id"):
        raise ValueError("Order ID is missing.")

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title=f"MadHut Invoice - {order['order_id']}",
        author="MadHut",
    )

    styles = getSampleStyleSheet()

    brand_style = ParagraphStyle(
        "MadHutBrand",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=DARK,
        alignment=0,
        spaceAfter=0,
    )

    invoice_style = ParagraphStyle(
        "InvoiceHeading",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=DARK,
        alignment=TA_RIGHT,
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=DARK,
        spaceAfter=5,
    )

    normal_style = ParagraphStyle(
        "InvoiceNormal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=DARK,
    )

    small_style = ParagraphStyle(
        "InvoiceSmall",
        parent=normal_style,
        fontSize=8,
        leading=11,
        textColor=TEXT_GREY,
    )

    product_style = ParagraphStyle(
        "InvoiceProduct",
        parent=normal_style,
        fontSize=8,
        leading=11,
        wordWrap="CJK",
    )

    right_style = ParagraphStyle(
        "InvoiceRight",
        parent=normal_style,
        alignment=TA_RIGHT,
    )

    center_style = ParagraphStyle(
        "InvoiceCenter",
        parent=normal_style,
        alignment=TA_CENTER,
    )

    story = []

    # -------------------------------------------------
    # Header
    # -------------------------------------------------
    header = Table(
        [[
            Paragraph("MadHut", brand_style),
            Paragraph("INVOICE", invoice_style),
        ]],
        colWidths=[85 * mm, 85 * mm],
    )

    header.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -1), 2, YELLOW),
        ])
    )

    story.append(header)
    story.append(Spacer(1, 7 * mm))

    # -------------------------------------------------
    # Order information
    # -------------------------------------------------
    order_id = _safe_text(order.get("order_id"))
    order_date = _safe_text(
        _format_order_date(order.get("created_at"))
    )

    order_info = Table(
        [
            [
                Paragraph("<b>Order / Invoice Reference</b>", normal_style),
                Paragraph("<b>Order Date</b>", right_style),
            ],
            [
                Paragraph(order_id, small_style),
                Paragraph(order_date, right_style),
            ],
        ],
        colWidths=[85 * mm, 85 * mm],
    )

    order_info.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ])
    )

    story.append(order_info)
    story.append(Spacer(1, 7 * mm))

    # -------------------------------------------------
    # Customer and shipping address
    # -------------------------------------------------
    shipping = order.get("shipping_address") or {}

    address_parts = [
        shipping.get("address"),
        shipping.get("city"),
        shipping.get("pincode"),
    ]

    address = ", ".join(
        str(part) for part in address_parts if part
    ) or "-"

    customer_content = [
        Paragraph("<b>BILL TO / SHIP TO</b>", section_style),
        Paragraph(
            f"<b>{_safe_text(shipping.get('full_name'))}</b>",
            normal_style,
        ),
        Paragraph(_safe_text(address), small_style),
        Paragraph(
            f"Phone: {_safe_text(shipping.get('phone'))}",
            small_style,
        ),
    ]

    customer_table = Table(
        [[customer_content]],
        colWidths=[170 * mm],
    )

    customer_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ])
    )

    story.append(customer_table)
    story.append(Spacer(1, 7 * mm))

    # -------------------------------------------------
    # Items table
    # -------------------------------------------------
    story.append(Paragraph("ORDER ITEMS", section_style))

    item_rows = [[
        "Product",
        "Size",
        "Color",
        "Qty",
        "Unit Price",
        "Amount",
    ]]

    items = order.get("items") or []

    if not isinstance(items, list) or not items:
        raise ValueError("Order has no invoice items.")

    for item in items:
        quantity = item.get("quantity", 0)
        price = item.get("price", 0)
        subtotal = item.get("subtotal", 0)

        item_rows.append([
            Paragraph(_safe_text(item.get("name")), product_style),
            _safe_text(item.get("size")),
            _safe_text(item.get("color")),
            str(quantity),
            _money(price),
            _money(subtotal),
        ])

    items_table = Table(
        item_rows,
        colWidths=[
            64 * mm,
            13 * mm,
            17 * mm,
            12 * mm,
            29 * mm,
            30 * mm,
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    items_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (1, 1), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (3, 1), (-1, -1), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(items_table)
    story.append(Spacer(1, 6 * mm))

    # -------------------------------------------------
    # Order total
    # -------------------------------------------------
    total_table = Table(
        [[
            Paragraph("<b>Order Total</b>", normal_style),
            Paragraph(
                f"<b>{_money(order.get('total_amount'))}</b>",
                right_style,
            ),
        ]],
        colWidths=[125 * mm, 45 * mm],
    )

    total_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1),
             colors.HexColor("#FFF6D8")),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    story.append(total_table)
    story.append(Spacer(1, 6 * mm))

    # -------------------------------------------------
    # Payment details
    # -------------------------------------------------
    payment_table = Table(
        [
            [
                Paragraph("<b>Payment Method</b>", normal_style),
                Paragraph("<b>Payment Status</b>", right_style),
            ],
            [
                Paragraph(
                    _safe_text(order.get("payment_mode")),
                    small_style,
                ),
                Paragraph(
                    _safe_text(order.get("payment_status")),
                    right_style,
                ),
            ],
        ],
        colWidths=[85 * mm, 85 * mm],
    )

    payment_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ])
    )

    story.append(payment_table)
    story.append(Spacer(1, 12 * mm))

    footer_style = ParagraphStyle(
        "InvoiceFooter",
        parent=normal_style,
        alignment=TA_CENTER,
        textColor=TEXT_GREY,
        fontSize=9,
    )

    story.append(
        Paragraph(
            "Thank you for shopping with MadHut!",
            footer_style,
        )
    )

    # Build PDF and return it in memory.
    document.build(story)
    buffer.seek(0)

    return buffer
