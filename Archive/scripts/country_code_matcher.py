#!/usr/bin/env python3
"""
Script to parse country codes from RTF file and add ISO-2 codes to regions.csv
"""

import csv
import re

def parse_rtf_country_codes(rtf_file_path: str) -> dict:
    """
    Parse the RTF file to extract country name to ISO-2 code mapping.

    Args:
        rtf_file_path: Path to the RTF file containing country codes

    Returns:
        Dictionary mapping country names to ISO-2 codes
    """
    country_mapping = {}

    with open(rtf_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the header line (around line 59) and start parsing from there
    header_found = False
    for i, line in enumerate(lines):
        if 'ISO\tISO3\tISO-Numeric\tfips\tCountry' in line:
            header_found = True
            print(f"Found header at line {i + 1}")
            continue

        if header_found and line.strip():
            # Remove RTF formatting and split by tabs
            clean_line = line.strip().replace('\\', '')
            if clean_line and not clean_line.startswith('#'):
                parts = clean_line.split('\t')
                if len(parts) >= 5:
                    iso2_code = parts[0].strip()
                    country_name = parts[4].strip()

                    # Only add if both ISO2 code and country name are valid
                    if iso2_code and len(iso2_code) == 2 and country_name:
                        country_mapping[country_name] = iso2_code
                        print(f"Mapped: {country_name} -> {iso2_code}")

    print(f"Total countries parsed from RTF: {len(country_mapping)}")
    return country_mapping

def create_country_name_variants(country_mapping: dict) -> dict:
    """
    Create additional mappings for common country name variations.

    Args:
        country_mapping: Original mapping from RTF file

    Returns:
        Extended mapping including common variations
    """
    extended_mapping = country_mapping.copy()

    # Add common variations based on what we see in the regions.csv
    variations = {
        # Common name variations
        'United States': 'US',
        'United Kingdom': 'GB',
        'South Korea': 'KR',
        'The Netherlands': 'NL',
        'Czechia': 'CZ',
        'North Macedonia': 'MK',
        'Republic of the Congo': 'CG',
        'Ivory Coast': 'CI',
        'Cabo Verde': 'CV',
        'Eswatini': 'SZ',
        'Timor Leste': 'TL',
        'Palestinian Territory': 'PS',
    }

    # Add the variations to the mapping
    for variation, iso_code in variations.items():
        extended_mapping[variation] = iso_code

    # Add direct mappings from the RTF file, handling special cases
    for country, iso_code in country_mapping.items():
        # Handle some specific RTF naming patterns
        if 'Korea, Republic of' in country:
            extended_mapping['South Korea'] = iso_code
        elif country == 'Netherlands':
            extended_mapping['The Netherlands'] = iso_code
        elif 'Czech Republic' in country:
            extended_mapping['Czechia'] = iso_code
        elif 'Macedonia' in country and 'North' in country:
            extended_mapping['North Macedonia'] = iso_code
        elif 'Congo' in country and 'Republic' in country and 'Democratic' not in country:
            extended_mapping['Republic of the Congo'] = iso_code
        elif 'Cote d\'Ivoire' in country or 'Côte d\'Ivoire' in country:
            extended_mapping['Ivory Coast'] = iso_code
        elif 'Cape Verde' in country:
            extended_mapping['Cabo Verde'] = iso_code
        elif 'Swaziland' in country:
            extended_mapping['Eswatini'] = iso_code
        elif 'Timor-Leste' in country:
            extended_mapping['Timor Leste'] = iso_code
        elif 'Palestine' in country:
            extended_mapping['Palestinian Territory'] = iso_code

    return extended_mapping

def fuzzy_match_country(country_name: str, country_mapping: dict) -> str:
    """
    Attempt to find a fuzzy match for a country name.

    Args:
        country_name: Country name to match
        country_mapping: Dictionary of country names to ISO codes

    Returns:
        ISO-2 code if match found, empty string otherwise
    """
    # Try exact match first
    if country_name in country_mapping:
        return country_mapping[country_name]

    # Try case-insensitive match
    for mapped_country, iso_code in country_mapping.items():
        if country_name.lower() == mapped_country.lower():
            return iso_code

    # Try partial matching - check if the region country name is contained in the RTF country name
    for mapped_country, iso_code in country_mapping.items():
        if country_name.lower() in mapped_country.lower():
            return iso_code

    # Try reverse partial matching - check if the RTF country name is contained in the region country name
    for mapped_country, iso_code in country_mapping.items():
        if mapped_country.lower() in country_name.lower():
            return iso_code

    return ""

def update_regions_csv(csv_file_path: str, country_mapping: dict):
    """
    Update the regions.csv file with ISO-2 country codes.

    Args:
        csv_file_path: Path to the regions.csv file
        country_mapping: Dictionary mapping country names to ISO-2 codes
    """
    # Read the CSV file
    rows = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    print(f"Loaded {len(rows)} rows from regions.csv")

    # Create extended mapping with variations
    extended_mapping = create_country_name_variants(country_mapping)

    # Process each row and add country_id
    unmatched_countries = set()
    matched_count = 0

    for row in rows:
        country = row.get('Country', '').strip()

        if not country:  # Handle empty country names
            row['country_id'] = ""
            continue

        # Try to find the ISO code
        iso_code = fuzzy_match_country(country, extended_mapping)

        if iso_code:
            row['country_id'] = iso_code
            matched_count += 1
            print(f"✓ Matched: {country} -> {iso_code}")
        else:
            row['country_id'] = ""
            unmatched_countries.add(country)
            print(f"✗ No match found for: {country}")

    # Write the updated CSV
    fieldnames = ['Country', 'Region', 'country_id']

    # Save as backup first
    backup_path = csv_file_path.replace('.csv', '_backup.csv')
    with open(backup_path, 'w', newline='', encoding='utf-8') as backup_file:
        with open(csv_file_path, 'r', encoding='utf-8') as original_file:
            backup_file.write(original_file.read())

    # Write updated file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n=== SUMMARY ===")
    print(f"Total countries processed: {len(rows)}")
    print(f"Countries matched: {matched_count}")
    print(f"Countries unmatched: {len(unmatched_countries)}")
    print(f"Backup saved as: {backup_path}")
    print(f"Updated file: {csv_file_path}")

    if unmatched_countries:
        print(f"\nUnmatched countries:")
        for country in sorted(unmatched_countries):
            if country:  # Only show non-empty country names
                print(f"  - {country}")

    return rows

def main():
    """Main function to execute the country code matching process."""
    rtf_file = "/Users/jordyrodriguez/Downloads/data/Country Codes.rtf"
    csv_file = "/Users/jordyrodriguez/Downloads/data/regions.csv"

    print("Starting country code matching process...")
    print("=" * 50)

    # Parse the RTF file
    print("1. Parsing RTF file for country codes...")
    country_mapping = parse_rtf_country_codes(rtf_file)

    if not country_mapping:
        print("ERROR: No country codes found in RTF file!")
        return

    print(f"Found {len(country_mapping)} countries in RTF file")

    # Update the CSV file
    print("\n2. Updating regions.csv with country codes...")
    updated_rows = update_regions_csv(csv_file, country_mapping)

    print("\n3. Process completed successfully!")

    # Show a sample of the results
    print("\nSample of updated data (first 10 rows):")
    print("Country | Region | country_id")
    print("-" * 50)
    for i, row in enumerate(updated_rows[:10]):
        country = row.get('Country', '')
        region = row.get('Region', '')
        country_id = row.get('country_id', '')
        print(f"{country} | {region} | {country_id}")

if __name__ == "__main__":
    main()