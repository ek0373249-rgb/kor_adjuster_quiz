import os
import json
from pypdf import PdfReader

# Configuration
PDF_DIR = r"c:\Users\kim\Documents\Antigravity\01_Adjuster_test\02기출문제"
OUTPUT_FILE = "extracted_exam_text.json"

def extract_text_from_pdfs(pdf_dir, output_file):
    results = []
    
    # Check if directory exists
    if not os.path.exists(pdf_dir):
        print(f"Error: Directory {pdf_dir} not found.")
        return

    # List all PDF files
    files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    print(f"Found {len(files)} PDF files.")

    for filename in files:
        file_path = os.path.join(pdf_dir, filename)
        print(f"Processing: {filename}...")
        
        try:
            reader = PdfReader(file_path)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
            
            results.append({
                "filename": filename,
                "content": text_content
            })
            print(f"  - Extracted {len(text_content)} characters.")
            
        except Exception as e:
            print(f"  - Failed to extract text from {filename}: {e}")

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Extraction complete. Saved to {output_file}")

if __name__ == "__main__":
    extract_text_from_pdfs(PDF_DIR, OUTPUT_FILE)
