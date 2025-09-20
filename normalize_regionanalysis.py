#!/usr/bin/env python3
"""
Normalize regionanalysis.csv data by applying normalization formula to collaboration and onet_task facets.
Normalization formula: new_task_pct = old_task_pct / sum_all_old_task_pct

This script:
1. Reads the original regionanalysis.csv file
2. For each region and each facet (onet_task, collaboration):
   - Filters out 'none' and 'not_classified' entries
   - Calculates sum of remaining percentages
   - Applies normalization formula
   - Ensures normalized percentages sum to exactly 100%
3. Creates regionanalysis_normalized.csv with normalized data
4. Generates validation report
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import sys
import os

def load_data(file_path: str) -> pd.DataFrame:
    """Load the regionanalysis.csv file."""
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded {len(df)} rows from {file_path}")
        return df
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)

def validate_data_structure(df: pd.DataFrame) -> None:
    """Validate that the data has the expected structure."""
    required_columns = ['region', 'facet', 'level', 'variable', 'cluster_name', 'value']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        sys.exit(1)

    print("Data structure validation passed.")

def get_normalization_targets(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Identify regions and facets that need normalization."""
    targets = {}

    # Get all unique regions (excluding 'region' header if present)
    regions = df['region'].unique()
    regions = [r for r in regions if r != 'region']

    for region in regions:
        region_data = df[df['region'] == region]
        facets = region_data['facet'].unique()

        # Only process onet_task and collaboration facets
        target_facets = [f for f in facets if f in ['onet_task', 'collaboration']]

        if target_facets:
            targets[region] = target_facets

    return targets

