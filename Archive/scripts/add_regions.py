#!/usr/bin/env python3
"""
Script to add region column to claude.csv by mapping geo_id values
to regions from regions.csv
"""

import pandas as pd
import sys
from pathlib import Path

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
        regions_df = pd.read_csv(regions_file)

        # Create mapping from country_id to Region
        # Handle empty country_id values by filtering them out
        region_mapping = {}
        for _, row in regions_df.iterrows():
            country_id = row['country_id']
            region = row['Region']

            # Skip empty country_id values
            if pd.notna(country_id) and country_id.strip():
                region_mapping[country_id.strip()] = region

        print(f"Created mapping for {len(region_mapping)} countries")

    except Exception as e:
        print(f"Error reading regions.csv: {e}")
        return 1

    print("Reading claude.csv...")
    try:
        # Read claude.csv
        claude_df = pd.read_csv(claude_file)
        print(f"Loaded {len(claude_df)} rows from claude.csv")

        # Check if region column already exists
        if 'region' in claude_df.columns:
            print("Warning: 'region' column already exists. It will be overwritten.")

    except Exception as e:
        print(f"Error reading claude.csv: {e}")
        return 1

    print("Mapping geo_id to regions...")
    try:
        # Map geo_id to region using the mapping dictionary
        claude_df['region'] = claude_df['geo_id'].map(region_mapping).fillna('Unknown')

        # Count successful mappings
        mapped_count = (claude_df['region'] != 'Unknown').sum()
        unknown_count = (claude_df['region'] == 'Unknown').sum()

        print(f"Successfully mapped {mapped_count} rows")
        print(f"Set {unknown_count} rows to 'Unknown' (no matching region found)")

        # Show unique geo_id values that couldn't be mapped
        if unknown_count > 0:
            unknown_geo_ids = claude_df[claude_df['region'] == 'Unknown']['geo_id'].unique()
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
        claude_original = pd.read_csv(claude_file)
        claude_original.to_csv(backup_file, index=False)
        print(f"Original file backed up to {backup_file}")

        # Save updated dataframe
        claude_df.to_csv(claude_file, index=False)
        print(f"Successfully saved updated file to {claude_file}")

        # Show sample of the updated data
        print("\nSample of updated data:")
        sample_columns = ['geo_id', 'geography', 'region'] if 'geography' in claude_df.columns else ['geo_id', 'region']
        print(claude_df[sample_columns].head(10).to_string(index=False))

        # Show region distribution
        print(f"\nRegion distribution:")
        region_counts = claude_df['region'].value_counts()
        for region, count in region_counts.items():
            print(f"  {region}: {count:,} rows")

    except Exception as e:
        print(f"Error saving file: {e}")
        return 1

    print("\nScript completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())