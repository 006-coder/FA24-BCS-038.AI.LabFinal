def decision(original_text, injection_score, pii_results):
    redacted_text = ""
    if pii_results:
        redacted_text = original_text
        for item in pii_results:
            redacted_text = redacted_text.replace(item["Value"], f"[{item['Type']}]")

    if injection_score >= 70:
        return "BLOCK", f"Access Denied: prompt injection detected. Your text: \"{redacted_text}\""

    if pii_results:
        return "MASK", redacted_text

    return "ALLOW", original_text