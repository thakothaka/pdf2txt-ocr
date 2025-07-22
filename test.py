from pdf2image import convert_from_path
from PIL import ImageOps, ImageEnhance
from pathlib import Path

# --- CONFIG ---
poppler_path = r"C:\Users\user\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pdf_folder = Path(r"C:\Users\user\Desktop\pdf2txt\test_pdf_folder")

# Get first PDF file in the folder
pdf_files = list(pdf_folder.glob("*.pdf"))
if not pdf_files:
    print("❌ No PDF files found.")
    exit()

pdf_path = pdf_files[0]
print(f"🖼 Showing processed image for: {pdf_path.name} (Page 1)")

# Convert first page to image
pages = convert_from_path(str(pdf_path), dpi=300, first_page=1, last_page=1, poppler_path=poppler_path)
page = pages[0]

# --- Image Preprocessing ---
gray = ImageOps.grayscale(page)
contrast = ImageEnhance.Contrast(gray).enhance(2.0)
resized = contrast.resize((gray.width * 2, gray.height * 2))  # Double size

# --- Show Image ---
resized.show()  # Opens in default image viewer
