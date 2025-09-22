#!/usr/bin/env python3
"""
Improved Software Development Filter Script

This script filters the regional requests dataset to include only genuine software development
requests while excluding false positives from broad terms like 'development', 'application',
and 'program'.

The filter uses:
1. More precise software-specific keywords
2. Exclusion keywords to filter out non-software contexts
3. Combined positive and negative filtering logic
"""

import pandas as pd
import re

def create_improved_software_filter():
    """
    Creates improved software development filter with precise keywords and exclusions.

    Returns:
        tuple: (software_keywords, exclusion_keywords)
    """

    # More precise software development keywords (replacing broad terms)
    software_keywords = [
        # Specific development terms
        'software development', 'app development', 'web development',
        'mobile development', 'game development', 'API development',
        'frontend development', 'backend development', 'full stack development',

        # Programming and coding terms
        'programming language', 'code review', 'coding', 'programming',
        'debug', 'debugging', 'software program', 'software application',
        'web app', 'mobile app', 'software code', 'source code',

        # Technical terms
        'software', 'algorithm', 'database', 'API', 'framework',
        'library', 'repository', 'git', 'github', 'deployment',
        'containerization', 'docker', 'kubernetes', 'devops',

        # Specific technologies
        'python', 'javascript', 'java', 'react', 'vue', 'angular',
        'node.js', 'django', 'flask', 'spring', 'laravel', 'ruby',
        'php', 'c++', 'c#', 'swift', 'kotlin', 'flutter', 'dart',
        'html', 'css', 'sql', 'nosql', 'mongodb', 'postgresql',
        'mysql', 'redis', 'elasticsearch',

        # Development activities
        'unit test', 'testing', 'integration', 'ci/cd', 'build',
        'compile', 'refactor', 'optimization', 'performance tuning',
        'security vulnerability', 'penetration testing',

        # Software architecture
        'microservice', 'architecture', 'design pattern', 'mvc',
        'rest api', 'graphql', 'webhook', 'authentication',
        'authorization', 'encryption',

        # Development tools
        'ide', 'compiler', 'interpreter', 'package manager',
        'npm', 'pip', 'maven', 'gradle', 'webpack', 'babel',

        # Platforms and environments
        'cloud computing', 'aws', 'azure', 'gcp', 'heroku',
        'netlify', 'vercel', 'linux', 'ubuntu', 'centos',

        # AI/ML software development
        'machine learning', 'deep learning', 'neural network',
        'tensorflow', 'pytorch', 'scikit-learn', 'ai model',
        'data science', 'analytics', 'big data',

        # Specific software types
        'trading bot', 'chatbot', 'automation script', 'web scraping',
        'data pipeline', 'etl', 'batch processing', 'real-time processing',

        # UI/UX development
        'user interface', 'ui component', 'frontend component',
        'responsive design', 'user experience', 'ux design',

        # Blockchain and crypto development
        'blockchain', 'smart contract', 'cryptocurrency', 'defi',
        'nft', 'web3', 'solidity', 'ethereum'
    ]

    # Exclusion keywords to filter out non-software contexts
    exclusion_keywords = [
        # Educational/Academic contexts
        'language learning', 'foreign language', 'k-12 educational',
        'educational materials', 'teaching resources', 'curriculum',
        'instruction', 'learning program', 'training program',
        'academic research', 'academic writing', 'educational content',
        'student', 'teacher', 'classroom', 'school', 'university',
        'degree', 'course', 'lesson', 'homework', 'assignment',

        # Business/Professional development (non-technical)
        'professional development', 'business development',
        'personal development', 'career development', 'skill development',
        'leadership development', 'team development',
        'business consulting', 'strategic development', 'business strategy',
        'market development', 'sales development', 'marketing',

        # Document and content creation
        'business documents', 'formal reports', 'marketing materials',
        'promotional content', 'email drafts', 'resume', 'cv',
        'professional profiles', 'presentations', 'diagrams',
        'visual graphics', 'content creation',

        # Philosophy and abstract concepts
        'philosophical', 'philosophy', 'literature', 'creative writing',
        'poetry', 'fiction', 'non-fiction', 'storytelling',
        'theoretical', 'conceptual analysis',

        # Translation and language services
        'translate text', 'translation', 'multilingual', 'interpreter',
        'language services', 'localization',

        # Financial services (non-technical)
        'investment advice', 'financial education', 'financial planning',
        'portfolio management', 'wealth management', 'insurance',
        'banking services', 'loan', 'mortgage', 'credit',

        # General business operations
        'spreadsheet operations', 'excel operations', 'data entry',
        'administrative', 'clerical', 'bookkeeping', 'accounting',
        'human resources', 'recruitment', 'hiring',

        # Healthcare and medical (non-technical)
        'medical advice', 'health consultation', 'therapy',
        'counseling', 'wellness', 'fitness', 'nutrition',

        # Entertainment and media
        'entertainment content', 'media platforms', 'gaming support',
        'game strategy', 'entertainment', 'leisure',

        # Legal and compliance
        'legal advice', 'legal consultation', 'compliance',
        'regulatory', 'law', 'legal document',

        # Real estate and property
        'real estate', 'property', 'housing', 'rental',
        'lease', 'mortgage', 'property management'
    ]

    return software_keywords, exclusion_keywords

