import os

from ingestion.vcf_standardization.standardize import standardize_vcf
from ingestion.generic.utils import check_manifest
from lifeomic_logging import scoped_logger


def process(
    manifest_file: str,
    vcf_file: str,
    source_file_id: str,
    out_path: str,
) -> dict[str, str]:
    with scoped_logger(__name__) as log:

        # Read in supplied manifest
        manifest = check_manifest(manifest_file, log)

        # Process VCF
        base_vcf_file = os.path.basename(vcf_file)
        vcf_out = base_vcf_file.replace(".vcf", ".modified.vcf")
        vcf_line_count = standardize_vcf(vcf_file, vcf_out, out_path, log)

        # Add to manifest
        manifest["sourceFileId"] = source_file_id
        manifest["resources"] = [
            {"fileName": f'.lifeomic/vcf-ingest/{manifest["name"]}/{base_vcf_file}'}
        ]
        manifest["files"] = [
            {
                "fileName": f'.lifeomic/vcf-ingest/{manifest["name"]}/{vcf_out}',
                "sequenceType": "germline",
                "type": "shortVariant",
            }
        ]

        case_metadata = {
            "test_type": manifest["testType"],
            "vcf_line_count": vcf_line_count,
            "case_id": manifest["reportID"],
            "germline_genome_reference": manifest["reference"],
        }

        return case_metadata, manifest
