import os
import re
import pymupdf

names_list = [
    # "HON. JUSTICE MARSHAL UMUKORO \n (LIFE BENCHER) +1",
    "Hon. Justice Onome Marshal-Umukoro",
    "Mr. Obatarhe Marshal-Umukoro",
]

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

    x0 = p_width * 0.28
    x1 = p_width * 0.93
    y0 = p_height * 0.61
    y1 = p_height * 0.70
    start_font_size = 18

    return pymupdf.Rect(x0, y0, x1, y1), start_font_size


def format_long_name(name):
    # If the user already manually added a newline (\n), preserve it
    if "\n" in name:
        lines = [line.strip() for line in name.split("\n")]
        return "\n".join(lines)

    # Automatic split for long single-line names
    if len(name) > 35:
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

    # Clean name while retaining user-inserted newlines (\n)
    clean_lines = [
        re.sub(r"^[0-9.]+\s*|\s*<.*?>", "", line).strip().upper()
        for line in name.split("\n")
    ]
    clean_name = "\n".join(clean_lines)

    # Format long names onto multiple lines
    formatted_name = format_long_name(clean_name)

    box_rect, font_size = get_relative_box_and_size(page)
    min_size = 6

    page.insert_font(fontname=font_alias, fontfile=font_path)

    while font_size >= min_size:
        # Note: Set line height via expand parameter or standard fit;
        # PyMuPDF handles tight line spacing natively when font size fits box
        rc = page.insert_textbox(
            box_rect,
            formatted_name,
            fontsize=font_size,
            fontname=font_alias,
            color=RICH_BROWN,
            align=pymupdf.TEXT_ALIGN_CENTER,
            overlay=True,
        )

        if rc >= 0:
            break

        font_size -= 0.5

    # Clean filename (strip newlines and non-alphanumeric chars)
    single_line_clean = formatted_name.replace("\n", " ")
    safe_name = "".join(
        c for c in single_line_clean if c.isalnum() or c in (" ", "_", "-", "&")
    ).strip()
    safe_name = re.sub(r"\s+", " ", safe_name)

    output_filename = (
        f"{safe_name} (NOV 14) WHITE WED INVITE-DTO&DORIS VIP 2026 (ASABA).pdf"
    )

    doc.save(os.path.join(output_dir, output_filename))
    doc.close()

print(f"White Wedding batch complete! Generated {len(names_list)} PDFs.")
