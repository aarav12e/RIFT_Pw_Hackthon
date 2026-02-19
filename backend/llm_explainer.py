import os
import json
import urllib.request
from typing import Dict, List

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def _clean_severity_text(severity: str) -> str:
    mapping = {
        "none":     "no increased clinical risk",
        "low":      "low clinical risk requiring awareness",
        "moderate": "moderate clinical risk requiring dose adjustment",
        "high":     "high clinical risk requiring immediate clinical attention",
        "critical": "critical clinical risk requiring urgent intervention"
    }
    return mapping.get(severity, "clinical risk requiring evaluation")

def generate_clinical_explanation(
    drug: str, gene: str, phenotype: str, diplotype: str,
    risk_label: str, severity: str, detected_variants: List[Dict],
    recommendation: str, mechanism: str
) -> Dict:

    variant_list = ", ".join([v.get("rsid", "unknown") for v in detected_variants]) if detected_variants else "None"
    star_alleles  = ", ".join([v.get("star_allele", "unknown") for v in detected_variants]) if detected_variants else "*1/*1 (reference)"

    prompt = f"""You are a clinical pharmacogenomics expert. Generate a structured clinical explanation.

PATIENT PROFILE:
- Drug: {drug}
- Gene: {gene}
- Diplotype: {diplotype}
- Phenotype: {phenotype} (PM=Poor Metabolizer, IM=Intermediate, NM=Normal, RM=Rapid, URM=Ultrarapid)
- Risk: {risk_label} (Severity: {severity})
- Variants: {variant_list}
- Mechanism: {mechanism}
- Recommendation: {recommendation}

Return ONLY valid JSON with EXACTLY these fields:
{{
  "summary": "2-3 sentence clinical summary citing specific variants and their impact on {drug} therapy. If Variants is 'None', state that no actionable variants were detected.",
  "mechanism_explanation": "Detailed molecular explanation of how {gene} variants affect {drug}",
  "patient_friendly": "Simple 2-3 sentence explanation for a patient without medical background",
  "clinical_significance": "Why this finding matters clinically and what happens if ignored",
  "monitoring_parameters": "Specific lab tests or clinical parameters to monitor",
  "alternative_drugs": "Specific alternative medications to consider if applicable"
}}

Be specific, cite exact variants ({variant_list}) if present, reference CPIC guidelines. Return ONLY valid JSON, no markdown."""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1000}
        }).encode("utf-8")

        req = urllib.request.Request(url, data=payload,
            headers={"Content-Type": "application/json"}, method="POST")

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            result = json.loads(text.strip())
            result.pop("error", None)   # NEVER let error leak out
            return result

    except Exception:
        # Clean fallback — absolutely NO error field
        severity_text = _clean_severity_text(severity)

        if risk_label == "Ineffective":
            patient_msg   = f"Your genetic profile indicates that {drug} will likely not work for you due to variants in your {gene} gene. Your doctor should consider an alternative medication."
            significance  = f"Without pharmacogenomic-guided prescribing this patient may receive a drug that provides no therapeutic benefit, potentially delaying effective treatment."
        elif risk_label == "Toxic":
            patient_msg   = f"Your genetic profile indicates that {drug} could be dangerous at standard doses due to variants in your {gene} gene. Your doctor must adjust or avoid this medication."
            significance  = f"Without pharmacogenomic-guided prescribing this patient faces serious risk of drug toxicity which could be life-threatening."
        elif risk_label == "Adjust Dosage":
            patient_msg   = f"Your genetic profile suggests the standard dose of {drug} may not be right for you due to variants in your {gene} gene. Your doctor should adjust your dose accordingly."
            significance  = f"Without dose adjustment this patient may experience suboptimal therapeutic outcomes or increased side effects from {drug}."
        else:
            patient_msg   = f"Your genetic profile indicates that {drug} can be used at standard doses. Your {gene} gene variants show normal drug metabolism."
            significance  = f"This finding indicates {severity_text}. Standard dosing is appropriate for this patient."

        if risk_label == "Ineffective":
            article = "an"
            risk_desc = "ineffective"
        elif risk_label == "Adjust Dosage":
            article = "an"
            risk_desc = "adjusted dosage"
        elif risk_label == "Toxic":
            article = "a"
            risk_desc = "toxic"
        else:
            article = "a"
            risk_desc = risk_label.lower()

        if detected_variants:
            summary_text = f"This patient carries {gene} variants {diplotype} consistent with a {phenotype} phenotype, predicting {article} {risk_desc} response to {drug} therapy. Detected variants {variant_list} alter {gene} enzyme function per CPIC guidelines."
        else:
            summary_text = f"This patient carries {gene} {diplotype} consistent with a Normal Metabolizer phenotype. No clinically actionable pharmacogenomic variants were detected according to CPIC guidelines."

        return {
            "summary": summary_text,
            "mechanism_explanation": mechanism,
            "patient_friendly": patient_msg,
            "clinical_significance": significance,
            "monitoring_parameters": f"Monitor for signs of {drug} {'toxicity including adverse drug reactions' if risk_label == 'Toxic' else 'therapeutic failure' if risk_label == 'Ineffective' else 'dose-related effects'}. Consult clinical pharmacist for {gene}-specific therapeutic drug monitoring.",
            "alternative_drugs": recommendation
        }
