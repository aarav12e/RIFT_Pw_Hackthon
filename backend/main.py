from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import datetime
import time
import uvicorn
from typing import Optional

from vcf_parser import parse_vcf, extract_pharmacogenomic_variants, determine_phenotype, get_diplotype
from cpic_rules import GENE_DRUG_RULES, DRUG_TO_GENE
from llm_explainer import generate_clinical_explanation

app = FastAPI(title="PharmaGuard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "PharmaGuard API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze(
    vcf_file: UploadFile = File(...),
    drugs: str = Form(...)
):
    start_time = time.time()

    # Validate file type
    if not vcf_file.filename.endswith('.vcf'):
        raise HTTPException(status_code=400, detail="Only .vcf files are accepted")

    # Read file content
    try:
        content = await vcf_file.read()
        vcf_content = content.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read VCF file: {str(e)}")

    # Parse VCF
    parsed_vcf = parse_vcf(vcf_content)

    if not parsed_vcf["parse_success"] and parsed_vcf["total_variants"] == 0:
        raise HTTPException(status_code=400, detail="VCF file contains no parseable variants")

    patient_id = parsed_vcf["patient_id"]

    # Process each drug
    drug_list = [d.strip().upper() for d in drugs.split(',')]
    results = []

    for drug in drug_list:
        if drug not in GENE_DRUG_RULES:
            results.append({
                "drug": drug,
                "error": f"Drug '{drug}' not supported. Supported: {list(GENE_DRUG_RULES.keys())}",
                "patient_id": patient_id
            })
            continue

        rule = GENE_DRUG_RULES[drug]
        gene = rule["gene"]

        # Extract relevant variants
        pgx_variants = extract_pharmacogenomic_variants(parsed_vcf, gene)

        # Determine phenotype
        phenotype = determine_phenotype(pgx_variants, gene)

        # Get risk assessment
        phenotype_risks = rule["phenotype_risks"]
        risk_info = phenotype_risks.get(phenotype, phenotype_risks.get("NM"))

        # Get diplotype
        diplotype = get_diplotype(pgx_variants)

        # Generate LLM explanation
        llm_explanation = generate_clinical_explanation(
            drug=drug,
            gene=gene,
            phenotype=phenotype,
            diplotype=diplotype,
            risk_label=risk_info["risk_label"],
            severity=risk_info["severity"],
            detected_variants=pgx_variants,
            recommendation=risk_info["recommendation"],
            mechanism=risk_info["mechanism"]
        )

        processing_time = round(time.time() - start_time, 2)

        result = {
            "patient_id": patient_id,
            "drug": drug,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "risk_assessment": {
                "risk_label": risk_info["risk_label"],
                "confidence_score": risk_info["confidence_score"],
                "severity": risk_info["severity"]
            },
            "pharmacogenomic_profile": {
                "primary_gene": gene,
                "diplotype": diplotype,
                "phenotype": phenotype,
                "detected_variants": pgx_variants
            },
            "clinical_recommendation": {
                "action": risk_info["recommendation"],
                "cpic_guideline": f"CPIC Guideline for {drug} and {gene}",
                "mechanism": risk_info["mechanism"]
            },
            "llm_generated_explanation": llm_explanation,
            "quality_metrics": {
                "vcf_parsing_success": parsed_vcf["parse_success"],
                "total_variants_in_vcf": parsed_vcf["total_variants"],
                "pharmacogenomic_variants_found": len(pgx_variants),
                "processing_time_seconds": processing_time
            }
        }
        results.append(result)

    # Return single result or array
    if len(results) == 1:
        return JSONResponse(content=results[0])
    else:
        return JSONResponse(content={
            "patient_id": patient_id,
            "multi_drug_analysis": results,
            "total_drugs_analyzed": len(results),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        })


@app.get("/supported-drugs")
def supported_drugs():
    return {
        "drugs": list(GENE_DRUG_RULES.keys()),
        "genes": list(DRUG_TO_GENE.values())
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