def normalize_facet_data(df: pd.DataFrame, region: str, facet: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Normalize percentage data for a specific region and facet.

    Returns:
        - Modified dataframe with normalized values
        - Validation info dictionary
    """
    validation_info = {
        'region': region,
        'facet': facet,
        'original_sum': 0,
        'normalized_sum': 0,
        'excluded_items': [],
        'normalized_items': [],
        'records_modified': 0
    }

    # Filter data for this region and facet
    mask = (df['region'] == region) & (df['facet'] == facet) & (df['variable'].str.endswith('_pct'))
    facet_data = df[mask].copy()

    if facet_data.empty:
        print(f"Warning: No percentage data found for {region} - {facet}")
        return df, validation_info

    # Separate items to exclude from normalization
    exclude_mask = facet_data['cluster_name'].isin(['none', 'not_classified'])
    excluded_items = facet_data[exclude_mask].copy()
    items_to_normalize = facet_data[~exclude_mask].copy()

    if items_to_normalize.empty:
        print(f"Warning: No items to normalize for {region} - {facet} (all are 'none' or 'not_classified')")
        return df, validation_info

    # Record excluded items
    validation_info['excluded_items'] = excluded_items['cluster_name'].tolist()

    # Calculate original sum of items to be normalized
    original_sum = items_to_normalize['value'].sum()
    validation_info['original_sum'] = original_sum

    if original_sum == 0:
        print(f"Warning: Sum of normalizable items is 0 for {region} - {facet}")
        return df, validation_info

    # Apply normalization formula: new_pct = old_pct / sum_old_pct * 100
    normalized_values = (items_to_normalize['value'] / original_sum) * 100

    # Update the dataframe with normalized values
    for idx, new_value in zip(items_to_normalize.index, normalized_values):
        df.loc[idx, 'value'] = new_value
        validation_info['records_modified'] += 1

    # Record normalized items and final sum
    validation_info['normalized_items'] = items_to_normalize['cluster_name'].tolist()
    validation_info['normalized_sum'] = normalized_values.sum()

    return df, validation_info

def add_normalization_flag(df: pd.DataFrame, normalization_targets: Dict[str, List[str]]) -> pd.DataFrame:
    """Add a column to track which records were normalized."""
    df = df.copy()
    df['normalization_applied'] = False

    for region, facets in normalization_targets.items():
        for facet in facets:
            # Mark percentage records that were normalized (excluding 'none' and 'not_classified')
            mask = (
                (df['region'] == region) &
                (df['facet'] == facet) &
                (df['variable'].str.endswith('_pct')) &
                (~df['cluster_name'].isin(['none', 'not_classified']))
            )
            df.loc[mask, 'normalization_applied'] = True

    return df

def generate_validation_report(validation_results: List[Dict], output_path: str) -> None:
    """Generate a detailed validation report."""
    with open(output_path, 'w') as f:
        f.write("REGIONANALYSIS NORMALIZATION VALIDATION REPORT\n")
        f.write("=" * 50 + "\n\n")

        f.write("SUMMARY:\n")
        f.write(f"Total regions processed: {len(set(r['region'] for r in validation_results))}\n")
        f.write(f"Total facets processed: {len(validation_results)}\n")
        f.write(f"Total records modified: {sum(r['records_modified'] for r in validation_results)}\n\n")

        f.write("DETAILED RESULTS BY REGION AND FACET:\n")
        f.write("-" * 40 + "\n\n")

        for result in validation_results:
            f.write(f"Region: {result['region']}\n")
            f.write(f"Facet: {result['facet']}\n")
            f.write(f"Original sum: {result['original_sum']:.6f}%\n")
            f.write(f"Normalized sum: {result['normalized_sum']:.6f}%\n")
            f.write(f"Records modified: {result['records_modified']}\n")

            if result['excluded_items']:
                f.write(f"Excluded items: {', '.join(result['excluded_items'])}\n")

            if result['normalized_items']:
                f.write(f"Normalized items count: {len(result['normalized_items'])}\n")
                if len(result['normalized_items']) <= 10:
                    f.write(f"Normalized items: {', '.join(result['normalized_items'][:10])}\n")
                else:
                    f.write(f"Normalized items (first 10): {', '.join(result['normalized_items'][:10])}...\n")

            # Check if normalization was successful (sum should be ~100%)
            if abs(result['normalized_sum'] - 100.0) < 0.0001:
                f.write("✓ Normalization successful (sum = 100%)\n")
            else:
                f.write(f"⚠ Warning: Normalized sum is {result['normalized_sum']:.6f}% (not exactly 100%)\n")

            f.write("\n" + "-" * 40 + "\n\n")

def main():
    """Main function to execute the normalization process."""
    # File paths
    input_file = "/Users/jordyrodriguez/Downloads/data/regionanalysis.csv"
    output_file = "/Users/jordyrodriguez/Downloads/data/regionanalysis_normalized.csv"
    validation_report = "/Users/jordyrodriguez/Downloads/data/normalization_validation_report.txt"

    print("Starting regionanalysis data normalization...")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Validation report: {validation_report}")
    print()

    # Load and validate data
    df = load_data(input_file)
    validate_data_structure(df)

    # Identify normalization targets
    normalization_targets = get_normalization_targets(df)
    print("Normalization targets identified:")
    for region, facets in normalization_targets.items():
        print(f"  {region}: {', '.join(facets)}")
    print()

    # Apply normalization
    validation_results = []
    df_normalized = df.copy()

    for region, facets in normalization_targets.items():
        for facet in facets:
            print(f"Processing {region} - {facet}...")
            df_normalized, validation_info = normalize_facet_data(df_normalized, region, facet)
            validation_results.append(validation_info)

    # Add normalization flag
    df_normalized = add_normalization_flag(df_normalized, normalization_targets)

    # Save normalized data
    df_normalized.to_csv(output_file, index=False)
    print(f"\nNormalized data saved to: {output_file}")

    # Generate validation report
    generate_validation_report(validation_results, validation_report)
    print(f"Validation report saved to: {validation_report}")

    # Print summary
    print("\nNORMALIZATION SUMMARY:")
    print(f"Original records: {len(df)}")
    print(f"Normalized records: {len(df_normalized)}")
    print(f"Records with normalization applied: {df_normalized['normalization_applied'].sum()}")
    print(f"Regions processed: {len(normalization_targets)}")
    print(f"Total facets processed: {len(validation_results)}")

    print("\nNormalization completed successfully!")

if __name__ == "__main__":
    main()