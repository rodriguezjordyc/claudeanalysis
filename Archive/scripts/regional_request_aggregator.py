#!/usr/bin/env python3
"""
Regional Request Aggregation Script
Generates comprehensive regional request patterns dataset for enterprise analysis.

Focuses on request facet aggregation across regions using weighted averages
for percentage variables and sum aggregation for count variables.

Uses only standard library modules for maximum compatibility.
"""

import csv
import json
from collections import defaultdict, Counter
from datetime import datetime

def load_and_validate_data(file_path):
    """Load claude.csv and validate data structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        print(f"✓ Loaded {len(data):,} rows from {file_path}")

        # Validate required columns
        if not data:
            raise ValueError("No data loaded from file")

        required_cols = ['region', 'geo_id', 'facet', 'level', 'variable', 'cluster_name', 'value']
        actual_cols = list(data[0].keys())
        missing_cols = [col for col in required_cols if col not in actual_cols]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Filter for request facet only
        request_data = [row for row in data if row['facet'] == 'request']
        print(f"✓ Filtered to {len(request_data):,} request facet rows")

        # Validate facet levels
        levels = sorted(set(row['level'] for row in request_data))
        print(f"✓ Found request facet levels: {levels}")

        # Validate variables
        variables = sorted(set(row['variable'] for row in request_data))
        print(f"✓ Found request variables: {variables}")

        return data, request_data

    except Exception as e:
        print(f"✗ Error loading data: {e}")
        raise

def extract_country_usage_weights(data):
    """Extract country usage counts for weighting calculations"""
    # Get country facet usage counts
    country_data = [
        row for row in data
        if row['facet'] == 'country' and row['variable'] == 'usage_count'
    ]

    if not country_data:
        print("⚠ Warning: No country usage data found. Using equal weights.")
        # Create equal weights for all countries
        countries = set(row['geo_id'] for row in data)
        weights = {country: 1.0 for country in countries}
    else:
        weights = {row['geo_id']: float(row['value']) for row in country_data}
        print(f"✓ Extracted usage weights for {len(weights)} countries")

    return weights

def aggregate_request_data_by_region(request_data, country_weights):
    """
    Aggregate request facet data by region using appropriate methods:
    - Count variables: Sum across countries
    - Percentage variables: Weighted average using country usage_count
    """
    # Group data by region, level, variable, cluster_name
    grouped_data = defaultdict(list)

    for row in request_data:
        key = (row['region'], row['level'], row['variable'], row['cluster_name'])
        grouped_data[key].append(row)

    aggregated_data = []

    for group_key, group_rows in grouped_data.items():
        region, level, variable, cluster_name = group_key

        # Get countries and their values in this group
        countries = [row['geo_id'] for row in group_rows]
        values = [float(row['value']) for row in group_rows]

        # Calculate weights for these countries
        group_weights = [country_weights.get(country, 1.0) for country in countries]
        total_weight = sum(group_weights)

        if variable.endswith('_count'):
            # Sum for count variables
            aggregated_value = sum(values)
            calculation_method = 'sum'
        elif variable.endswith('_pct'):
            # Weighted average for percentage variables
            if total_weight > 0:
                weighted_sum = sum(val * weight for val, weight in zip(values, group_weights))
                aggregated_value = weighted_sum / total_weight
            else:
                aggregated_value = sum(values) / len(values)
            calculation_method = 'weighted_average'
        else:
            # Default to weighted average for other variables
            if total_weight > 0:
                weighted_sum = sum(val * weight for val, weight in zip(values, group_weights))
                aggregated_value = weighted_sum / total_weight
            else:
                aggregated_value = sum(values) / len(values)
            calculation_method = 'weighted_average'

        # Calculate regional weight (proportion of total usage)
        total_country_weight = sum(country_weights.values()) if country_weights else len(set(row['geo_id'] for row in request_data))
        regional_weight = total_weight / total_country_weight

        aggregated_data.append({
            'region': region,
            'facet': 'request',
            'level': level,
            'variable': variable,
            'cluster_name': cluster_name,
            'value': aggregated_value,
            'calculation_method': calculation_method,
            'contributing_countries': ','.join(sorted(set(countries))),
            'regional_weight': regional_weight
        })

    print(f"✓ Generated {len(aggregated_data):,} regional aggregations")
    return aggregated_data

def generate_validation_report(original_data, request_data, regional_data, country_weights):
    """Generate comprehensive validation report"""
    report_lines = []
    report_lines.append("=== REGIONAL REQUEST AGGREGATION VALIDATION REPORT ===")
    report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Original data summary
    report_lines.append("1. SOURCE DATA SUMMARY")
    report_lines.append("-" * 50)
    report_lines.append(f"Total request facet records: {len(request_data):,}")

    countries = set(row['geo_id'] for row in request_data)
    regions = set(row['region'] for row in request_data)
    levels = sorted(set(row['level'] for row in request_data))
    variables = sorted(set(row['variable'] for row in request_data))

    report_lines.append(f"Unique countries: {len(countries)}")
    report_lines.append(f"Unique regions: {len(regions)}")
    report_lines.append(f"Request facet levels: {levels}")
    report_lines.append(f"Request variables: {variables}")
    report_lines.append("")

    # Coverage by region and level
    report_lines.append("2. COVERAGE BY REGION AND LEVEL")
    report_lines.append("-" * 50)
    coverage = defaultdict(int)
    for row in request_data:
        coverage[(row['region'], row['level'])] += 1

    for (region, level), count in sorted(coverage.items()):
        report_lines.append(f"  {region} - Level {level}: {count:,} records")
    report_lines.append("")

    # Cluster diversity by level
    report_lines.append("3. REQUEST CLUSTER DIVERSITY BY LEVEL")
    report_lines.append("-" * 50)
    cluster_by_level = defaultdict(set)
    for row in request_data:
        cluster_by_level[row['level']].add(row['cluster_name'])

    for level in sorted(cluster_by_level.keys()):
        unique_clusters = len(cluster_by_level[level])
        report_lines.append(f"  Level {level}: {unique_clusters} unique request clusters")
    report_lines.append("")

    # Regional aggregation summary
    report_lines.append("4. REGIONAL AGGREGATION SUMMARY")
    report_lines.append("-" * 50)
    report_lines.append(f"Total regional records generated: {len(regional_data):,}")

    agg_coverage = defaultdict(int)
    for row in regional_data:
        agg_coverage[(row['region'], row['level'])] += 1

    for (region, level), count in sorted(agg_coverage.items()):
        report_lines.append(f"  {region} - Level {level}: {count:,} aggregations")
    report_lines.append("")

    # Method distribution
    report_lines.append("5. AGGREGATION METHOD DISTRIBUTION")
    report_lines.append("-" * 50)
    method_counts = Counter(row['calculation_method'] for row in regional_data)
    total_records = len(regional_data)
    for method, count in method_counts.items():
        pct = (count / total_records) * 100
        report_lines.append(f"  {method}: {count:,} records ({pct:.1f}%)")
    report_lines.append("")

    # Regional weights
    report_lines.append("6. REGIONAL WEIGHT DISTRIBUTION")
    report_lines.append("-" * 50)
    regional_weights = {}
    for row in regional_data:
        if row['region'] not in regional_weights:
            regional_weights[row['region']] = row['regional_weight']

    for region, weight in sorted(regional_weights.items(), key=lambda x: x[1], reverse=True):
        pct = weight * 100
        report_lines.append(f"  {region}: {weight:.4f} ({pct:.2f}%)")
    report_lines.append("")

    # Country weights summary
    report_lines.append("7. COUNTRY USAGE WEIGHTS SUMMARY")
    report_lines.append("-" * 50)
    if country_weights:
        total_usage = sum(country_weights.values())
        top_countries = sorted(country_weights.items(), key=lambda x: x[1], reverse=True)[:10]
        report_lines.append(f"Total usage across all countries: {total_usage:,.0f}")
        report_lines.append("Top 10 countries by usage:")
        for country, usage in top_countries:
            pct = (usage / total_usage) * 100
            report_lines.append(f"  {country}: {usage:,.0f} ({pct:.2f}%)")
    else:
        report_lines.append("  No country usage weights available - used equal weighting")
    report_lines.append("")

    # Data quality checks
    report_lines.append("8. DATA QUALITY CHECKS")
    report_lines.append("-" * 50)

    # Check value ranges
    values = [row['value'] for row in regional_data]
    min_val, max_val = min(values), max(values)
    mean_val = sum(values) / len(values)
    report_lines.append(f"  Value range: {min_val:.2f} to {max_val:.2f}")
    report_lines.append(f"  Mean value: {mean_val:.2f}")

    # Check for negative values in counts
    count_values = [row['value'] for row in regional_data if row['variable'].endswith('_count')]
    negative_counts = sum(1 for val in count_values if val < 0)
    if negative_counts == 0:
        report_lines.append("  ✓ No negative values in count variables")
    else:
        report_lines.append(f"  ⚠ {negative_counts} negative values in count variables")

    # Check percentage ranges
    pct_values = [row['value'] for row in regional_data if row['variable'].endswith('_pct')]
    if pct_values:
        out_of_range = sum(1 for val in pct_values if val < 0 or val > 100)
        if out_of_range == 0:
            report_lines.append("  ✓ All percentage values in valid range (0-100)")
        else:
            report_lines.append(f"  ⚠ {out_of_range} percentage values outside 0-100 range")

    report_lines.append("")

    # Strategic insights
    report_lines.append("9. STRATEGIC INSIGHTS")
    report_lines.append("-" * 50)

    # Regional sophistication analysis (based on level 0 vs level 2 distribution)
    level_0_counts = defaultdict(float)
    level_2_counts = defaultdict(float)

    for row in regional_data:
        if row['level'] == '0' and row['variable'] == 'request_count':
            level_0_counts[row['region']] += row['value']
        elif row['level'] == '2' and row['variable'] == 'request_count':
            level_2_counts[row['region']] += row['value']

    sophistication_ratios = {}
    for region in level_0_counts:
        level_2_val = level_2_counts.get(region, 0)
        sophistication_ratios[region] = level_0_counts[region] / (level_2_val + 1)

    report_lines.append("  Regional request sophistication ranking (Level 0/Level 2 ratio):")
    for region, ratio in sorted(sophistication_ratios.items(), key=lambda x: x[1], reverse=True):
        report_lines.append(f"    {region}: {ratio:.2f}")

    report_lines.append("")
    report_lines.append("=== END OF VALIDATION REPORT ===")

    return "\n".join(report_lines)

def save_to_csv(data, file_path):
    """Save data to CSV file"""
    if not data:
        raise ValueError("No data to save")

    fieldnames = list(data[0].keys())

    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"✓ Saved {len(data):,} records to: {file_path}")

def main():
    """Main execution function"""
    print("🚀 Starting Regional Request Aggregation Process")
    print("=" * 60)

    # File paths
    input_file = '/Users/jordyrodriguez/Downloads/data/claude.csv'
    output_file = '/Users/jordyrodriguez/Downloads/data/regionalrequests.csv'
    validation_file = '/Users/jordyrodriguez/Downloads/data/request_aggregation_validation.txt'

    try:
        # Step 1: Load and validate data
        print("\n📊 Step 1: Loading and validating source data...")
        all_data, request_data = load_and_validate_data(input_file)

        # Step 2: Extract country usage weights
        print("\n⚖️ Step 2: Extracting country usage weights...")
        country_weights = extract_country_usage_weights(all_data)

        # Step 3: Process request facet data
        print("\n🎯 Step 3: Processing request facet data...")

        if not request_data:
            raise ValueError("No request facet data found in source file")

        print(f"✓ Found {len(request_data):,} request facet records")

        regions = sorted(set(row['region'] for row in request_data))
        levels = sorted(set(row['level'] for row in request_data))
        variables = sorted(set(row['variable'] for row in request_data))

        print(f"✓ Regions: {regions}")
        print(f"✓ Levels: {levels}")
        print(f"✓ Variables: {variables}")

        # Step 4: Aggregate data by region
        print("\n🔄 Step 4: Aggregating request data by region...")
        regional_data = aggregate_request_data_by_region(request_data, country_weights)

        # Step 5: Save results
        print("\n💾 Step 5: Saving results...")
        save_to_csv(regional_data, output_file)

        # Step 6: Generate validation report
        print("\n📋 Step 6: Generating validation report...")
        validation_report = generate_validation_report(all_data, request_data, regional_data, country_weights)

        with open(validation_file, 'w', encoding='utf-8') as f:
            f.write(validation_report)
        print(f"✓ Saved validation report to: {validation_file}")

        # Final summary
        print("\n🎉 REGIONAL REQUEST AGGREGATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📈 Generated {len(regional_data):,} regional request aggregations")

        unique_regions = set(row['region'] for row in regional_data)
        unique_levels = set(row['level'] for row in regional_data)
        unique_clusters = set(row['cluster_name'] for row in regional_data)

        print(f"🌍 Covering {len(unique_regions)} regions")
        print(f"📊 Across {len(unique_levels)} complexity levels")
        print(f"🏷️ With {len(unique_clusters)} unique request clusters")

        # Display sample results
        print("\n📋 Sample Results:")
        for i, row in enumerate(regional_data[:5]):
            print(f"  {i+1}. {row['region']} | Level {row['level']} | {row['variable']} | {row['cluster_name'][:50]}... | {row['value']:.2f}")

        return True

    except Exception as e:
        print(f"\n❌ Error in aggregation process: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)