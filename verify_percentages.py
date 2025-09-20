#!/usr/bin/env python3
"""
Verification script to check that percentages sum to 100% within each region+level combination.
"""

import csv
from collections import defaultdict

def verify_percentages():
    """
    Verify that percentages sum to 100% within each region+level combination.
    """
    output_file = "/Users/jordyrodriguez/Downloads/data/softwareregionalrequests_clean.csv"

    print("Reading output file to verify percentages...")

    # Read percentage records
    percentage_records = []
    with open(output_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['variable'] == 'request_pct':
                row['value'] = float(row['value'])
                percentage_records.append(row)

    print(f"Found {len(percentage_records)} percentage records")

    # Group by region+level
    region_level_groups = defaultdict(list)
    for record in percentage_records:
        key = (record['region'], record['level'])
        region_level_groups[key].append(record)

    print(f"Found {len(region_level_groups)} region+level combinations")

    # Check sums
    print("\nVerification results:")
    all_valid = True

    for (region, level), group_records in region_level_groups.items():
        total_pct = sum(record['value'] for record in group_records)
        is_valid = abs(total_pct - 100.0) < 0.01

        if not is_valid:
            all_valid = False

        status = "✓" if is_valid else "✗"
        print(f"{status} {region}, level {level}: {total_pct:.6f}% ({len(group_records)} clusters)")

    if all_valid:
        print("\n✓ All region+level combinations sum to exactly 100%!")
    else:
        print("\n✗ Some combinations do not sum to 100%")

    # Show sample records
    print("\nSample percentage records:")
    sample_key = list(region_level_groups.keys())[0]
    sample_records = region_level_groups[sample_key][:5]

    print(f"\nRegion: {sample_key[0]}, Level: {sample_key[1]}")
    for record in sample_records:
        cluster_name = record['cluster_name']
        display_name = cluster_name[:60] + ('...' if len(cluster_name) > 60 else '')
        print(f"  {display_name}: {record['value']:.2f}%")

if __name__ == "__main__":
    verify_percentages()