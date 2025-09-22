#!/usr/bin/env python3
"""
Clean Software Data Script

Removes the non-software request "Say a specific single-digit number" from
the softwareregionalrequests_clean.csv and recalculates clean percentages.
"""

import csv
import pandas as pd

def clean_and_recalculate():
    """Remove non-software request and recalculate percentages"""

    input_file = 'softwareregionalrequests_clean.csv'
    output_file = 'softwareregionalrequests_clean_fixed.csv'

    # Read the data
    df = pd.read_csv(input_file)

    print(f"Original data: {len(df)} records")

    # Remove the problematic cluster
    problematic_cluster = "Say a specific single-digit number"
    before_count = len(df)
    df = df[df['cluster_name'] != problematic_cluster]
    after_count = len(df)

    print(f"Removed '{problematic_cluster}': {before_count - after_count} records")
    print(f"Remaining data: {after_count} records")

    # Now recalculate clean percentages
    # Group by region and level, then recalculate percentages within each group

    results = []

    for region in df['region'].unique():
        for level in df['level'].unique():
            # Get request_count records for this region-level combination
            mask = ((df['region'] == region) &
                   (df['level'] == level) &
                   (df['variable'] == 'request_count'))

            group_data = df[mask].copy()

            if len(group_data) == 0:
                continue

            # Calculate total for this region-level
            total_count = group_data['value'].astype(float).sum()

            # Add request_count records
            for _, row in group_data.iterrows():
                results.append(row.to_dict())

            # Calculate and add request_pct records
            for _, row in group_data.iterrows():
                pct_row = row.copy()
                pct_row['variable'] = 'request_pct'
                pct_row['value'] = (float(row['value']) / total_count) * 100
                pct_row['calculation_method'] = 'count_based_composition'
                results.append(pct_row.to_dict())

    # Create new dataframe
    cleaned_df = pd.DataFrame(results)

    # Sort by region, level, variable, value (descending for counts)
    cleaned_df = cleaned_df.sort_values(['region', 'level', 'variable', 'value'],
                                       ascending=[True, True, True, False])

    # Save to file
    cleaned_df.to_csv(output_file, index=False)

    print(f"\nCleaned data saved to: {output_file}")
    print(f"Final record count: {len(cleaned_df)}")

    # Validation: Check that percentages sum to 100% within each region-level
    print("\nValidation - Percentage sums by region and level:")
    for region in cleaned_df['region'].unique():
        for level in cleaned_df['level'].unique():
            pct_data = cleaned_df[(cleaned_df['region'] == region) &
                                 (cleaned_df['level'] == level) &
                                 (cleaned_df['variable'] == 'request_pct')]
            if len(pct_data) > 0:
                pct_sum = pct_data['value'].astype(float).sum()
                print(f"  {region}, Level {level}: {pct_sum:.6f}%")

if __name__ == "__main__":
    clean_and_recalculate()