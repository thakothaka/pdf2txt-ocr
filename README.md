# PDF to Text OCR + Search Automation

This project consists of two Python scripts to automate OCR conversion of Thai/English PDFs and filter them by keywords from Excel.

## 📁 Project Structure
```bash
pdf2txt/
├── convert_pdf2txt.py         # Convert scanned PDFs to text with auto-rotation and preprocessing
├── search.py                  # Search text files for keywords from Excel and copy matching PDFs
├── pdf_folder/                # Input scanned PDF files
├── output/                    # Output text files (OCR results)
├── filtered/                  # Output folders for matched PDFs by keyword
├── search_keywords.xlsx       # Excel file with search keywords in column A
└── venv/                      # Optional: Python virtual environment
```
---

## Features

### `convert_pdf2txt.py`
- Converts all PDFs in a folder to text using Tesseract OCR
- Supports both Thai and English
- Detects and corrects image rotation automatically
- Increases contrast and resizes image for better OCR accuracy
- Saves results as `.txt` files

### `search.py`
- Loads keywords from an Excel file (Column A)
- Searches each `.txt` file for keywords
- Copies matched PDFs into a new folder named after the keyword

---

## Requirements

Install Python packages:
```bash
pip install pytesseract pdf2image pillow openpyxl
```

External dependencies
Tesseract OCR: [Download](https://github.com/UB-Mannheim/tesseract/wiki)

for Thai language : https://github.com/tesseract-ocr/tessdata

Poppler for Windows: [Download](https://github.com/oschwartz10612/poppler-windows/releases/)

## Configuration
Edit the following paths inside each script to match your system:

### convert_pdf2txt.py
```bash
tesseract_path = r"C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\Users\user\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pdf_folder = Path(r"C:\Users\user\Desktop\pdf2txt\pdf_folder")
output_folder = Path(r"C:\Users\user\Desktop\pdf2txt\output")
```
### search.py
```bash
txt_folder = Path(r"C:\Users\user\Desktop\pdf2txt\output")
pdf_folder = Path(r"C:\Users\user\Downloads\Tank Folder")
excel_path = Path(r"C:\Users\user\Desktop\search_keywords.xlsx")
filtered_root = Path(r"C:\Users\user\Desktop\pdf2txt\filtered")
```

## How to Use
### Step 1: Convert PDFs to Text
```bash
python convert_pdf2txt.py
```
Output will be in the output/ folder.

### Step 2: Search by Excel Keywords
Make sure your Excel file (search_keywords.xlsx) has keywords in Column A.
```bash
python search.py
```
Matched PDFs will be copied to filtered/ under each keyword-named folder.

##  Notes
Rotation is automatically corrected based on Tesseract's orientation detection.

OCR accuracy is improved with grayscale, contrast enhancement, and upscaling.

Make sure scanned PDFs are clean and legible.

## Credits
Developed by Jirawat Petcharoen

For personal document digitization and filtering
