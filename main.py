from fastapi import FastAPI
from prompt_injection import detect_promptInjection
from jailbreak import detect_jailbreak
from analyzer import analyzer
from policy_decision import decision
app = FastAPI(title="AI Security Gateway Project")
@app.post("/check-security")
def security_gateway(payload: dict):
    user_text = payload.get("text", "")

    if not user_text:
        return {"error": "No text provided"}

    injection_score = detect_promptInjection(user_text)
    jailbreak_score = detect_jailbreak(user_text)
    final_risk_score = injection_score + jailbreak_score
    pii_results = analyzer(user_text)
    status, final_result = decision(user_text, final_risk_score, pii_results)

    return {
        "status": status,
        "decision result": final_result,
        "metadata": {
            "Injection Score": injection_score,
            "Jailbreak Score": jailbreak_score,
            "PII Count": len(pii_results)
        }
    }