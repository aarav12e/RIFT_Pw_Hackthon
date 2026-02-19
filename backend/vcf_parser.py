import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class VCFVariant:
    chrom: str
    pos: int
    rsid: str
    ref: str
    alt: str
    gene: Optional[str] = None
    star_allele: Optional[str] = None
    genotype: Optional[str] = None

def parse_vcf(content: str) -> Dict:
    """
    Parse VCF file content and extract pharmacogenomic variants.
    Returns structured data with variants, patient ID, and metadata.
    """
    lines = content.strip().split('\n')
    variants = []
    patient_id = "PATIENT_UNKNOWN"
    metadata = {}

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Parse metadata headers
        if line.startswith('##'):
            if 'patient_id' in line.lower() or 'sample' in line.lower():
                match = re.search(r'=([A-Za-z0-9_\-]+)', line)
                if match:
                    patient_id = match.group(1)
            continue

        # Parse column header
        if line.startswith('#CHROM'):
            cols = line.lstrip('#').split('\t')
            if len(cols) > 8:
                # Sample name is usually the last column
                patient_id = cols[-1] if cols[-1] not in ['FORMAT', 'SAMPLE'] else patient_id
            continue

        # Parse variant lines
        if not line.startswith('#'):
            parts = line.split('\t')
            if len(parts) < 5:
                continue

            chrom = parts[0]
            pos = int(parts[1]) if parts[1].isdigit() else 0
            rsid = parts[2] if parts[2] != '.' else f"pos_{pos}"
            ref = parts[3]
            alt = parts[4]

            # Extract gene from INFO field
            gene = None
            star_allele = None
            genotype = None

            if len(parts) > 7:
                info = parts[7]
                gene_match = re.search(r'GENE=([^;]+)', info)
                if gene_match:
                    gene = gene_match.group(1)

                star_match = re.search(r'STAR=([^;]+)', info)
                if star_match:
                    star_allele = star_match.group(1)

            # Extract genotype from FORMAT/SAMPLE columns
            if len(parts) > 9:
                fmt = parts[8].split(':')
                smp = parts[9].split(':')
                fmt_dict = dict(zip(fmt, smp))
                genotype = fmt_dict.get('GT', None)
            elif len(parts) > 8:
                genotype = parts[8] if '/' in parts[8] or '|' in parts[8] else None

            variant = VCFVariant(
                chrom=chrom,
                pos=pos,
                rsid=rsid.lower() if rsid.startswith('RS') else rsid,
                ref=ref,
                alt=alt,
                gene=gene,
                star_allele=star_allele,
                genotype=genotype
            )
            variants.append(variant)

    return {
        "patient_id": patient_id,
        "total_variants": len(variants),
        "variants": variants,
        "metadata": metadata,
        "parse_success": len(variants) > 0
    }


def extract_pharmacogenomic_variants(parsed_vcf: Dict, target_gene: str) -> List[Dict]:
    """
    Filter VCF variants to only those relevant to the target gene.
    Cross-references with known pharmacogenomic rsIDs.
    """
    from cpic_rules import VARIANT_STAR_ALLELES

    variants = parsed_vcf.get("variants", [])
    pgx_variants = []

    seen_rsids = set()
    unique_pgx_variants = []

    for v in variants:
        rsid_lower = v.rsid.lower()
        if rsid_lower in seen_rsids:
            continue
            
        # CRITICAL FIX: skip if genotype is homozygous reference (0/0) or missing
        # We only care about variants that are actually present
        if v.genotype in ["0/0", "0|0", "./.", ".|.", ".", None]:
            continue

        # Check by rsID in known database
        if rsid_lower in VARIANT_STAR_ALLELES:
            info = VARIANT_STAR_ALLELES[rsid_lower]
            if info["gene"] == target_gene:
                seen_rsids.add(rsid_lower)
                unique_pgx_variants.append({
                    "rsid": v.rsid,
                    "chromosome": v.chrom,
                    "position": v.pos,
                    "ref_allele": v.ref,
                    "alt_allele": v.alt,
                    "gene": info["gene"],
                    "star_allele": info["star_allele"],
                    "function_status": info["function"],
                    "activity_score": info.get("activity_score", 0), # Default to 0 if not found for PGx variants
                    "genotype": v.genotype or "unknown"
                })
        # Also check by gene annotation in VCF
        elif v.gene == target_gene and v.rsid != f"pos_{v.pos}":
            seen_rsids.add(rsid_lower)
            unique_pgx_variants.append({
                "rsid": v.rsid,
                "chromosome": v.chrom,
                "position": v.pos,
                "ref_allele": v.ref,
                "alt_allele": v.alt,
                "gene": target_gene,
                "star_allele": v.star_allele or "unknown",
                "function_status": "unknown",
                "activity_score": 0,
                "genotype": v.genotype or "unknown"
            })

    return unique_pgx_variants


def determine_phenotype(variants: List[Dict], gene: str) -> str:
    """
    Determine phenotype (PM/IM/NM/RM/URM) based on detected variants.
    Uses diplotype logic based on CPIC guidelines.
    """
    if not variants:
        return "NM"  # Default: Normal Metabolizer if no variants found

    # Activity Score Logic (CPIC Standard)
    # Default alleles: *1/*1 (Score 1.0 + 1.0 = 2.0)
    allele_scores = [1.0, 1.0] 

    if len(variants) == 1:
        # One variant detected.
        v = variants[0]
        score = v.get("activity_score", 1.0) # Default to 1 if unknown, but usually 0 for variants in our list
        
        # Check zygosity
        gt = v.get("genotype", "")
        if gt in ["1/1", "1|1"]:
            # Homozygous for the variant: *Var/*Var
            allele_scores = [score, score]
        else:
            # Heterozygous: *1/*Var
            allele_scores = [1.0, score]

    elif len(variants) >= 2:
        # Two or more variants. 
        # Simplified: Take the top 2 impacted alleles (lowest scores) to be conservative, 
        # or assume compound heterozygosity for the first two found.
        # Strict logic: *A/*B
        v1 = variants[0]
        v2 = variants[1]
        score1 = v1.get("activity_score", 1.0)
        score2 = v2.get("activity_score", 1.0)
        allele_scores = [score1, score2]

    total_activity_score = sum(allele_scores)

    # Phenotype Mapping based on Total Activity Score
    # >= 1.5 -> NM (Normal Metabolizer)
    # 1.0   -> IM (Intermediate Metabolizer)
    # <= 0.5 -> PM (Poor Metabolizer)
    
    if total_activity_score >= 1.5:
        return "NM"
    elif total_activity_score >= 1.0:
        return "IM"
    else:
        return "PM"


def get_diplotype(variants: List[Dict]) -> str:
    """Build diplotype string from detected variants."""
    if not variants:
        return "*1/*1"
    star_alleles = [v.get("star_allele", "*1") for v in variants[:2]]
    if len(star_alleles) == 1:
        star_alleles.append("*1")
    return f"{star_alleles[0]}/{star_alleles[1]}"
