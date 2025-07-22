from pathlib import Path
import shutil
import openpyxl

# 📂 Folder paths
txt_folder = Path(r"C:\Users\user\Desktop\pdf2txt\output")
pdf_folder = Path(r"C:\Users\user\Downloads\Tank Folder")
excel_path = Path(r"C:\Users\user\Desktop\search_keywords.xlsx")
filtered_root = Path(r"C:\Users\user\Desktop\pdf2txt\filtered")

# Ensure root output folder exists
filtered_root.mkdir(exist_ok=True)

# 📖 Load search words from Excel (column A)
wb = openpyxl.load_workbook(excel_path)
ws = wb.active
search_words = [str(cell.value).strip() for cell in ws['A'] if cell.value]

# ✅ Loop through each search word
for search_phrase in search_words:
    matched_files = []

    for txt_file in txt_folder.glob("*.txt"):
        page_numbers = set()
        current_page = None

        with open(txt_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("--- Page"):
                    parts = line.strip().split()
                    if len(parts) >= 3 and parts[2].isdigit():
                        current_page = int(parts[2])
                elif search_phrase in line and current_page is not None:
                    page_numbers.add(current_page)

        if page_numbers:
            pages = sorted(page_numbers)
            print(f"✅ Found '{search_phrase}' in {txt_file.name} on pages: {', '.join(map(str, pages))}")
            matched_files.append((txt_file.stem, pages))

    # Only create output folder and copy PDFs if at least one match
    if matched_files:
        output_pdf_folder = filtered_root / search_phrase
        output_pdf_folder.mkdir(parents=True, exist_ok=True)

        for base_name, _ in matched_files:
            matching_pdf = pdf_folder / f"{base_name}.pdf"
            if matching_pdf.exists():
                dest_path = output_pdf_folder / matching_pdf.name
                shutil.copy2(matching_pdf, dest_path)
                print(f"📁 Copied PDF to: {dest_path}")
            else:
                print(f"⚠️ PDF not found for: {base_name}.pdf")

print("\n🎉 All search phrases processed.")
