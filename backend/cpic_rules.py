# CPIC Guidelines - Gene-Drug-Phenotype-Risk Mappings
# Based on CPIC clinical guidelines (cpicpgx.org)

GENE_DRUG_RULES = {
    "CODEINE": {
        "gene": "CYP2D6",
        "phenotype_risks": {
            "URM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "confidence_score": 0.95,
                "recommendation": "Avoid codeine. Ultrarapid metabolism leads to excessive morphine production causing respiratory depression and potential death. Use alternative analgesic such as morphine (with care) or a non-opioid.",
                "mechanism": "CYP2D6 ultrarapid metabolizers convert codeine to morphine too rapidly, causing toxic morphine plasma levels."
            },
            "PM": {
                "risk_label": "Ineffective",
                "severity": "high",
                "confidence_score": 0.92,
                "recommendation": "Avoid codeine. Poor metabolizers cannot convert codeine to its active form morphine, resulting in no analgesic effect. Use an alternative non-CYP2D6-dependent opioid.",
                "mechanism": "CYP2D6 poor metabolizers lack the enzyme activity to O-demethylate codeine to morphine, producing no analgesic effect."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "moderate",
                "confidence_score": 0.80,
                "recommendation": "Use with caution. Reduced analgesic effect expected. Consider lower dose or alternative analgesic.",
                "mechanism": "Reduced CYP2D6 activity leads to decreased morphine production from codeine."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.90,
                "recommendation": "Standard dosing applies. Monitor for expected analgesic effect.",
                "mechanism": "Normal CYP2D6 activity provides expected codeine to morphine conversion."
            },
            "RM": {
                "risk_label": "Adjust Dosage",
                "severity": "low",
                "confidence_score": 0.75,
                "recommendation": "Use with caution. Slightly increased morphine production possible. Monitor for opioid side effects.",
                "mechanism": "Mildly increased CYP2D6 activity may produce elevated morphine levels."
            }
        }
    },
    "WARFARIN": {
        "gene": "CYP2C9",
        "phenotype_risks": {
            "PM": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "confidence_score": 0.93,
                "recommendation": "Reduce warfarin dose by 50-75%. Poor metabolizers have significantly reduced warfarin clearance, leading to elevated plasma levels and bleeding risk. Monitor INR closely.",
                "mechanism": "CYP2C9 poor metabolizers have severely impaired warfarin S-enantiomer metabolism, prolonging anticoagulant effect."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "moderate",
                "confidence_score": 0.85,
                "recommendation": "Reduce warfarin starting dose by 25-50%. Monitor INR more frequently during initiation.",
                "mechanism": "Intermediate CYP2C9 activity reduces warfarin clearance, requiring lower doses to achieve target INR."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.88,
                "recommendation": "Standard dosing and monitoring apply.",
                "mechanism": "Normal CYP2C9 activity provides expected warfarin metabolism."
            },
            "URM": {
                "risk_label": "Adjust Dosage",
                "severity": "low",
                "confidence_score": 0.70,
                "recommendation": "May require higher warfarin doses to achieve therapeutic INR. Monitor closely.",
                "mechanism": "Increased CYP2C9 activity leads to faster warfarin clearance."
            },
            "RM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.78,
                "recommendation": "Standard dosing with routine monitoring.",
                "mechanism": "Near-normal warfarin metabolism expected."
            }
        }
    },
    "CLOPIDOGREL": {
        "gene": "CYP2C19",
        "phenotype_risks": {
            "PM": {
                "risk_label": "Ineffective",
                "severity": "critical",
                "confidence_score": 0.95,
                "recommendation": "Avoid clopidogrel. Poor metabolizers cannot activate the prodrug, resulting in no antiplatelet effect. Use prasugrel or ticagrelor as alternatives.",
                "mechanism": "CYP2C19 poor metabolizers cannot convert clopidogrel to its active thiol metabolite, resulting in absent platelet inhibition and increased cardiovascular event risk."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "moderate",
                "confidence_score": 0.82,
                "recommendation": "Consider alternative antiplatelet agent (prasugrel or ticagrelor). If clopidogrel must be used, higher dose monitoring required.",
                "mechanism": "Reduced CYP2C19 activity leads to decreased active metabolite formation and suboptimal platelet inhibition."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.90,
                "recommendation": "Standard clopidogrel dosing recommended.",
                "mechanism": "Normal CYP2C19 activity provides adequate clopidogrel activation."
            },
            "RM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.85,
                "recommendation": "Standard dosing. Enhanced drug activation may provide good antiplatelet effect.",
                "mechanism": "Increased CYP2C19 activity leads to enhanced clopidogrel activation."
            },
            "URM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.80,
                "recommendation": "Standard dosing with good expected response.",
                "mechanism": "Ultrarapid CYP2C19 activity provides robust clopidogrel activation."
            }
        }
    },
    "SIMVASTATIN": {
        "gene": "SLCO1B1",
        "phenotype_risks": {
            "PM": {
                "risk_label": "Toxic",
                "severity": "high",
                "confidence_score": 0.91,
                "recommendation": "Avoid simvastatin 40-80mg doses. High risk of simvastatin-induced myopathy. Use lower dose (10-20mg) or switch to pravastatin or rosuvastatin.",
                "mechanism": "SLCO1B1 poor function leads to reduced hepatic uptake of simvastatin, increasing plasma concentrations and myopathy risk."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "moderate",
                "confidence_score": 0.83,
                "recommendation": "Use lower simvastatin dose (20-40mg max) or consider alternative statin. Monitor for muscle symptoms (myalgia, CK elevation).",
                "mechanism": "Decreased SLCO1B1 transporter activity leads to elevated simvastatin plasma levels."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.87,
                "recommendation": "Standard simvastatin dosing. Routine monitoring recommended.",
                "mechanism": "Normal SLCO1B1 function provides adequate hepatic simvastatin uptake."
            },
            "URM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.75,
                "recommendation": "Standard or potentially higher doses may be needed for therapeutic effect.",
                "mechanism": "Enhanced SLCO1B1 activity increases hepatic uptake, potentially reducing systemic exposure."
            },
            "RM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.80,
                "recommendation": "Standard dosing recommended.",
                "mechanism": "Normal to enhanced SLCO1B1 function."
            }
        }
    },
    "AZATHIOPRINE": {
        "gene": "TPMT",
        "phenotype_risks": {
            "PM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "confidence_score": 0.96,
                "recommendation": "CONTRAINDICATED at standard doses. TPMT-deficient patients accumulate toxic thioguanine nucleotides causing life-threatening bone marrow suppression. Reduce dose by 90% or use alternative agent.",
                "mechanism": "Absent TPMT activity causes accumulation of cytotoxic thioguanine nucleotides, leading to severe myelosuppression."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "confidence_score": 0.89,
                "recommendation": "Reduce azathioprine dose by 30-70%. Monitor CBC weekly for first month, then monthly. Watch for signs of myelosuppression.",
                "mechanism": "Reduced TPMT activity leads to accumulation of thioguanine nucleotides above therapeutic levels."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.91,
                "recommendation": "Standard azathioprine dosing with routine CBC monitoring.",
                "mechanism": "Normal TPMT activity maintains thioguanine nucleotides within therapeutic range."
            },
            "RM": {
                "risk_label": "Adjust Dosage",
                "severity": "low",
                "confidence_score": 0.70,
                "recommendation": "May require higher doses for therapeutic effect. Monitor thiopurine metabolite levels.",
                "mechanism": "Increased TPMT activity leads to reduced thioguanine nucleotide accumulation."
            },
            "URM": {
                "risk_label": "Ineffective",
                "severity": "moderate",
                "confidence_score": 0.72,
                "recommendation": "Standard doses may be insufficient. Consider alternative immunosuppressant or monitor drug metabolite levels closely.",
                "mechanism": "Very high TPMT activity rapidly clears thioguanine nucleotides, potentially reducing therapeutic efficacy."
            }
        }
    },
    "FLUOROURACIL": {
        "gene": "DPYD",
        "phenotype_risks": {
            "PM": {
                "risk_label": "Toxic",
                "severity": "critical",
                "confidence_score": 0.97,
                "recommendation": "CONTRAINDICATED. DPYD-deficient patients cannot metabolize fluorouracil, leading to severe and potentially fatal toxicity (mucositis, neutropenia, neurotoxicity). Avoid completely or reduce dose by 50-85% with therapeutic drug monitoring.",
                "mechanism": "Absent DPYD activity prevents catabolism of fluorouracil, causing massive drug accumulation and life-threatening systemic toxicity."
            },
            "IM": {
                "risk_label": "Adjust Dosage",
                "severity": "high",
                "confidence_score": 0.90,
                "recommendation": "Reduce fluorouracil starting dose by 25-50%. Begin at lower dose and titrate based on tolerability and drug levels. Requires close monitoring.",
                "mechanism": "Partial DPYD deficiency reduces fluorouracil catabolism, elevating exposure and toxicity risk."
            },
            "NM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.89,
                "recommendation": "Standard fluorouracil dosing. Routine toxicity monitoring recommended.",
                "mechanism": "Normal DPYD activity provides expected fluorouracil catabolism."
            },
            "RM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.80,
                "recommendation": "Standard dosing. Slightly enhanced drug clearance may occur.",
                "mechanism": "Near-normal DPYD function with adequate fluorouracil metabolism."
            },
            "URM": {
                "risk_label": "Safe",
                "severity": "none",
                "confidence_score": 0.75,
                "recommendation": "Standard dosing. May require higher doses for full therapeutic effect in some cases.",
                "mechanism": "Enhanced DPYD activity may increase fluorouracil catabolism slightly."
            }
        }
    }
}

