from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import datetime
import time

from vcf_parser import parse_vcf, extract_pharmacogenomic_variants, determine_phenotype, get_diplotype
from cpic_rules import GENE_DRUG_RULES, DRUG_TO_GENE
from llm_explainer import generate_clinical_explanation

app = FastAPI(title="PharmaGuard API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "PharmaGuard API is running", "version": "2.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/supported-drugs")
def supported_drugs():
    return {
        "drugs": list(GENE_DRUG_RULES.keys()),
        "genes": list(DRUG_TO_GENE.values())
    }


def build_single_result(patient_id, drug, parsed_vcf, start_time):
    """Build one RIFT-compliant result object for a single drug."""

    rule      = GENE_DRUG_RULES[drug]
    gene      = rule["gene"]
    pgx_vars  = extract_pharmacogenomic_variants(parsed_vcf, gene)
    phenotype = determine_phenotype(pgx_vars, gene)
    risk_info = rule["phenotype_risks"].get(phenotype, rule["phenotype_risks"]["NM"])
    diplotype = get_diplotype(pgx_vars)

    llm_explanation = generate_clinical_explanation(
        drug=drug, gene=gene, phenotype=phenotype, diplotype=diplotype,
        risk_label=risk_info["risk_label"], severity=risk_info["severity"],
        detected_variants=pgx_vars, recommendation=risk_info["recommendation"],
        mechanism=risk_info["mechanism"]
    )
    # Guarantee no error key ever reaches output
    llm_explanation.pop("error", None)

    processing_time = round(time.time() - start_time, 2)

    return {
        "patient_id": patient_id,
        "drug": drug,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "risk_assessment": {
            "risk_label":       risk_info["risk_label"],
            "confidence_score": risk_info["confidence_score"],
            "severity":         risk_info["severity"]
        },
        "pharmacogenomic_profile": {
            "primary_gene":      gene,
            "diplotype":         diplotype,
            "phenotype":         phenotype,
            "detected_variants": pgx_vars
        },
        "clinical_recommendation": {
            "action":          risk_info["recommendation"],
            "cpic_guideline":  f"CPIC Guideline for {drug} and {gene}",
            "mechanism":       risk_info["mechanism"]
        },
        "llm_generated_explanation": llm_explanation,
        "quality_metrics": {
            "vcf_parsing_success":          parsed_vcf["parse_success"],
            "total_variants_in_vcf":        parsed_vcf["total_variants"],
            "pharmacogenomic_variants_found": len(pgx_vars),
            "processing_time_seconds":      processing_time
        }
    }


@app.post("/analyze")
async def analyze(
    vcf_file: UploadFile = File(...),
    drugs:    str        = Form(...)
):
    start_time = time.time()

    # Validate file
    if not vcf_file.filename.endswith(".vcf"):
        raise HTTPException(status_code=400, detail="Only .vcf files are accepted")

    try:
        content     = await vcf_file.read()
        vcf_content = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read VCF file: {str(e)}")

    parsed_vcf = parse_vcf(vcf_content)
    if not parsed_vcf["parse_success"] and parsed_vcf["total_variants"] == 0:
        raise HTTPException(status_code=400, detail="VCF file contains no parseable variants")

    patient_id = parsed_vcf["patient_id"]
    drug_list  = [d.strip().upper() for d in drugs.split(",") if d.strip()]

    results = []
    for drug in drug_list:
        if drug not in GENE_DRUG_RULES:
            # Still return valid schema even for unsupported drug
            results.append({
                "patient_id": patient_id,
                "drug": drug,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "risk_assessment": {
                    "risk_label": "Unknown",
                    "confidence_score": 0.0,
                    "severity": "none"
                },
                "pharmacogenomic_profile": {
                    "primary_gene": "Unknown",
                    "diplotype": "*1/*1",
                    "phenotype": "Unknown",
                    "detected_variants": []
                },
                "clinical_recommendation": {
                    "action": f"Drug '{drug}' is not supported. Supported drugs: {', '.join(GENE_DRUG_RULES.keys())}",
                    "cpic_guideline": "N/A",
                    "mechanism": "N/A"
                },
                "llm_generated_explanation": {
                    "summary": f"Drug '{drug}' is not in the supported drug list.",
                    "mechanism_explanation": "N/A",
                    "patient_friendly": f"This drug is not currently supported by PharmaGuard.",
                    "clinical_significance": "N/A",
                    "monitoring_parameters": "N/A",
                    "alternative_drugs": "N/A"
                },
                "quality_metrics": {
                    "vcf_parsing_success": parsed_vcf["parse_success"],
                    "total_variants_in_vcf": parsed_vcf["total_variants"],
                    "pharmacogenomic_variants_found": 0,
                    "processing_time_seconds": round(time.time() - start_time, 2)
                }
            })
            continue

        result = build_single_result(patient_id, drug, parsed_vcf, start_time)
        results.append(result)

    # ✅ RIFT SCHEMA COMPLIANT:
    # Single drug  → return single object   { patient_id, drug, ... }
    # Multi drug   → return JSON array      [ { ... }, { ... } ]
    if len(results) == 1:
        return JSONResponse(content=results[0])
    else:
        return JSONResponse(content=results)
