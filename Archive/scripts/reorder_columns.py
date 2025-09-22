#!/usr/bin/env python3
"""
Script to reorder columns in claude.csv file.
Moves 'region' column from last position to first position.
"""

import pandas as pd
import shutil
from datetime import datetime
import os

def main():
    # File paths
    input_file = '/Users/jordyrodriguez/Downloads/data/claude.csv'
    backup_file = f'/Users/jordyrodriguez/Downloads/data/claude_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    print("Starting column reordering process...")

    # Step 1: Create backup of original file
    print(f"Creating backup: {backup_file}")
    try:
        shutil.copy2(input_file, backup_file)
        print("✓ Backup created successfully")
    except Exception as e:
        print(f"✗ Error creating backup: {e}")
        return False

    # Step 2: Read the CSV file
    print("Reading claude.csv file...")
    try:
        df = pd.read_csv(input_file)
        print(f"✓ File read successfully. Shape: {df.shape}")
        print(f"Current columns: {list(df.columns)}")
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return False

    # Step 3: Verify current column structure
    expected_columns = ['geo_id', 'geography', 'date_start', 'date_end', 'platform_and_product',
                       'facet', 'level', 'variable', 'cluster_name', 'value', 'region']

    if list(df.columns) != expected_columns:
        print(f"✗ Warning: Column structure doesn't match expected format")
        print(f"Expected: {expected_columns}")
        print(f"Found: {list(df.columns)}")
        # Continue anyway, but let user know

    # Step 4: Reorder columns with 'region' first
    desired_order = ['region', 'geo_id', 'geography', 'date_start', 'date_end',
                    'platform_and_product', 'facet', 'level', 'variable', 'cluster_name', 'value']

    print("Reordering columns...")
    try:
        # Verify all desired columns exist
        missing_columns = [col for col in desired_order if col not in df.columns]
        if missing_columns:
            print(f"✗ Missing columns: {missing_columns}")
            return False

        # Reorder the DataFrame
        df_reordered = df[desired_order]
        print(f"✓ Columns reordered successfully")
        print(f"New column order: {list(df_reordered.columns)}")

    except Exception as e:
        print(f"✗ Error reordering columns: {e}")
        return False

    # Step 5: Save the reordered file
    print("Saving updated file...")
    try:
        df_reordered.to_csv(input_file, index=False)
        print("✓ File saved successfully")

        # Verify the save worked
        verification_df = pd.read_csv(input_file)
        if list(verification_df.columns) == desired_order:
            print("✓ File verification passed - columns are in correct order")
        else:
            print("✗ File verification failed - columns may not be in correct order")

    except Exception as e:
        print(f"✗ Error saving file: {e}")
        return False

    # Step 6: Display summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Original file: {input_file}")
    print(f"Backup created: {backup_file}")
    print(f"Rows processed: {len(df_reordered):,}")
    print(f"Columns: {len(df_reordered.columns)}")
    print(f"New column order: {' -> '.join(desired_order)}")
    print("✓ Column reordering completed successfully!")

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n✗ Script completed with errors. Check the backup file if needed.")
        exit(1)
    else:
        print("\n✓ Script completed successfully!")