import os
import re

import pymupdf

names_list = [
    "Mr. Godfrey Godwin Ekpo",
    "Hon. Raymond Mgbakor",
    "Mr. Ugochukwu Obi",
    "Mr. Paul Ifeanyi Okoh",
]

# Path to your single template PDF file
template_pdf_path = "RESERVED.pdf"
output_dir = "output_reserved_pdfs"

font_path = "Cinzel-SemiBold.ttf"
font_alias = "cinzel_semibold"

os.makedirs(output_dir, exist_ok=True)


def get_relative_box_and_size(page):
    """Calculates relative coordinates and starting font size for the single template."""
    p_width = page.rect.width
    p_height = page.rect.height

    x0 = p_width * 0.15
    x1 = p_width * 0.85
    y0 = p_height * 0.81
    y1 = p_height * 0.88
    start_font_size = 14

    return pymupdf.Rect(x0, y0, x1, y1), start_font_size


for name in names_list:
    # Open a fresh instance of the template PDF
    doc = pymupdf.open(template_pdf_path)
    page = doc[0]

    clean_name = re.sub(r"^[0-9.]+\s*|\s*<.*?>", "", name).strip().upper()

    box_rect, font_size = get_relative_box_and_size(page)
    min_size = 6

    # Register the font once on the page
    page.insert_font(fontname=font_alias, fontfile=font_path)

    # Shrink font until name fits completely
    while font_size >= min_size:
        rc = page.insert_textbox(
            box_rect,
            clean_name,
            fontsize=font_size,
            fontname=font_alias,
            color=(0x17 / 255, 0x6B / 255, 0x4D / 255),
            align=pymupdf.TEXT_ALIGN_CENTER,
            overlay=True,
        )

        if rc >= 0:
            break

        font_size -= 0.5

    # Format output filename
    safe_name = "".join(
        c for c in clean_name if c.isalnum() or c in (" ", "_", "-", "&")
    ).strip()
    output_filename = f"{safe_name} (OCT 17) TRAD WED INVITE-DTO&DORIS 2026 (IKEJA).pdf"

    doc.save(os.path.join(output_dir, output_filename))
    doc.close()

print(f"Batch complete! Generated {len(names_list)} PDFs.")
