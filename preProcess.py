import fitz  # PyMuPDF
import re
import os
import pytesseract
from pdf2image import convert_from_path
import uuid

# ---------- CONFIG ----------
OCR_LANG = "eng"  # Add 'eng+deu' for multi-language
CHUNK_SIZE = 500  # Tokens or chars (we'll refine later)
CHUNK_OVERLAP = 50



def is_scanned_pdf(pdf_path):
    """Check if PDF is scanned by searching for text layer."""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            if page.get_text().strip():
                return False
    return True

def ocr_pdf(pdf_path):
    """OCR scanned PDFs into text."""
    pages = convert_from_path(pdf_path)
    text = ""
    for page_img in pages:
        text += pytesseract.image_to_string(page_img, lang=OCR_LANG) + "\n"
    return text

def extract_text(pdf_path):
    """Extract text from PDF or OCR if scanned."""
    if is_scanned_pdf(pdf_path):
        print(f"[OCR] Running OCR on: {pdf_path}")
        return ocr_pdf(pdf_path)
    else:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text

def remove_headers_footers(text):
    """Remove repetitive headers/footers."""
    lines = text.split("\n")
    # Detect repeated lines
    from collections import Counter
    counts = Counter(lines)
    repetitive = {line for line, cnt in counts.items() if cnt > 3 and len(line) < 80}
    cleaned = [line for line in lines if line not in repetitive]
    return "\n".join(cleaned)

def normalize_text(text):
    """Clean OCR errors and normalize spaces."""
    text = re.sub(r"\s+", " ", text)
    text = text.replace("–", "-").replace("’", "'").replace("“", '"').replace("”", '"')
    return text.strip()

def split_into_sections(text):
    """Split by legal numbering (e.g., Section 1, 1.1, etc.)."""
    pattern = r"(?=(?:Section|Article|Clause)\s+\d+[\.\d]*)"
    sections = re.split(pattern, text, flags=re.IGNORECASE)
    sections = [sec.strip() for sec in sections if sec.strip()]
    return sections

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Chunk text with overlap."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += size - overlap
    return chunks

def extract_metadata(file_name, jurisdiction="UK", doc_type="statute", effective_date=None):
    """Attach metadata for filtering."""
    return {
        "id": str(uuid.uuid4()),
        "file_name": file_name,
        "doc_type": doc_type,
        # "jurisdiction": jurisdiction,
        # "effective_date": effective_date or datetime.utcnow().isoformat(),
        # "source": f"local://{file_name}"
    }



def preprocess_pdf(pdf_path):
    raw_text = extract_text(pdf_path)
    cleaned_text = remove_headers_footers(raw_text)
    normalized_text = normalize_text(cleaned_text)
    sections = split_into_sections(normalized_text)

    all_chunks = []
    for section in sections:
        section_chunks = chunk_text(section)
        all_chunks.extend(section_chunks)

    metadata = extract_metadata(os.path.basename(pdf_path))
    processed_docs = [{"text": chunk, "metadata": metadata} for chunk in all_chunks]

    return processed_docs