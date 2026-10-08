import os
import re
import pymupdf

names_list = [
    "Mr. Olumide Akpata",
    "Mr. Adetunji Osho SAN",
    "Mr. Tobenna Erojikwe",
    "Mr. Steve Nwabueze",
    "Dr. Ibrahim Effiong",
    "Mr. Andrew Odum SAN",
    "Mr. Emuobonuvie Majemite + 1",
    "Daniel Oyetoro",
    "Mr. Jeffrey Benson",
    "Mr. Jude Akpobire",
    "Engr. Maxwell Kwentua",
    "Dr. Pedro Obi",
    "Prof Nasiru Tijani",
    "Dr. Gbenga Orimogunje",
    "Mr. Ayo Shonaiya",
    "Mr. Joshua Nwachukwu",
    "Mrs. Jacqueline Agweh",
    "Hon. Dr. Midala Usman Balami",
    "Hon. Marilyn Okowa-Daramola",
    "Hon. Sebastian Okoh",
    "Mr. Iyke Mordi & Wife",
    "Dr. Steve Ojieh & Wife",
    "Mr. Chidi Odoemenam",
    "Mr. Uche Mgbakor",
    "Mr. Kehiku Irabor",
    "Mr. Desmond Ogba",
    "Hon. Justice Marcel Okoh",
    "Queen Anthonia Ezeagwu & 5 Guests",
    "Mr. Okaleka Ifeanyi Blessing",
    "Mr. Cheeka Onyeka",
    "DTO Mentorship Group (5 persons)",
    "Mr. Kingsley Orisewezie",
    "Mr. Monday Eugene",
    "Mr. Clement Edeh",
    "Mr. Gbenga Emmanuel",
    "Mr. Abba Hikima",
    "Mr. Benny Ike Etche & Wife",
    "Mr. Chioma Martins",
    "Mrs. Beatrice Onyejose",
    "Ms. Oluwaseun Ogunbemi",
    "Mr. Ayodeji Adedamola",
    "Mr. Jephta Uwadiegwu",
    "Mr. Sotubo Olatubosun",
    "Ms. Tolu Das.",
    "Ibidoyin Aina Esq",
    "Mr. Chidi Awodika",
    "Chinelo Nwude Esq",
    "Mr. Favour Onuoha",
    "Mr. Quwadeen Adesokan",
    "Mr. Victor Igbedi",
    "Mr. Taiwo Olukoju",
    "Mr. Oluwaseun Adebayo & Wife",
    "Mr. Michael Adebayo",
    "Mr. Obinna Tony Vincent",
    "Mr. Banye Julius",
    "Prof. Uchenna Uzor",
    "Mr. Jago Emmanuel",
    "Mr. Seun Olayiwola",
    "Mr. Kelechi Ogbogo",
    "Yolanda Ojolam Esq",
    "Mr. Festus Ogun & Wife",
    "Mr. Farouq Obisanya & Wife",
    "Mr. Dickson Ibiebele",
    "Mr. C.C. Tochukwu",
    "Mr. Hamza Dantani",
    "Mr. Peter Obasi & Wife",
    "Mr. Timothy Obasi & Wife",
    "Mr. Segun & Wife",
    "Mr. Eric Woke & Wife",
    "Mr. Emmanuel Nwobodo",
    "Mr. Sunusi Musa SAN",
    "Mr. Abdulrahman Bibi",
    "Mr. Geoffrey Nwokolo",
    "Mr. Japhet Olayemi",
    "Mr. Ifeyemi Samuel",
    "Mr. Oliver Omoredia",
    "Mr. Ukwata Chike",
    "Mr. Rotimi Bankole.",
    "Ms. Vera Enubianuzor",
    "Engr. Samuel Ikiseh",
    "Mr. Oghenemine Donbraye",
    "Isaac Oguntokun.",
    "Mr. David Akintomide",
    "Mr. Ebunoluwa Tugbogbo",
]

input_dir = "input_pdfs"
output_dir = "output_pdfss"

font_path = "Cinzel-SemiBold.ttf"
font_alias = "cinzel_semibold"

os.makedirs(output_dir, exist_ok=True)

pdf_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")])


def get_relative_box_and_size(page, pdf_name):
    """Returns targeted coordinates and initial font size based on PDF number range."""
    p_width = page.rect.width
    p_height = page.rect.height

    match = re.search(r"\d+", pdf_name)  # [cite: 2]
    pdf_num = int(match.group()) if match else 0

    if 151 <= pdf_num <= 200:
        x0 = p_width * 0.12
        x1 = p_width * 0.88
        y0 = p_height * 0.82
        y1 = p_height * 0.95
        start_font_size = 28
    else:
        x0 = p_width * 0.15
        x1 = p_width * 0.85
        y0 = p_height * 0.82
        y1 = p_height * 0.90
        start_font_size = 14

    return pymupdf.Rect(x0, y0, x1, y1), start_font_size


for index, name in enumerate(names_list):
    if index >= len(pdf_files):
        print(f"Done inserting names. {len(pdf_files)} PDFs processed.")
        break

    pdf_name = pdf_files[index]
    pdf_path = os.path.join(input_dir, pdf_name)

    doc = pymupdf.open(pdf_path)
    page = doc[0]

    clean_name = re.sub(r"^[0-9.]+\s*|\s*<.*?>", "", name).strip().upper()

    box_rect, font_size = get_relative_box_and_size(page, pdf_name)
    min_size = 6

    # Register the font once per page BEFORE entering the sizing loop
    page.insert_font(fontname=font_alias, fontfile=font_path)

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

    safe_name = "".join(
        c for c in clean_name if c.isalnum() or c in (" ", "_", "-", "&")
    ).strip()

    output_filename = f"{safe_name} (OCT 17) TRAD WED INVITE-DTO&DORIS 2026 (IKEJA).pdf"
    doc.save(os.path.join(output_dir, output_filename))
    doc.close()

print("Batch complete!")
