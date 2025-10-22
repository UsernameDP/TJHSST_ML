#!/usr/bin/env python3
import csv
import sys

# Toggle case-insensitive header matching if you want (default: exact match)
CASE_INSENSITIVE = False

# Columns to remove (by name)
REMOVE_BY_NAME = {
    # --- your original list ---
    "id",
    "federalId",
    "x",
    "y",
    "huc4",
    "huc6",
    "huc8",
    "otherNames",
    "formerNames",
    "otherStructureId",
    "fedOwnerIds",
    "fedFundingIds",
    "fedDesignIds",
    "fedConstructionIds",
    "fedRegulatoryIds",
    "fedInspectionIds",
    "fedOperationIds",
    "fedOtherIds",
    "yearsModified",
    "secondaryLengthOfLocks",
    "secondaryWidthOfLocks",
    "eapLastRevDate",
    "operationalStatusId",
    "operationalStatusDate",
    "lastEapExcerDate",
    "politicalPartyId",
    "aiannh",
    # --- new removes you requested ---
    "\ufeffOBJECTID",
    "name",
    "ownerNames",
    "nidId",
    "designerNames",
    "sourceAgency",
    "stateFedId",
    "county",
    "countyState",
    "city",
    "riverName",
    "congDist",
    "stateRegulatoryAgency",
    "zipcode",
    "dataUpdated",
    "inspectionDate",
    "inspectionFrequency",  # you noted it's not rational
    "conditionAssessDate",
    "websiteUrl",
    "usaceDivision",
    "usaceDistrict",
    "femaCommunity",
    "nation",  # redundant (always USA)
    "stateKey",  # redundant with 'state'
}


def normalize(name: str) -> str:
    return name.lower() if CASE_INSENSITIVE else name


def main(input_file, output_file):
    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        if reader.fieldnames is None:
            print("❌ No header row found in the CSV.")
            sys.exit(1)

        original_headers = reader.fieldnames
        norm_headers = [normalize(h) for h in original_headers]
        remove_norm = {normalize(n) for n in REMOVE_BY_NAME}

        # Compute which headers to drop/keep
        keep_fields = [
            h for h, nh in zip(original_headers, norm_headers) if nh not in remove_norm
        ]
        removed = [
            h for h, nh in zip(original_headers, norm_headers) if nh in remove_norm
        ]

        # Also report requested removals that didn't exist
        requested_not_found = sorted(remove_norm - set(norm_headers))

        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=keep_fields)
            writer.writeheader()
            for row in reader:
                writer.writerow({k: row.get(k, "") for k in keep_fields})

    print(f"✅ Cleaned CSV saved as {output_file}")
    print(f"Removed columns ({len(removed)}): {removed}")
    if requested_not_found:
        print(
            f"ℹ️ Requested but not found ({len(requested_not_found)}): {requested_not_found}"
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_csv.py input.csv output.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
