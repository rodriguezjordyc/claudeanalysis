#!/usr/bin/env python3
"""
Script to add region column to claude.csv by mapping geo_id values
to regions from regions.csv using built-in csv module
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

def main():
    # Define file paths
    regions_file = Path("regions.csv")
    claude_file = Path("claude.csv")

    # Check if files exist
    if not regions_file.exists():
        print(f"Error: {regions_file} not found")
        return 1

    if not claude_file.exists():
        print(f"Error: {claude_file} not found")
        return 1

    print("Reading regions.csv...")
    try:
        # Read regions.csv and create mapping dictionary
        region_mapping = {}
        with open(regions_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                country_id = row['country_id'].strip() if row['country_id'] else ''
                region = row['Region']

                # Skip empty country_id values
                if country_id:
                    region_mapping[country_id] = region

        print(f"Created mapping for {len(region_mapping)} countries")

    except Exception as e:
        print(f"Error reading regions.csv: {e}")
        return 1

    print("Reading claude.csv...")
    try:
        # Read claude.csv
        claude_rows = []
        with open(claude_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                claude_rows.append(row)

        print(f"Loaded {len(claude_rows)} rows from claude.csv")

        # Check if region column already exists
        if 'region' in fieldnames:
            print("Warning: 'region' column already exists. It will be overwritten.")
        else:
            fieldnames = list(fieldnames) + ['region']

    except Exception as e:
        print(f"Error reading claude.csv: {e}")
        return 1

    print("Mapping geo_id to regions...")
    try:
        # Map geo_id to region using the mapping dictionary
        mapped_count = 0
        unknown_count = 0
        unknown_geo_ids = set()

        for row in claude_rows:
            geo_id = row['geo_id']
            if geo_id in region_mapping:
                row['region'] = region_mapping[geo_id]
                mapped_count += 1
            else:
                row['region'] = 'Unknown'
                unknown_count += 1
                unknown_geo_ids.add(geo_id)

        print(f"Successfully mapped {mapped_count} rows")
        print(f"Set {unknown_count} rows to 'Unknown' (no matching region found)")

        # Show unique geo_id values that couldn't be mapped
        if unknown_count > 0:
            print(f"Unmapped geo_id values: {sorted(unknown_geo_ids)}")

    except Exception as e:
        print(f"Error mapping regions: {e}")
        return 1

    print("Saving updated claude.csv...")
    try:
        # Create backup of original file
        backup_file = claude_file.with_suffix('.csv.backup')
        if backup_file.exists():
            print(f"Backup file {backup_file} already exists, overwriting...")

        # Copy original to backup
        with open(claude_file, 'r', encoding='utf-8') as src, \
             open(backup_file, 'w', encoding='utf-8', newline='') as dst:
            dst.write(src.read())
        print(f"Original file backed up to {backup_file}")

        # Save updated dataframe
        with open(claude_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(claude_rows)

        print(f"Successfully saved updated file to {claude_file}")

        # Show sample of the updated data
        print("\nSample of updated data (first 10 rows):")
        print(f"{'geo_id':<6} {'geography':<12} {'region':<20}")
        print("-" * 38)
        for i, row in enumerate(claude_rows[:10]):
            geo_id = row.get('geo_id', '')[:6]
            geography = row.get('geography', '')[:12]
            region = row.get('region', '')[:20]
            print(f"{geo_id:<6} {geography:<12} {region:<20}")

        # Show region distribution
        print(f"\nRegion distribution:")
        region_counts = defaultdict(int)
        for row in claude_rows:
            region_counts[row['region']] += 1

        for region in sorted(region_counts.keys()):
            count = region_counts[region]
            print(f"  {region}: {count:,} rows")

    except Exception as e:
        print(f"Error saving file: {e}")
        return 1

    print("\nScript completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())