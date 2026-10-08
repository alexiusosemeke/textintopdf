import os
import re

import fitz  # PyMuPDF

# List of names provided
names_list = [
    "Mr. Olumide Akpata",
    "Mr. Adetunji Osho SAN",
    "Mr. Tobenna Erojikwe",
    "Mr. Steve Nwabueze",
    "Dr. Ibrahim Effiong",
    "Mr. Andrew Odum SAN",
    "Mr. Emuobonuvie Majemite",
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
    "Professor Uchenna Uzor",
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
output_dir = "output_pdfs"

os.makedirs(output_dir, exist_ok=True)

# Get sorted list of PDFs to maintain systematic matching
pdf_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")])


def get_box_rect(page):
    """Return the correct white box coordinates for the current invite template."""
    width = page.rect.width
    height = page.rect.height

    if width > 400 or height > 600:
        return fitz.Rect(50, 520, 545, 620)
    return fitz.Rect(28, 310, 270, 370)


def get_fitting_font_size(text, box_rect, fontname="helv", min_size=8, max_size=18):
    """Return a font size that keeps long names readable and inside the box."""
    usable_width = box_rect.width - 12

    # Longer names should start shrinking earlier so they look balanced inside the box.
    if len(text) > 26:
        max_size = 12
    elif len(text) > 20:
        max_size = 14
    elif len(text) > 16:
        max_size = 16
    else:
        max_size = 18

    for size in range(max_size, min_size - 1, -1):
        if fitz.get_text_length(text, fontname=fontname, fontsize=size) <= usable_width:
            return size

    return min_size


for index, name in enumerate(names_list):
    if index >= len(pdf_files):
        print(f"Done inserting names. {len(pdf_files)} PDFs processed.")
        break

    pdf_name = pdf_files[index]
    doc = fitz.open(os.path.join(input_dir, pdf_name))
    page = doc[0]  # First page
    box_rect = get_box_rect(page)

    # Clean name string
    clean_name = re.sub(r"^[0-9.]+\s*|\s*<.*?>", "", name).strip()
    clean_name = clean_name.upper()

    # Choose a readable font size that fits the white box, while keeping text centered
    font_size = get_fitting_font_size(clean_name, box_rect)

    page.insert_textbox(
        box_rect,
        clean_name,
        fontsize=font_size,
        fontname="helv",  # Bold option: "helv-bold"
        color=(0x17 / 255, 0x6B / 255, 0x4D / 255),  # #176B4D
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # Save processed PDF
    safe_filename = "".join(
        c for c in clean_name if c.isalnum() or c in (" ", "_", "-")
    ).rstrip()
    output_filename = f"{os.path.splitext(pdf_name)[0]}_{safe_filename}.pdf"
    doc.save(os.path.join(output_dir, output_filename))
    doc.close()

print("Batch complete!")