# Variant to Star Allele mapping (rsID -> functional impact)
VARIANT_STAR_ALLELES = {
    # CYP2D6
    "rs3892097": {"gene": "CYP2D6", "star_allele": "*4", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs35742686": {"gene": "CYP2D6", "star_allele": "*3", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs5030655": {"gene": "CYP2D6", "star_allele": "*6", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs16947": {"gene": "CYP2D6", "star_allele": "*2", "function": "normal_function", "activity_score": 1, "phenotype_contribution": "NM"},
    "rs28371725": {"gene": "CYP2D6", "star_allele": "*41", "function": "decreased_function", "activity_score": 0.5, "phenotype_contribution": "IM"},
    "rs1065852": {"gene": "CYP2D6", "star_allele": "*10", "function": "decreased_function", "activity_score": 0.5, "phenotype_contribution": "IM"},
    # CYP2C19
    "rs4244285": {"gene": "CYP2C19", "star_allele": "*2", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs4986893": {"gene": "CYP2C19", "star_allele": "*3", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs12248560": {"gene": "CYP2C19", "star_allele": "*17", "function": "increased_function", "activity_score": 1, "phenotype_contribution": "RM"}, # Technically increased, but often treated as 1+
    "rs28399504": {"gene": "CYP2C19", "star_allele": "*4", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    # CYP2C9
    "rs1799853": {"gene": "CYP2C9", "star_allele": "*2", "function": "decreased_function", "activity_score": 0.5, "phenotype_contribution": "IM"},
    "rs1057910": {"gene": "CYP2C9", "star_allele": "*3", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs28371686": {"gene": "CYP2C9", "star_allele": "*5", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    # SLCO1B1
    "rs4149056": {"gene": "SLCO1B1", "star_allele": "*5", "function": "decreased_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs2306283": {"gene": "SLCO1B1", "star_allele": "*1b", "function": "increased_function", "activity_score": 1, "phenotype_contribution": "RM"},
    "rs11045819": {"gene": "SLCO1B1", "star_allele": "*14", "function": "decreased_function", "activity_score": 0.5, "phenotype_contribution": "IM"},
    # TPMT
    "rs1800460": {"gene": "TPMT", "star_allele": "*3B", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs1142345": {"gene": "TPMT", "star_allele": "*3C", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs1800462": {"gene": "TPMT", "star_allele": "*2", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    # DPYD
    "rs3918290": {"gene": "DPYD", "star_allele": "*2A", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs55886062": {"gene": "DPYD", "star_allele": "*13", "function": "no_function", "activity_score": 0, "phenotype_contribution": "PM"},
    "rs67376798": {"gene": "DPYD", "star_allele": "c.2846A>T", "function": "decreased_function", "activity_score": 0.5, "phenotype_contribution": "IM"},
    "rs75017182": {"gene": "DPYD", "star_allele": "HapB3", "function": "decreased_function", "activity_score": 0.5, "phenotype_contribution": "IM"},
}

GENE_TO_DRUG = {
    "CYP2D6": "CODEINE",
    "CYP2C19": "CLOPIDOGREL",
    "CYP2C9": "WARFARIN",
    "SLCO1B1": "SIMVASTATIN",
    "TPMT": "AZATHIOPRINE",
    "DPYD": "FLUOROURACIL"
}

DRUG_TO_GENE = {v: k for k, v in GENE_TO_DRUG.items()}
