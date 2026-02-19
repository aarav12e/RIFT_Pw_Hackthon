import os
import json
import google.generativeai as genai
from typing import Dict, List

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

def generate_clinical_explanation(
    drug: str,
    gene: str,
    phenotype: str,
    diplotype: str,
    risk_label: str,
    severity: str,
    detected_variants: List[Dict],
    recommendation: str,
    mechanism: str
) -> Dict:
    """
    Generate LLM-powered clinical explanation using Google Gemini.
    Returns structured explanation with summary, mechanism, and patient-friendly text.
    """
    variant_list = ", ".join([v.get("rsid", "unknown") for v in detected_variants]) if detected_variants else "No pharmacogenomic variants detected"
    star_alleles = ", ".join([v.get("star_allele", "unknown") for v in detected_variants]) if detected_variants else "*1/*1 (reference)"

    prompt = f"""You are a clinical pharmacogenomics expert. Generate a structured clinical explanation for the following patient case.

PATIENT PHARMACOGENOMIC PROFILE:
- Drug: {drug}
- Primary Gene: {gene}
- Diplotype: {diplotype}
- Phenotype: {phenotype} (PM=Poor Metabolizer, IM=Intermediate, NM=Normal, RM=Rapid, URM=Ultrarapid)
- Risk Assessment: {risk_label} (Severity: {severity})
- Detected Variants: {variant_list}
- Star Alleles: {star_alleles}
- Biological Mechanism: {mechanism}
- Clinical Recommendation: {recommendation}

Generate a JSON response with EXACTLY these fields:
{{
  "summary": "2-3 sentence clinical summary citing specific variants and their impact on {drug} therapy",
  "mechanism_explanation": "Detailed explanation of how {gene} variants affect {drug} metabolism/transport at molecular level",
  "patient_friendly": "Simple 2-3 sentence explanation for a patient without medical background",
  "clinical_significance": "Why this finding matters clinically and what happens if ignored",
  "monitoring_parameters": "Specific lab tests or clinical parameters to monitor",
  "alternative_drugs": "Specific alternative medications to consider if applicable"
}}

Be specific, cite the exact variants ({variant_list}), and reference CPIC guidelines. Return ONLY valid JSON."""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean markdown code blocks if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        if text.endswith("```"):
            text = text[:-3]

        parsed = json.loads(text.strip())
        return parsed

    except Exception as e:
        # Fallback if Gemini fails
        return {
            "summary": f"Patient with {gene} {phenotype} phenotype (diplotype: {diplotype}) is predicted to have {risk_label.lower()} response to {drug}. Detected variants: {variant_list}.",
            "mechanism_explanation": mechanism,
            "patient_friendly": f"Your genetic profile suggests that {drug} may {'not work as expected' if risk_label == 'Ineffective' else 'cause side effects' if risk_label == 'Toxic' else 'need dose adjustment'} for you based on your {gene} gene variants.",
            "clinical_significance": f"This {severity} severity finding requires {'immediate attention and drug change' if severity in ['critical', 'high'] else 'dose adjustment consideration'}.",
            "monitoring_parameters": "Consult your clinical pharmacist for gene-specific monitoring recommendations.",
            "alternative_drugs": recommendation,
            "error": str(e)
        }


def generate_mock_explanation(drug: str, gene: str, phenotype: str, risk_label: str) -> Dict:
    """Fallback mock explanation when API is unavailable."""
    return {
        "summary": f"This patient carries {gene} variants consistent with a {phenotype} phenotype, predicting a {risk_label.lower()} response to {drug} therapy.",
        "mechanism_explanation": f"The {gene} gene encodes a key enzyme/transporter involved in {drug} metabolism. Variants alter protein function, changing drug plasma levels.",
        "patient_friendly": f"Your DNA test shows your body processes {drug} differently than average, which means your doctor may need to adjust your treatment.",
        "clinical_significance": f"Without pharmacogenomic-guided dosing, this patient faces elevated risk of therapeutic failure or adverse drug reactions.",
        "monitoring_parameters": "Complete blood count, liver function tests, and therapeutic drug monitoring as clinically indicated.",
        "alternative_drugs": "Consult with a clinical pharmacist for CPIC-recommended alternatives."
    }
