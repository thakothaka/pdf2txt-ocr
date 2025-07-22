import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import re

# --- CONFIGURATION ---
tesseract_path = r"C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\Users\user\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pdf_folder = Path(r"C:\Users\user\Desktop\pdf2txt\pdf_folder")
output_folder = Path(r"C:\Users\user\Desktop\pdf2txt\output")

# Setup
pytesseract.pytesseract.tesseract_cmd = tesseract_path
custom_config = r'--oem 3 --psm 3'
output_folder.mkdir(parents=True, exist_ok=True)

# --- MAIN LOOP ---
for pdf_path in pdf_folder.glob("*.pdf"):
    txt_output_path = output_folder / f"{pdf_path.stem}.txt"
    if txt_output_path.exists():
        print(f"⏭ Skipping (already exists): {pdf_path.name}")
        continue

    print(f"🔄 Processing: {pdf_path.name}")
    try:
        pages = convert_from_path(str(pdf_path), dpi=300, poppler_path=poppler_path)
        all_text = ""

        for i, img in enumerate(pages):
            # --- Convert to grayscale
            gray = ImageOps.grayscale(img)

            # --- Auto rotation detection ---
            osd = pytesseract.image_to_osd(gray, config='--psm 0')
            rotation_match = re.search(r"Rotate: (\d+)", osd)
            rotation = int(rotation_match.group(1)) if rotation_match else 0
            print(f"🔁 Detected rotation: {rotation} degrees")

            # --- Rotate to correct orientation ---
            if rotation != 0:
                gray = gray.rotate(-rotation, expand=True)  # Negative = clockwise

            # --- Preprocessing ---
            contrast = ImageEnhance.Contrast(gray).enhance(2.0)
            resized = contrast.resize((contrast.width * 2, contrast.height * 2))

            # --- OCR ---
            text = pytesseract.image_to_string(resized, lang='tha+eng', config=custom_config)
            all_text += f"\n--- Page {i+1} ---\n{text}"

        # --- Save to .txt ---
        with open(txt_output_path, "w", encoding="utf-8") as f:
            f.write(all_text)
        print(f"✅ Saved: {txt_output_path.name}")

    except Exception as e:
        print(f"❌ Error in {pdf_path.name}: {e}")

print("\n🎉 All PDFs processed with rotation fix and OCR.")
