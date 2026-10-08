import os
import re

import pymupdf

names_list = [
    "Mr. Olumide Akpata",
    "Hon. Tony Elekeokwuri",
    "Hon. Sebastian Okoh",
    "Hon. Teddy Jackson",
    "Hon. Mrs Cordelia Anyanwu",
    "Hon. Charles Aniagwu",
    "Hon. Chief Blessing Oborevwori",
    "Mr. Obatarhe Marshal-Umukoro",
]

# Update this to point to your white wedding master PDF template
template_pdf_path = "WHITE_WEDDING_VIP.pdf"
output_dir = "output_white_wedding_vip"

font_path = "Cinzel-SemiBold.ttf"
font_alias = "cinzel_semibold"

RICH_BROWN = (74 / 255, 46 / 255, 26 / 255)

os.makedirs(output_dir, exist_ok=True)


def get_relative_box_and_size(page):
    """Relative coordinates for the white wedding template box."""
    p_width = page.rect.width
    p_height = page.rect.height

    x0 = p_width * 0.25
    x1 = p_width * 0.93
    y0 = p_height * 0.63
    y1 = p_height * 0.68
    start_font_size = 18

    return pymupdf.Rect(x0, y0, x1, y1), start_font_size


def format_long_name(name):
    # If the name is unusually long (e.g., > 35 characters), format into 2 lines
    if len(name) > 35:
        # Split before suffixes like (Life Bencher), +1, or & Wife
        if " (" in name:
            return name.replace(" (", "\n(", 1)
        elif " +" in name:
            return name.replace(" +", "\n+", 1)
        elif " & " in name:
            return name.replace(" & ", "\n& ", 1)
    return name


for name in names_list:
    doc = pymupdf.open(template_pdf_path)
    page = doc[0]

    # Clean the string
    clean_name = re.sub(r"^[0-9.]+\s*|\s*<.*?>", "", name).strip().upper()

    # Format long names onto multiple lines
    formatted_name = format_long_name(clean_name)

    box_rect, font_size = get_relative_box_and_size(page)
    min_size = 6

    page.insert_font(fontname=font_alias, fontfile=font_path)

    while font_size >= min_size:
        rc = page.insert_textbox(
            box_rect,
            formatted_name,  # Pass the multiline string here
            fontsize=font_size,
            fontname=font_alias,
            color=RICH_BROWN,
            align=pymupdf.TEXT_ALIGN_CENTER,
            overlay=True,
        )

        if rc >= 0:
            break

        font_size -= 0.5

    safe_name = "".join(
        c for c in clean_name if c.isalnum() or c in (" ", "_", "-", "&")
    ).strip()

    output_filename = (
        f"{safe_name} (NOV 14) WHITE WED INVITE-DTO&DORIS VIP 2026 (ASABA).pdf"
    )

    doc.save(os.path.join(output_dir, output_filename))
    doc.close()

print(f"White Wedding batch complete! Generated {len(names_list)} PDFs.")
