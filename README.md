# Robust Multilingual Security Gateway for LLM Applications

[cite_start]An enterprise-grade, multi-tier pre-model security gateway designed to intercept, analyze, and sanitize user prompts before they reach downstream Large Language Models (LLMs) [cite: 8-9]. [cite_start]The architecture implements a hybrid detection approach combining rule-based heuristics with deep semantic validation to insulate applications from advanced prompt injections, jailbreaks, system prompt extractions, and localized PII data leakage across English, Urdu, and Korean vectors [cite: 6-7, 10, 19-20].

---

## 🛠️ Core Capabilities & Architecture
- [cite_start]**Hybrid Injection Detection:** Dual-layer defense mechanism combining fast token rules with advanced deep semantic classification thresholds[cite: 7].
- [cite_start]**Multilingual Engineering:** Built-in pattern analyzers for English, Urdu, and Korean prompt structures [cite: 19-20, 86].
- [cite_start]**Customized Presidio Layer:** Localized entity filters detecting custom parameters such as Pakistani CNICs and Student Registration Numbers with bracket placeholders (`<CNIC>`, `<STUDENT_ID>`) [cite: 90, 94-96].
- [cite_start]**Configurable Control Plane:** Fully externalized thresholds loaded dynamically from `gateway_config.yaml` to decouple runtime security posture from code execution layers.

---

## 📂 Project Repository Structure
[cite_start]This gateway architecture maintains absolute logical isolation across individual components to guarantee strict reproducibility[cite: 164]:

```text
llm-security-gateway-final/
├── app/
│   └── main.py              # Central FastAPI application gateway router
├── detectors/               # Rule-based and semantic classification modules
├── pii/                     # Microsoft Presidio customization processors
├── policy/                  # Multi-variable defensive policy engine
├── config/
│   └── gateway_config.yaml  # Configurable risk and LLM model definitions
├── data/
│   └── final_eval.csv       # Automated output log tracking 200+ case records
├── results/
│   ├── json_logs/           # Auditable transaction payloads per test case
│   └── metrics_summary.json # Global systemic evaluation scores (Accuracy, F1)
├── test_dataset.json        # Comprehensive labeled multi-scenario test grid
├── evaluate_gateway.py      # Automated replication and latency evaluation script
└── requirements.txt         # Core environment configuration profile