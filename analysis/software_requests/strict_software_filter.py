#!/usr/bin/env python3
"""
Strict Software Development Filter

Creates a much more precise filter for software development requests by using
positive software indicators AND negative exclusions.
"""

import csv
import pandas as pd

def strict_software_filter():
    """Apply strict filtering for software development requests only"""

    input_file = 'softwareregionalrequests_clean.csv'
    output_file = 'softwareregionalrequests_strict.csv'

    # Very strict positive software keywords - must contain at least one
    software_required = [
        'code', 'coding', 'program', 'programming', 'script', 'scripting',
        'software', 'application', 'app development', 'web development',
        'API', 'database', 'SQL', 'algorithm', 'function', 'method',
        'debug', 'debugging', 'testing', 'unit test', 'integration',
        'framework', 'library', 'package', 'module', 'import',
        'variable', 'array', 'object', 'class', 'inheritance',
        'repository', 'git', 'commit', 'merge', 'pull request',
        'HTML', 'CSS', 'JavaScript', 'Python', 'Java', 'C++', 'C#',
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
        'mobile app', 'iOS app', 'Android app', 'web app',
        'backend', 'frontend', 'full-stack', 'microservice',
        'deployment', 'DevOps', 'CI/CD', 'container', 'Docker',
        'cloud computing', 'AWS', 'Azure', 'GCP',
        'machine learning model', 'neural network', 'AI model',
        'data structure', 'sorting algorithm', 'optimization',
        'security vulnerability', 'encryption', 'authentication'
    ]

    # Strong exclusion keywords - exclude if any are present
    exclusions = [
        'financial advice', 'investment', 'purchasing advice', 'buying guide',
        'travel', 'vacation', 'recipe', 'cooking', 'diet', 'nutrition',
        'medical', 'health', 'exercise', 'fitness', 'yoga',
        'legal advice', 'law', 'contract review', 'legal document',
        'language learning', 'translation', 'foreign language',
        'creative writing', 'story', 'poem', 'novel', 'fiction',
        'academic essay', 'research paper', 'homework', 'assignment',
        'business plan', 'marketing strategy', 'sales pitch',
        'personal relationship', 'dating', 'family', 'parenting',
        'home improvement', 'gardening', 'interior design',
        'automotive', 'car repair', 'vehicle', 'maintenance',
        'subtitle', 'video editing', 'image editing', 'photo',
        'music', 'audio', 'podcast', 'entertainment',
        'fashion', 'clothing', 'style', 'beauty',
        'sports', 'game strategy', 'hobby', 'craft',
        'philosophical', 'ethical dilemma', 'moral question',
        'single-digit number', 'random number', 'count to'
    ]

    # Load data
    df = pd.read_csv(input_file)
    print(f"Original records: {len(df)}")

    # Apply strict filtering
    def is_software_request(cluster_name):
        cluster_lower = cluster_name.lower()

        # Must have at least one strong software indicator
        has_software_keyword = any(keyword.lower() in cluster_lower for keyword in software_required)

        # Must not have any exclusion keywords
        has_exclusion = any(exclusion.lower() in cluster_lower for exclusion in exclusions)

        return has_software_keyword and not has_exclusion

    # Filter the data
    filtered_df = df[df['cluster_name'].apply(is_software_request)].copy()

    print(f"After strict filtering: {len(filtered_df)} records")
    print(f"Removed: {len(df) - len(filtered_df)} records")

    # Show some examples of what was removed
    removed_df = df[~df['cluster_name'].apply(is_software_request)]
    print(f"\nSample of removed clusters:")
    unique_removed = removed_df['cluster_name'].unique()[:10]
    for cluster in unique_removed:
        print(f"  - {cluster}")

    # Recalculate percentages for the filtered data
    results = []

    for region in filtered_df['region'].unique():
        for level in filtered_df['level'].unique():
            # Get request_count records for this region-level combination
            mask = ((filtered_df['region'] == region) &
                   (filtered_df['level'] == level) &
                   (filtered_df['variable'] == 'request_count'))

            group_data = filtered_df[mask].copy()

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
    strict_df = pd.DataFrame(results)

    # Sort by region, level, variable, value (descending for counts)
    strict_df = strict_df.sort_values(['region', 'level', 'variable', 'value'],
                                     ascending=[True, True, True, False])

    # Save to file
    strict_df.to_csv(output_file, index=False)

    print(f"\nStrict software-only data saved to: {output_file}")
    print(f"Final record count: {len(strict_df)}")

    # Validation
    print("\nValidation - Percentage sums by region and level:")
    for region in strict_df['region'].unique():
        for level in strict_df['level'].unique():
            pct_data = strict_df[(strict_df['region'] == region) &
                                (strict_df['level'] == level) &
                                (strict_df['variable'] == 'request_pct')]
            if len(pct_data) > 0:
                pct_sum = pct_data['value'].astype(float).sum()
                print(f"  {region}, Level {level}: {pct_sum:.6f}%")

if __name__ == "__main__":
    strict_software_filter()