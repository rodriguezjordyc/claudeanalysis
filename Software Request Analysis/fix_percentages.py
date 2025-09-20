#!/usr/bin/env python3
"""
Fix Percentages

Recalculate all percentages to ensure they sum to exactly 100% within each region-level combination.
"""

import pandas as pd

def fix_percentages():
    """Recalculate percentages to sum to exactly 100%"""

    input_file = 'softwareregionalrequests_clean.csv'
    output_file = 'softwareregionalrequests_fixed.csv'

    # Load data
    df = pd.read_csv(input_file)
    print(f"Original records: {len(df)}")

    # Check current percentage sums
    print("\nCurrent percentage sums:")
    for region in sorted(df['region'].unique()):
        for level in sorted(df['level'].unique()):
            pct_data = df[(df['region'] == region) &
                         (df['level'] == level) &
                         (df['variable'] == 'request_pct')]
            if len(pct_data) > 0:
                pct_sum = pct_data['value'].astype(float).sum()
                print(f"  {region}, Level {level}: {pct_sum:.6f}%")

    # Rebuild with correct percentages
    results = []

    for region in df['region'].unique():
        for level in df['level'].unique():
            # Get request_count records for this region-level combination
            count_data = df[(df['region'] == region) &
                           (df['level'] == level) &
                           (df['variable'] == 'request_count')].copy()

            if len(count_data) == 0:
                continue

            # Calculate total for this region-level
            total_count = count_data['value'].astype(float).sum()

            # Add request_count records
            for _, row in count_data.iterrows():
                results.append(row.to_dict())

            # Calculate and add request_pct records
            for _, row in count_data.iterrows():
                pct_row = row.copy()
                pct_row['variable'] = 'request_pct'
                pct_row['value'] = (float(row['value']) / total_count) * 100
                pct_row['calculation_method'] = 'count_based_composition'
                results.append(pct_row.to_dict())

    # Create new dataframe
    fixed_df = pd.DataFrame(results)

    # Sort by region, level, variable, value (descending for counts)
    fixed_df = fixed_df.sort_values(['region', 'level', 'variable', 'value'],
                                   ascending=[True, True, True, False])

    # Save to file
    fixed_df.to_csv(output_file, index=False)

    print(f"\nFixed data saved to: {output_file}")
    print(f"Final record count: {len(fixed_df)}")

    # Validation
    print("\nValidation - Fixed percentage sums:")
    for region in sorted(fixed_df['region'].unique()):
        for level in sorted(fixed_df['level'].unique()):
            pct_data = fixed_df[(fixed_df['region'] == region) &
                               (fixed_df['level'] == level) &
                               (fixed_df['variable'] == 'request_pct')]
            if len(pct_data) > 0:
                pct_sum = pct_data['value'].astype(float).sum()
                print(f"  {region}, Level {level}: {pct_sum:.10f}%")

if __name__ == "__main__":
    fix_percentages()