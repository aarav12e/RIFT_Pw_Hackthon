import os
import json
import urllib.request
import urllib.error

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def generate_clinical_explanation(drug, gene, phenotype, diplotype, risk_label, severity, detected_variants, recommendation, mechanism):
    variant_list = ", ".join([v.get("rsid", "unknown") for v in detected_variants]) if detected_variants else "No variants detected"

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

Return ONLY valid JSON with these exact fields:
{{
  "summary": "2-3 sentence clinical summary citing specific variants",
  "mechanism_explanation": "Molecular explanation of how {gene} variants affect {drug}",
  "patient_friendly": "Simple explanation for a patient without medical background",
  "clinical_significance": "Why this finding matters clinically",
  "monitoring_parameters": "Specific lab tests or parameters to monitor",
  "alternative_drugs": "Specific alternative medications if applicable"
}}"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1000}
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            GEMINI_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Strip markdown if present
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())

    except Exception as e:
        # Fallback if Gemini fails
        return {
            "summary": f"Patient with {gene} {phenotype} phenotype ({diplotype}) predicted to have {risk_label.lower()} response to {drug}. Detected variants: {variant_list}.",
            "mechanism_explanation": mechanism,
            "patient_friendly": f"Your genetic profile suggests {drug} may need adjustment based on your {gene} gene variants.",
            "clinical_significance": f"This {severity} severity finding requires clinical attention.",
            "monitoring_parameters": "Consult clinical pharmacist for gene-specific monitoring.",
            "alternative_drugs": recommendation,
            "error": str(e)
        }
