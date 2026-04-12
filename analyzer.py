import re

def analyzer(text):
    detected_text = []
    patterns = {
        "REGISTRATION_NUMBER": r"(?:CIIT/)?(?:SP|FA)\d{2}[- ]?[A-Z]{3}[- ]?\d{3}(?:/WAH)?",
        "PHONE_NUMBER": r"(?:\+92|0) ?3\d{2}[- ]?\d{7}",
        "CNIC": r"\d{5}-\d{7}-\d",
        "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "CREDIT_CARD": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
        "ADDRESS": r"(?:House|Flat|Plot|Street|St)\s?#?\s?\d+[a-zA-Z0-9\s,.-]+",
        "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    }

    for text_type, regex in patterns.items():
        matching_items = re.findall(regex, text, re.IGNORECASE)
        for final_match in matching_items:
            detected_text.append({"Type": text_type, "Value": final_match})

    return detected_text