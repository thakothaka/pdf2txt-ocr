from pathlib import Path

# 🔍 Phrase to search
search_phrase = "945-TK1B"

# 📂 Folder with .txt files
txt_folder = Path(r"C:\Users\user\Desktop\pdf2txt\output")

# Loop through .txt files
for txt_file in txt_folder.glob("*.txt"):
    page_numbers = set()
    current_page = None

    with open(txt_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("--- Page"):
                # Detect page header like "--- Page 2 ---"
                parts = line.strip().split()
                if len(parts) >= 3 and parts[2].isdigit():
                    current_page = int(parts[2])
            elif search_phrase in line and current_page is not None:
                page_numbers.add(current_page)

    if page_numbers:
        pages = sorted(page_numbers)
        print(f"✅ Found in {txt_file.name} on pages: {', '.join(map(str, pages))}")
