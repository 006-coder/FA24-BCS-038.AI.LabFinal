def decision(original_text, injection_score, pii_results):
    if injection_score >= 70:
        return "BLOCK", f"Access Denied: High Risk Detected ({injection_score}%)"

    if pii_results:
        redacted = original_text
        for item in pii_results:
            redacted = redacted.replace(item["Value"], f"<{item['Type']}>")
        return "MASK", redacted

    return "ALLOW", original_text