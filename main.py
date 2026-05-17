from fastapi import FastAPI
from prompt_injection import detect_promptInjection
from jailbreak import detect_jailbreak
from analyzer import analyzer
from policy_decision import decision
from security_llm import get_llm_security_score
import time
import yaml

app = FastAPI(title="Robust AI Security Gateway - Lab Final")


with open("gateway_config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Dynamically extract the settings
RISK_THRESHOLD = config["security_settings"]["risk_threshold"]
LLM_MODEL = config["security_settings"]["llm_model"]

# NOW USE THESE VARIABLES IN YOUR LOGIC INSTEAD OF HARDCODED VALUES:
# Example in your security route:
# if final_risk >= RISK_THRESHOLD:
#     decision = "BLOCK"

# Example in your Groq API call:
# model=LLM_MODEL

@app.post("/check-security")
def security_gateway(payload: dict):
    start_time = time.time()
    user_text = payload.get("text", "")

    if not user_text:
        return {"error": "No text provided"}

    rule_injection = detect_promptInjection(user_text)
    rule_jailbreak = detect_jailbreak(user_text)
    rule_total = rule_injection + rule_jailbreak

    try:
        llm_score_decimal = get_llm_security_score(user_text)
        llm_final_score = llm_score_decimal * 100
    except Exception:
        llm_final_score = 0 

    final_risk_score = max(rule_total, llm_final_score)

    pii_results = analyzer(user_text)

    status, final_result = decision(user_text, final_risk_score, pii_results)

    latency_ms = int((time.time() - start_time) * 1000)

    return {
        "status": status,
        "decision_result": final_result,
        "metadata": {
            "rule_score": rule_total / 100,
            "semantic_score": llm_final_score / 100,
        "final_risk": final_risk_score / 100,
        "latency_ms": latency_ms
        },
        "reason_codes": ["SEMANTIC_INJECTION"] if llm_final_score > 70 else []
    }