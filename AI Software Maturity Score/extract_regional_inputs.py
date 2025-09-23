#!/usr/bin/env python3
"""
Extract regional input metrics for AI Software Maturity Score calculation.

This script pulls required metrics from the three analysis areas:
1. Collaboration Analysis: directive and feedback loop percentages
2. Length Analysis: software development length indices (prompt, completion, cost)
3. Software Request Analysis: Level 0 complexity request percentages

Output: regional_inputs.csv with standardized regional metrics
"""

import pandas as pd
import os

def extract_collaboration_metrics():
    """Extract collaboration pattern percentages by region."""
    print("Extracting collaboration metrics...")

    # Load collaboration data
    collab_file = "../Collaboration Analysis/regional_collaboration_analysis.csv"
    df_collab = pd.read_csv(collab_file)

    # Filter for percentage data and relevant patterns
    collab_pct = df_collab[df_collab['variable'] == 'collaboration_pct'].copy()

    # Focus on augmentation patterns (validation, task iteration, learning)

    results = {}
    for region in ['North America', 'Latin America', 'Europe', 'Middle East & Africa', 'APAC']:
        region_data = collab_pct[collab_pct['region'] == region]

        validation_pct = region_data[region_data['cluster_name'] == 'validation']['value'].iloc[0]
        task_iteration_pct = region_data[region_data['cluster_name'] == 'task iteration']['value'].iloc[0]
        learning_pct = region_data[region_data['cluster_name'] == 'learning']['value'].iloc[0]

        results[region] = {
            'validation_pct': validation_pct,
            'task_iteration_pct': task_iteration_pct,
            'learning_pct': learning_pct
        }

        print(f"  {region}: Validation {validation_pct:.1f}%, Task Iteration {task_iteration_pct:.1f}%, Learning {learning_pct:.1f}%")

    return results

def extract_efficiency_metrics():
    """Extract software development efficiency indices by region."""
    print("\nExtracting software development efficiency metrics...")

    # Load length data with complexity volumes
    length_file = "../Onet Analysis/onetregionalraw_with_complexity.csv"
    df_length = pd.read_csv(length_file)

    # Filter for software development domain only
    sw_data = df_length[df_length['domain'] == 'Software_Development'].copy()

    # Define efficiency metrics
    efficiency_metrics = {
        'prompt_tokens_complexity_volume': 'sw_prompt_length',
        'completion_tokens_complexity_volume': 'sw_completion_length',
        'cost_complexity_volume': 'sw_cost_index'
    }

    results = {}
    for region in ['North America', 'Latin America', 'Europe', 'Middle East & Africa', 'APAC']:
        region_data = sw_data[sw_data['region'] == region]

        # Get original volume total for software development
        original_total = region_data[region_data['variable'] == 'onet_task_count']['value'].sum()

        efficiency_indices = {}
        for metric_var, metric_name in efficiency_metrics.items():
            # Get efficiency volume total
            efficiency_total = region_data[region_data['variable'] == metric_var]['value'].sum()

            # Calculate weighted efficiency index
            efficiency_index = efficiency_total / original_total if original_total > 0 else 0
            efficiency_indices[metric_name] = efficiency_index

        results[region] = efficiency_indices

        print(f"  {region}: Prompt {efficiency_indices['sw_prompt_length']:.3f}, " +
              f"Completion {efficiency_indices['sw_completion_length']:.3f}, " +
              f"Cost {efficiency_indices['sw_cost_index']:.3f}")

    return results

def extract_complexity_metrics():
    """Extract Level 0 software complexity request percentages by region."""
    print("\nExtracting software complexity metrics...")

    # Load software request data
    request_file = "../Software Request Analysis/softwareregionalrequests_with_sdlc.csv"
    df_requests = pd.read_csv(request_file)

    results = {}
    for region in ['North America', 'Latin America', 'Europe', 'Middle East & Africa', 'APAC']:
        region_data = df_requests[df_requests['region'] == region]

        # Calculate total software requests for this region
        total_requests = region_data['value'].sum()

        # Calculate Level 0 (highest complexity) requests
        level0_requests = region_data[region_data['level'] == 0]['value'].sum()

        # Calculate percentage
        level0_pct = (level0_requests / total_requests * 100) if total_requests > 0 else 0

        results[region] = {
            'level0_sw_pct': level0_pct,
            'total_sw_requests': int(total_requests),
            'level0_sw_requests': int(level0_requests)
        }

        print(f"  {region}: Level 0: {level0_pct:.1f}% ({int(level0_requests):,} / {int(total_requests):,})")

    return results

def create_regional_database():
    """Combine all metrics into standardized regional database."""
    print("\n" + "="*60)
    print("CREATING REGIONAL INPUT DATABASE")
    print("="*60)

    # Extract all metrics
    collab_metrics = extract_collaboration_metrics()
    efficiency_metrics = extract_efficiency_metrics()
    complexity_metrics = extract_complexity_metrics()

    # Combine into single database
    regions = ['North America', 'Latin America', 'Europe', 'Middle East & Africa', 'APAC']

    database = []
    for region in regions:
        row = {
            'region': region,
            'validation_pct': collab_metrics[region]['validation_pct'],
            'task_iteration_pct': collab_metrics[region]['task_iteration_pct'],
            'learning_pct': collab_metrics[region]['learning_pct'],
            'sw_prompt_length': efficiency_metrics[region]['sw_prompt_length'],
            'sw_completion_length': efficiency_metrics[region]['sw_completion_length'],
            'sw_cost_index': efficiency_metrics[region]['sw_cost_index'],
            'level0_sw_pct': complexity_metrics[region]['level0_sw_pct'],
            'total_sw_requests': complexity_metrics[region]['total_sw_requests'],
            'level0_sw_requests': complexity_metrics[region]['level0_sw_requests']
        }
        database.append(row)

    # Create DataFrame and save
    df_database = pd.DataFrame(database)
    output_file = "regional_inputs.csv"
    df_database.to_csv(output_file, index=False)

    print(f"\n✅ Regional input database created: {output_file}")
    print(f"   Database shape: {df_database.shape}")
    print(f"   Regions: {len(regions)}")
    print(f"   Metrics per region: {len(df_database.columns) - 1}")

    # Display summary
    print(f"\n📊 REGIONAL INPUT SUMMARY:")
    print("-" * 80)
    for _, row in df_database.iterrows():
        print(f"{row['region']:<20}: " +
              f"Validation {row['validation_pct']:5.1f}% | " +
              f"Task Iter {row['task_iteration_pct']:5.1f}% | " +
              f"Learning {row['learning_pct']:5.1f}% | " +
              f"Level0 {row['level0_sw_pct']:5.1f}%")

    return df_database

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("AI SOFTWARE MATURITY SCORE - DATA EXTRACTION")
    print("=" * 60)

    # Create the database
    database = create_regional_database()

    print(f"\n🎯 Next step: Implement scoring function and calculate maturity scores!")