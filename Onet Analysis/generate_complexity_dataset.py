#!/usr/bin/env python3
"""
Generate expanded O*NET regional dataset with API complexity volumes.

This script transforms the existing onetregionalraw.csv to include complexity volume
metrics derived from 1P API complexity benchmarks, enabling regional AI utilization
sophistication analysis.

Input:
- onetregionalraw.csv: Regional O*NET task volumes
- ../api.csv: Global API complexity benchmarks

Output:
- onetregionalraw_with_complexity.csv: Expanded dataset with complexity volumes

Structure: For each task, creates 4 rows:
1. Original: onet_task_count (baseline volume)
2. New: prompt_complexity_volume (volume × prompt_tokens_index)
3. New: completion_complexity_volume (volume × completion_tokens_index)
4. New: cost_complexity_volume (volume × cost_index)
"""

import csv
import os
from collections import defaultdict

def load_api_complexity_benchmarks(api_file_path):
    """Load API complexity indices for O*NET tasks."""
    complexity_benchmarks = {}

    with open(api_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Look for onet_task::* facets with ::index cluster names
            if ('onet_task::' in row['facet'] and
                '::index' in row['cluster_name']):

                task_name = row['cluster_name'].replace('::index', '')
                metric_type = row['facet'].split('::')[1]  # prompt_tokens, completion_tokens, cost
                complexity_index = float(row['value'])

                if task_name not in complexity_benchmarks:
                    complexity_benchmarks[task_name] = {}
                complexity_benchmarks[task_name][metric_type] = complexity_index

    print(f"Loaded complexity benchmarks for {len(complexity_benchmarks)} tasks")
    return complexity_benchmarks

def generate_complexity_dataset(input_file, output_file, complexity_benchmarks):
    """Transform regional dataset by adding complexity volume metrics."""

    output_rows = []
    tasks_with_complexity = 0
    tasks_without_complexity = 0
    total_volume_covered = 0
    total_volume_uncovered = 0

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Keep original row
            output_rows.append(row.copy())

            # Skip non-task rows (not_classified, none)
            if row['cluster_name'] in ['not_classified', 'none']:
                continue

            task_name = row['cluster_name']
            original_volume = float(row['value'])

            # Check if we have complexity data for this task
            if task_name in complexity_benchmarks:
                tasks_with_complexity += 1
                total_volume_covered += original_volume
                complexity_data = complexity_benchmarks[task_name]

                # Generate complexity volume rows
                for metric_type in ['prompt_tokens', 'completion_tokens', 'cost']:
                    if metric_type in complexity_data:
                        complexity_index = complexity_data[metric_type]
                        complexity_volume = original_volume * complexity_index

                        # Create new row with complexity volume
                        complexity_row = row.copy()
                        complexity_row['variable'] = f'{metric_type}_complexity_volume'
                        complexity_row['value'] = str(complexity_volume)

                        output_rows.append(complexity_row)
            else:
                tasks_without_complexity += 1
                total_volume_uncovered += original_volume

    # Write expanded dataset
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['region', 'facet', 'level', 'variable', 'cluster_name', 'value', 'domain']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    # Print summary statistics
    total_tasks = tasks_with_complexity + tasks_without_complexity
    total_volume = total_volume_covered + total_volume_uncovered
    coverage_pct = (total_volume_covered / total_volume) * 100 if total_volume > 0 else 0

    print(f"\nDataset Generation Summary:")
    print(f"=" * 50)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Total output rows: {len(output_rows):,}")
    print(f"\nComplexity Coverage:")
    print(f"Tasks with complexity data: {tasks_with_complexity:,}")
    print(f"Tasks without complexity data: {tasks_without_complexity:,}")
    print(f"Volume coverage: {coverage_pct:.1f}%")
    print(f"Covered volume: {total_volume_covered:,.0f}")
    print(f"Uncovered volume: {total_volume_uncovered:,.0f}")

def main():
    # File paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'onetregionalraw.csv')
    output_file = os.path.join(script_dir, 'onetregionalraw_with_complexity.csv')
    api_file = os.path.join(script_dir, '..', 'api.csv')

    print("Generating O*NET Regional Dataset with Complexity Volumes")
    print("=" * 60)

    # Load API complexity benchmarks
    print("Step 1: Loading API complexity benchmarks...")
    complexity_benchmarks = load_api_complexity_benchmarks(api_file)

    # Generate expanded dataset
    print("Step 2: Generating expanded dataset...")
    generate_complexity_dataset(input_file, output_file, complexity_benchmarks)

    print(f"\n✅ Complete! New dataset saved as: {output_file}")

if __name__ == "__main__":
    main()