def is_software_development_request(cluster_name, software_keywords, exclusion_keywords):
    """
    Determines if a cluster name represents a software development request.

    Args:
        cluster_name (str): The cluster name to evaluate
        software_keywords (list): List of software-specific keywords
        exclusion_keywords (list): List of exclusion keywords

    Returns:
        bool: True if it's a software development request, False otherwise
    """
    cluster_lower = cluster_name.lower()

    # Check for software keywords
    has_software_keyword = any(keyword.lower() in cluster_lower for keyword in software_keywords)

    # Check for exclusion keywords
    has_exclusion_keyword = any(exclusion.lower() in cluster_lower for exclusion in exclusion_keywords)

    # Must have software keyword AND not have exclusion keyword
    return has_software_keyword and not has_exclusion_keyword

def generate_filtering_summary(original_df, filtered_df, software_keywords, exclusion_keywords):
    """
    Generates a summary of the filtering process.

    Args:
        original_df (pd.DataFrame): Original dataset
        filtered_df (pd.DataFrame): Filtered dataset
        software_keywords (list): Software keywords used
        exclusion_keywords (list): Exclusion keywords used

    Returns:
        dict: Summary statistics and examples
    """
    # Get unique cluster names for analysis
    original_clusters = set(original_df['cluster_name'].unique())
    filtered_clusters = set(filtered_df['cluster_name'].unique())
    excluded_clusters = original_clusters - filtered_clusters

    # Calculate statistics for request_count only
    original_count_data = original_df[original_df['variable'] == 'request_count']
    filtered_count_data = filtered_df[filtered_df['variable'] == 'request_count']

    summary = {
        'original_clusters': len(original_clusters),
        'filtered_clusters': len(filtered_clusters),
        'excluded_clusters': len(excluded_clusters),
        'original_records': len(original_count_data),
        'filtered_records': len(filtered_count_data),
        'excluded_records': len(original_count_data) - len(filtered_count_data),
        'retention_rate': len(filtered_count_data) / len(original_count_data) * 100,
        'software_keywords_count': len(software_keywords),
        'exclusion_keywords_count': len(exclusion_keywords)
    }

    # Get examples of excluded clusters
    excluded_examples = list(excluded_clusters)[:10]
    kept_examples = list(filtered_clusters)[:10]

    summary['excluded_examples'] = excluded_examples
    summary['kept_examples'] = kept_examples

    return summary

def main():
    """Main function to run the improved software development filter."""

    print("=== Improved Software Development Filter ===\n")

    # File paths
    input_file = "/Users/jordyrodriguez/Downloads/data/regionalrequests_clean.csv"
    output_file = "/Users/jordyrodriguez/Downloads/data/softwareregionalrequests.csv"

    # Load the data
    print("Loading data...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} records from {input_file}")

    # Get filter keywords
    software_keywords, exclusion_keywords = create_improved_software_filter()
    print(f"Using {len(software_keywords)} software keywords and {len(exclusion_keywords)} exclusion keywords")

    # Apply the filter
    print("\nApplying improved filter...")
    mask = df['cluster_name'].apply(
        lambda x: is_software_development_request(x, software_keywords, exclusion_keywords)
    )

    # Filter to only request_count records (no request_pct)
    count_mask = df['variable'] == 'request_count'
    final_mask = mask & count_mask

    filtered_df = df[final_mask].copy()

    # Generate summary
    summary = generate_filtering_summary(df, filtered_df, software_keywords, exclusion_keywords)

    # Save the filtered data
    filtered_df.to_csv(output_file, index=False)
    print(f"\nSaved {len(filtered_df)} filtered records to {output_file}")

    # Print summary
    print("\n=== FILTERING SUMMARY ===")
    print(f"Original clusters: {summary['original_clusters']}")
    print(f"Filtered clusters: {summary['filtered_clusters']}")
    print(f"Excluded clusters: {summary['excluded_clusters']}")
    print(f"Original records (request_count): {summary['original_records']}")
    print(f"Filtered records (request_count): {summary['filtered_records']}")
    print(f"Excluded records: {summary['excluded_records']}")
    print(f"Retention rate: {summary['retention_rate']:.1f}%")
    print(f"Software keywords used: {summary['software_keywords_count']}")
    print(f"Exclusion keywords used: {summary['exclusion_keywords_count']}")

    print("\n=== EXAMPLES OF EXCLUDED CLUSTERS ===")
    for i, cluster in enumerate(summary['excluded_examples'], 1):
        print(f"{i:2d}. {cluster}")

    print("\n=== EXAMPLES OF KEPT CLUSTERS ===")
    for i, cluster in enumerate(summary['kept_examples'], 1):
        print(f"{i:2d}. {cluster}")

    print(f"\n=== FILTERING COMPLETE ===")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()