# 🧬 PharmaGuard — Pharmacogenomic Risk Prediction System

> AI-powered web application that analyzes patient genetic data (VCF files) and predicts personalized drug risks using CPIC guidelines + Google Gemini AI explanations.

---

## 🔗 Important Links

| | Link |
|---|---|
| 🌐 **Live Demo** | `https://your-app.vercel.app` *(update this)* |
| 🎥 **LinkedIn Video** | `https://linkedin.com/posts/your-video` *(update this)* |
| 💻 **GitHub Repo** | `https://github.com/yourusername/pharmaguard` *(update this)* |
| 🔧 **Backend API** | `https://your-api.onrender.com` *(update this)* |

---

## 🏥 Problem Statement

Adverse drug reactions kill over **100,000 Americans annually**. Many of these deaths are preventable through pharmacogenomic testing — analyzing how a patient's genetic variants affect drug metabolism.

**PharmaGuard** solves this by:
- Parsing real VCF (Variant Call Format) genetic files
- Identifying pharmacogenomic variants across 6 critical genes
- Predicting drug-specific risks: Safe, Adjust Dosage, Toxic, or Ineffective
- Generating clinically actionable AI explanations using Google Gemini
- Aligning all recommendations with **CPIC (Clinical Pharmacogenomics Implementation Consortium)** guidelines

---

## 🏗 Architecture Overview

```
User (Browser)
      │
      ▼
React Frontend (Vercel)
      │  POST /analyze
      │  multipart/form-data: VCF file + drug names
      ▼
FastAPI Backend (Render)
      │
      ├── VCF Parser
      │     └── Extracts rsIDs, gene annotations, genotypes
      │
      ├── CPIC Rules Engine
      │     └── Maps variants → star alleles → phenotype (PM/IM/NM/RM/URM)
      │
      ├── Risk Predictor
      │     └── Phenotype + Drug → Risk Label + Severity + Confidence
      │
      └── Gemini AI (via HTTP)
            └── Generates clinical explanation with variant citations
      │
      ▼
Structured JSON Response
      │
      ▼
React UI — Color-coded results, confidence gauge, downloadable JSON
```

---

## 🧬 Supported Genes & Drugs

| Drug | Gene | Risk if Variant Present |
|---|---|---|
| CODEINE | CYP2D6 | Respiratory depression (URM) / No effect (PM) |
| WARFARIN | CYP2C9 | Dangerous bleeding risk (PM) |
| CLOPIDOGREL | CYP2C19 | Heart attack risk — cannot activate prodrug (PM) |
| SIMVASTATIN | SLCO1B1 | Muscle damage / myopathy (PM) |
| AZATHIOPRINE | TPMT | Fatal bone marrow toxicity (PM) |
| FLUOROURACIL | DPYD | Life-threatening systemic toxicity (PM) |

### Phenotype Classification

| Code | Phenotype | Meaning |
|---|---|---|
| PM | Poor Metabolizer | Drug builds up — risk of toxicity |
| IM | Intermediate Metabolizer | Reduced drug processing |
| NM | Normal Metabolizer | Standard dose is appropriate |
| RM | Rapid Metabolizer | Faster drug clearance |
| URM | Ultrarapid Metabolizer | Drug clears too fast — may be ineffective or toxic |

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn |
| AI/LLM | Google Gemini 1.5 Flash (via direct HTTP) |
| VCF Parsing | Custom Python parser (VCFv4.2 compliant) |
| CPIC Rules | Hardcoded CPIC guideline mappings |
| Deployment | Vercel (frontend) + Render (backend) |
| Uptime | cron-job.org keep-alive ping every 10 minutes |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/pharmaguard.git
cd pharmaguard/backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Add your GEMINI_API_KEY inside .env

