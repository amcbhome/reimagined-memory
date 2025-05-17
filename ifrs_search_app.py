import fitz  # PyMuPDF
import pandas as pd
import os

def extract_pdf_to_csv(pdf_path, output_csv_path):
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found at: {pdf_path}")
        return
    
    doc = fitz.open(pdf_path)
    data = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        data.append({'Page': page_num + 1, 'Content': text})

    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)
    print(f"✅ Extraction complete. CSV saved to: {output_csv_path}")

if __name__ == "__main__":
    pdf_file = "ifrs-for-smes.pdf"  # Ensure this PDF is in the project directory
    output_csv = "ifrs_smes_full_text.csv"
    extract_pdf_to_csv(pdf_file, output_csv)
