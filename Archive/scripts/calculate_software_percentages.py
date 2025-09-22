#!/usr/bin/env python3
"""
Script to calculate clean request_pct values for software development dataset.

Adds request_pct records to softwareregionalrequests.csv so that within each
region+level combination, all cluster percentages sum to 100%.
"""

import csv
from collections import defaultdict, OrderedDict

def calculate_software_percentages():
    """
    Calculate clean request_pct values for the software development dataset.
    """
    # File paths
    input_file = "/Users/jordyrodriguez/Downloads/data/softwareregionalrequests.csv"
    output_file = "/Users/jordyrodriguez/Downloads/data/softwareregionalrequests_clean.csv"

    print("Reading input file...")

    # Read all records
    records = []
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            # Convert value to float
            row['value'] = float(row['value'])
            records.append(row)

    print(f"Original dataset records: {len(records)}")

    # Verify all records are request_count
    all_request_count = all(row['variable'] == 'request_count' for row in records)
    print(f"All records are request_count: {all_request_count}")

    if not all_request_count:
        raise ValueError("Expected all records to have variable='request_count'")

    # Group records by region+level
    region_level_groups = defaultdict(list)
    for record in records:
        key = (record['region'], record['level'])
        region_level_groups[key].append(record)

    print(f"Unique region+level combinations: {len(region_level_groups)}")

    # Calculate totals for each region+level
    region_level_totals = {}
    for key, group_records in region_level_groups.items():
        total = sum(record['value'] for record in group_records)
        region_level_totals[key] = total

    print("\nCalculating percentages by region+level...")

    # Create percentage records
    percentage_records = []
    validation_data = []

    for (region, level), group_records in region_level_groups.items():
        total_count = region_level_totals[(region, level)]

        print(f"Processing {region}, level {level}: {len(group_records)} clusters, total count: {total_count}")

        # Calculate percentages for this group
        group_percentage_sum = 0

        for record in group_records:
            # Calculate percentage
            cluster_pct = (record['value'] / total_count) * 100
            group_percentage_sum += cluster_pct

            # Create new record for percentage
            pct_record = record.copy()
            pct_record['variable'] = 'request_pct'
            pct_record['value'] = cluster_pct
            pct_record['calculation_method'] = 'count_based_composition'

            percentage_records.append(pct_record)

        # Store validation data
        validation_data.append({
            'region': region,
            'level': level,
            'percentage_sum': group_percentage_sum,
            'is_valid': abs(group_percentage_sum - 100.0) < 0.01  # Allow for small floating point errors
        })

    print(f"Created {len(percentage_records)} percentage records")

    # Validation
    print("\nValidating percentage calculations...")
    valid_combinations = sum(1 for v in validation_data if v['is_valid'])
    invalid_combinations = len(validation_data) - valid_combinations

    print(f"Validation summary:")
    print(f"- Total region+level combinations: {len(validation_data)}")
    print(f"- Valid combinations (sum = 100%): {valid_combinations}")
    print(f"- Invalid combinations: {invalid_combinations}")

    if invalid_combinations > 0:
        print("\nWARNING: Some percentage sums do not equal 100%:")
        for v in validation_data:
            if not v['is_valid']:
                print(f"  {v['region']}, level {v['level']}: {v['percentage_sum']:.4f}%")
    else:
        print("✓ All percentage combinations sum to exactly 100%")

    # Show sample of percentage calculations
    print("\nSample percentage calculations:")
    sample_validation = validation_data[0]
    sample_key = (sample_validation['region'], sample_validation['level'])
    sample_pct_records = [r for r in percentage_records
                         if r['region'] == sample_key[0] and r['level'] == sample_key[1]][:5]

    print(f"\nRegion: {sample_validation['region']}, Level: {sample_validation['level']}")
    for record in sample_pct_records:
        cluster_name = record['cluster_name']
        display_name = cluster_name[:50] + ('...' if len(cluster_name) > 50 else '')
        print(f"  {display_name}: {record['value']:.2f}%")

    # Combine original and percentage records
    all_records = records + percentage_records

    print(f"\nFinal dataset records: {len(all_records)}")
    print(f"Original records: {len(records)}")
    print(f"Percentage records: {len(percentage_records)}")

    # Write output file
    print(f"\nWriting output to: {output_file}")
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in all_records:
            writer.writerow(record)

    print("✓ Processing completed successfully!")

    # Final summary
    print(f"\nSummary:")
    print(f"- Input file: {input_file}")
    print(f"- Output file: {output_file}")
    print(f"- Original records: {len(records)} (all request_count)")
    print(f"- New percentage records: {len(percentage_records)} (all request_pct)")
    print(f"- Total records in output: {len(all_records)}")
    print(f"- Record count doubled as expected: {len(all_records) == 2 * len(records)}")

if __name__ == "__main__":
    calculate_software_percentages()