# Start backend server
uvicorn main:app --reload --port 8000
# Runs at http://localhost:8000
```

### Frontend Setup

```bash
cd pharmaguard/frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
# Runs at http://localhost:5173
```

---

## 📋 API Documentation

### `POST /analyze`

Analyzes a VCF file for pharmacogenomic drug interactions.

**Request:** `multipart/form-data`

| Field | Type | Description |
|---|---|---|
| `vcf_file` | File | `.vcf` file, max 5MB |
| `drugs` | String | Comma-separated drug names e.g. `CODEINE,WARFARIN` |

**Supported drugs:** `CODEINE`, `WARFARIN`, `CLOPIDOGREL`, `SIMVASTATIN`, `AZATHIOPRINE`, `FLUOROURACIL`

**Response:**

```json
{
  "patient_id": "PATIENT_001",
  "drug": "CODEINE",
  "timestamp": "2026-02-19T12:00:00Z",
  "risk_assessment": {
    "risk_label": "Toxic",
    "confidence_score": 0.95,
    "severity": "critical"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2D6",
    "diplotype": "*4/*3",
    "phenotype": "PM",
    "detected_variants": [
      {
        "rsid": "rs3892097",
        "star_allele": "*4",
        "function_status": "no_function",
        "genotype": "1|1"
      }
    ]
  },
  "clinical_recommendation": {
    "action": "Avoid codeine. Use alternative analgesic.",
    "cpic_guideline": "CPIC Guideline for CODEINE and CYP2D6",
    "mechanism": "CYP2D6 poor metabolizers cannot convert codeine to morphine."
  },
  "llm_generated_explanation": {
    "summary": "...",
    "mechanism_explanation": "...",
    "patient_friendly": "...",
    "clinical_significance": "...",
    "monitoring_parameters": "...",
    "alternative_drugs": "..."
  },
  "quality_metrics": {
    "vcf_parsing_success": true,
    "total_variants_in_vcf": 8,
    "pharmacogenomic_variants_found": 2,
    "processing_time_seconds": 3.2
  }
}
```

### `GET /health`

Health check endpoint.

```json
{ "status": "healthy" }
```

### `GET /supported-drugs`

Returns list of supported drugs and genes.

```json
{
  "drugs": ["CODEINE", "WARFARIN", "CLOPIDOGREL", "SIMVASTATIN", "AZATHIOPRINE", "FLUOROURACIL"],
  "genes": ["CYP2D6", "CYP2C9", "CYP2C19", "SLCO1B1", "TPMT", "DPYD"]
}
```

---

## 🧪 Usage Examples

### Testing with Sample VCF Files

| VCF File | Drug to Select | Expected Result |
|---|---|---|
| `patient_001_test.vcf` | CODEINE | ☠️ Toxic (CYP2D6 PM) |
| `patient_002_dpyd_pm.vcf` | FLUOROURACIL | ☠️ Toxic / Critical |
| Normal patient VCF | Any drug | ✅ Safe |

### Quick Demo Flow (for judges)

1. Open the live URL
2. Click **"🔴 Critical"** sample button (auto-loads Fluorouracil test case)
3. Click **"Analyze 1 Drug →"**
4. See critical red result with AI explanation
5. Click **"↓ Download JSON"** to show output schema compliance

---

## ⚠️ Known Limitations

- Only 6 genes and 6 drugs supported (per RIFT specification)
- Phenotype prediction uses simplified diplotype logic — does not implement full CYP2D6 Activity Score method
- VCF parser handles standard VCFv4.2 format; exotic formats may need preprocessing
- LLM explanations require valid Gemini API key; falls back to rule-based text if API unavailable
- CYP2D6 copy number variations (gene duplications) not implemented
- Not validated for clinical use — research and educational purposes only

---

## 👥 Team Members

| Name | Role |
|---|---|
| *(Add your name)* | Full Stack + AI |
| *(Add teammate)* | Frontend |
| *(Add teammate)* | Backend |

---

## 📄 Disclaimer

> PharmaGuard is built for the RIFT 2026 Hackathon. It is intended for **research and educational purposes only** and is **not validated for clinical diagnosis or treatment decisions**. Always consult a qualified healthcare professional for medical advice.

---

*Built with ❤️ for RIFT 2026 Hackathon — HealthTech / Pharmacogenomics Track*