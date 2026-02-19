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

    for v in variants:
        rsid_lower = v.rsid.lower()
        # Check by rsID in known database
        if rsid_lower in VARIANT_STAR_ALLELES:
            info = VARIANT_STAR_ALLELES[rsid_lower]
            if info["gene"] == target_gene:
                pgx_variants.append({
                    "rsid": v.rsid,
                    "chromosome": v.chrom,
                    "position": v.pos,
                    "ref_allele": v.ref,
                    "alt_allele": v.alt,
                    "gene": info["gene"],
                    "star_allele": info["star_allele"],
                    "function_status": info["function"],
                    "genotype": v.genotype or "unknown"
                })
        # Also check by gene annotation in VCF
        elif v.gene == target_gene and v.rsid != f"pos_{v.pos}":
            pgx_variants.append({
                "rsid": v.rsid,
                "chromosome": v.chrom,
                "position": v.pos,
                "ref_allele": v.ref,
                "alt_allele": v.alt,
                "gene": target_gene,
                "star_allele": v.star_allele or "unknown",
                "function_status": "unknown",
                "genotype": v.genotype or "unknown"
            })

    return pgx_variants


def determine_phenotype(variants: List[Dict], gene: str) -> str:
    """
    Determine phenotype (PM/IM/NM/RM/URM) based on detected variants.
    Uses diplotype logic based on CPIC guidelines.
    """
    if not variants:
        return "NM"  # Default: Normal Metabolizer if no variants found

    function_statuses = [v.get("function_status", "normal_function") for v in variants]

    no_function_count = sum(1 for f in function_statuses if f == "no_function")
    decreased_count = sum(1 for f in function_statuses if f == "decreased_function")
    increased_count = sum(1 for f in function_statuses if f == "increased_function")

    # Simplified diplotype → phenotype logic
    if no_function_count >= 2:
        return "PM"
    elif no_function_count == 1 and decreased_count >= 1:
        return "PM"
    elif no_function_count == 1:
        return "IM"
    elif decreased_count >= 2:
        return "IM"
    elif decreased_count == 1:
        return "IM"
    elif increased_count >= 2:
        return "URM"
    elif increased_count == 1:
        return "RM"
    else:
        return "NM"


def get_diplotype(variants: List[Dict]) -> str:
    """Build diplotype string from detected variants."""
    if not variants:
        return "*1/*1"
    star_alleles = [v.get("star_allele", "*1") for v in variants[:2]]
    if len(star_alleles) == 1:
        star_alleles.append("*1")
    return f"{star_alleles[0]}/{star_alleles[1]}"
