import re

def clean_ocr_text(text: str) -> str:
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Enlève caractères spéciaux
    return text.strip()

def extract_metadata(text: str) -> dict:
    metadata = {}
    lines = text.split("\n")

    for line in lines:
        if "Date" in line or re.search(r'\d{2}/\d{2}/\d{4}', line):
            metadata["date"] = line.strip()
        elif "Auteur" in line or "Author" in line:
            metadata["author"] = line.strip()
        elif "Titre" in line or "Title" in line:
            metadata["title"] = line.strip()

    return metadata

def guess_document_type(text: str) -> str:
    text = text.lower()
    if "facture" in text or "montant" in text:
        return "facture"
    elif "rapport" in text or "conclusion" in text:
        return "rapport"
    elif "objet" in text and "cordialement" in text:
        return "lettre"
    return "inconnu"
