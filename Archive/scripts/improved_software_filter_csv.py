#!/usr/bin/env python3
"""
Improved Software Development Filter Script (CSV-based)

This script filters the regional requests dataset to include only genuine software development
requests while excluding false positives from broad terms like 'development', 'application',
and 'program'. Uses only built-in Python CSV module.
"""

import csv
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

def main():
    """Main function to run the improved software development filter."""

    print("=== Improved Software Development Filter ===\n")

    # File paths
    input_file = "/Users/jordyrodriguez/Downloads/data/regionalrequests_clean.csv"
    output_file = "/Users/jordyrodriguez/Downloads/data/softwareregionalrequests.csv"

    # Get filter keywords
    software_keywords, exclusion_keywords = create_improved_software_filter()
    print(f"Using {len(software_keywords)} software keywords and {len(exclusion_keywords)} exclusion keywords")

    # Statistics tracking
    original_clusters = set()
    filtered_clusters = set()
    original_records = 0
    filtered_records = 0
    excluded_examples = []
    kept_examples = []

    print("\nApplying improved filter...")

    # Read input and write filtered output
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            cluster_name = row['cluster_name']
            variable = row['variable']

            # Track all clusters for statistics
            original_clusters.add(cluster_name)

            # Only process request_count records
            if variable == 'request_count':
                original_records += 1

                # Apply the software filter
                if is_software_development_request(cluster_name, software_keywords, exclusion_keywords):
                    writer.writerow(row)
                    filtered_records += 1
                    filtered_clusters.add(cluster_name)

                    # Collect examples of kept clusters
                    if len(kept_examples) < 10 and cluster_name not in kept_examples:
                        kept_examples.append(cluster_name)
                else:
                    # Collect examples of excluded clusters
                    if len(excluded_examples) < 10 and cluster_name not in excluded_examples:
                        excluded_examples.append(cluster_name)

    # Calculate excluded clusters
    excluded_clusters = original_clusters - filtered_clusters

    # Print summary
    print(f"\nSaved {filtered_records} filtered records to {output_file}")

    print("\n=== FILTERING SUMMARY ===")
    print(f"Original clusters: {len(original_clusters)}")
    print(f"Filtered clusters: {len(filtered_clusters)}")
    print(f"Excluded clusters: {len(excluded_clusters)}")
    print(f"Original records (request_count): {original_records}")
    print(f"Filtered records (request_count): {filtered_records}")
    print(f"Excluded records: {original_records - filtered_records}")
    print(f"Retention rate: {filtered_records / original_records * 100:.1f}%")
    print(f"Software keywords used: {len(software_keywords)}")
    print(f"Exclusion keywords used: {len(exclusion_keywords)}")

    print("\n=== EXAMPLES OF EXCLUDED CLUSTERS ===")
    for i, cluster in enumerate(excluded_examples, 1):
        print(f"{i:2d}. {cluster}")

    print("\n=== EXAMPLES OF KEPT CLUSTERS ===")
    for i, cluster in enumerate(kept_examples, 1):
        print(f"{i:2d}. {cluster}")

    print(f"\n=== FILTERING COMPLETE ===")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()