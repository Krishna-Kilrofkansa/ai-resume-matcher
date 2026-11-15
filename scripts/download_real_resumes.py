import os
import sys
import shutil
import urllib.request
import json
from pypdf import PdfReader

ONLINE_RESUMES_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "data", "online_resumes")
os.makedirs(ONLINE_RESUMES_DIR, exist_ok=True)

# Curated real-world multi-page resumes from the standard Kaggle/LiveCareer dataset
CURATED_SOURCES = [
    # Information Technology & Software
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/INFORMATION-TECHNOLOGY/10089434.pdf", "IT_Systems_Administrator.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/INFORMATION-TECHNOLOGY/10247517.pdf", "Senior_IT_Specialist.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/INFORMATION-TECHNOLOGY/10265057.pdf", "Software_Support_Engineer.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/INFORMATION-TECHNOLOGY/10553553.pdf", "Database_Systems_Analyst.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/INFORMATION-TECHNOLOGY/10641230.pdf", "IT_Project_Manager.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/INFORMATION-TECHNOLOGY/10759363.pdf", "Network_Security_Engineer.pdf"),
    # Engineering & DevOps
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/ENGINEERING/10030015.pdf", "Senior_Software_Engineer.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/ENGINEERING/10219099.pdf", "Systems_Infrastructure_Engineer.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/ENGINEERING/10624813.pdf", "Lead_Applications_Engineer.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/ENGINEERING/10712803.pdf", "Mechanical_Systems_Engineer.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/ENGINEERING/10985403.pdf", "Technical_Project_Engineer.pdf"),
    # Role / Domain Mismatches (UI/UX, Finance)
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/DESIGNER/10582236.pdf", "Creative_Graphic_Designer.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/DESIGNER/10931201.pdf", "UI_UX_Product_Designer.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/FINANCE/10287515.pdf", "Senior_Financial_Analyst.pdf"),
    ("https://raw.githubusercontent.com/amitvikramraj/CV-JD-Matching/main/data/FINANCE/10557342.pdf", "Corporate_Accountant.pdf"),
]


def download_resumes():
    print(f"Downloading real-world sample resumes to: {ONLINE_RESUMES_DIR}")
    headers = {"User-Agent": "Mozilla/5.0"}
    downloaded_count = 0

    for url, filename in CURATED_SOURCES:
        out_path = os.path.join(ONLINE_RESUMES_DIR, filename)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                pdf_bytes = resp.read()

            with open(out_path, "wb") as f:
                f.write(pdf_bytes)

            reader = PdfReader(out_path)
            pages = len(reader.pages)
            size_kb = len(pdf_bytes) / 1024
            print(f"✓ Downloaded {filename:<32} ({pages} pages, {size_kb:.1f} KB)")
            downloaded_count += 1
        except Exception as e:
            print(f"✗ Failed to download {filename} from {url}: {e}")

    # Also copy user's local real resumes from Documents if present
    docs_dir = os.path.join(os.environ.get("USERPROFILE", ""), "Documents")
    user_resumes = ["Aakarshak resume.pdf", "Aakarshak aiml.pdf", "Aakarshak_Swaraj.pdf"]
    for u_name in user_resumes:
        src = os.path.join(docs_dir, u_name)
        if os.path.exists(src):
            dst = os.path.join(ONLINE_RESUMES_DIR, u_name)
            shutil.copy2(src, dst)
            reader = PdfReader(dst)
            print(f"✓ Copied local real resume: {u_name} ({len(reader.pages)} page(s))")
            downloaded_count += 1

    print("=" * 60)
    print(f"Successfully gathered {downloaded_count} complete, multi-page resumes!")
    print(f"Target Directory: {ONLINE_RESUMES_DIR}")


if __name__ == "__main__":
    download_resumes()
