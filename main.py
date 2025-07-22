import pytesseract
from pdf2image import convert_from_path
from PIL import ImageOps, ImageEnhance
from pathlib import Path

# --- CONFIGURATION ---
tesseract_path = r"C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\Users\user\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pdf_folder = Path(r"C:\Users\user\Desktop\pdf2txt\test_pdf_folder")
output_folder = Path(r"C:\Users\user\Desktop\pdf2txt\output")

# Ensure output folder exists
output_folder.mkdir(parents=True, exist_ok=True)

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = tesseract_path
custom_config = r'--oem 3 --psm 3'  # More flexible layout and engine

# --- PROCESSING PDFs ---
for pdf_path in pdf_folder.glob("*.pdf"):
    txt_output_path = output_folder / (pdf_path.stem + ".txt")

    if txt_output_path.exists():
        print(f"⏭ Skipping (already converted): {pdf_path.name}")
        continue

    print(f"🔄 Processing: {pdf_path.name}")
    try:
        pages = convert_from_path(str(pdf_path), dpi=300, poppler_path=poppler_path)

        all_text = ""
        for i, page in enumerate(pages):
            # --- IMAGE PREPROCESSING ---
            gray = ImageOps.grayscale(page)                      # Convert to grayscale
            contrast = ImageEnhance.Contrast(gray).enhance(2.0)  # Increase contrast
            resized = contrast.resize((contrast.width * 2, contrast.height * 2))  # Resize to help Thai OCR

            # --- OCR ---
            text = pytesseract.image_to_string(resized, lang='tha+eng', config=custom_config)
            all_text += f"\n--- Page {i+1} ---\n{text}"

        # --- SAVE TO .TXT ---
        with open(txt_output_path, "w", encoding="utf-8") as f:
            f.write(all_text)

        print(f"✅ Saved: {txt_output_path.name}")

    except Exception as e:
        print(f"❌ Error with {pdf_path.name}: {e}")

print("\n🎉 All PDFs processed with image preprocessing.")