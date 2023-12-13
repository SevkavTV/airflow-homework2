import easyocr
import re

def perform_ocr(image_path):
    reader = easyocr.Reader(['en'])
    text_results = reader.readtext(image_path, detail=0)
    
    combined_text = " ".join(text_results)

    domain = extract_domain(combined_text)
    return domain

def extract_domain(text):
    pattern = r'\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]{1,63}\.[a-zA-Z]{2,6})\b'
    
    match = re.search(pattern, text)

    if match:
        return match.group(1)

    return None
