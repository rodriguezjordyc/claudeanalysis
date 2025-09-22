#!/usr/bin/env python3
"""
Software Development Request Filter Script

This script filters regionalrequests_clean.csv to extract only software development
related requests based on keyword matching on cluster_name field.

Author: Regional Analysis Pipeline
Date: 2025-09-19
"""

import csv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def filter_software_requests():
    """
    Filter regionalrequests_clean.csv for software development requests only
    Output: softwareregionalrequests.csv with only request_count records
    """

    # Software development keywords for filtering
    software_keywords = [
        'software', 'application', 'app', 'program', 'programming', 'code', 'coding',
        'development', 'develop', 'developer', 'API', 'database', 'web', 'mobile',
        'chatbot', 'bot', 'debug', 'testing', 'deployment', 'integration',
        'AI', 'machine learning', 'ML', 'algorithm', 'game', 'gaming',
        'automation', 'script', 'website', 'dashboard', 'interface', 'UI', 'UX',
        'frontend', 'backend', 'full-stack', 'fullstack', 'server', 'cloud'
    ]

    input_file = '/Users/jordyrodriguez/Downloads/data/regionalrequests_clean.csv'
    output_file = '/Users/jordyrodriguez/Downloads/data/softwareregionalrequests.csv'

    # Statistics tracking
    stats = {
        'total_records': 0,
        'request_count_records': 0,
        'software_records': 0,
        'regions': {},
        'levels': {}
    }

    logger.info("Starting software development request filtering...")

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8', newline='') as outfile:

            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                stats['total_records'] += 1

                # Only process request_count records (exclude request_pct as requested)
                if row['variable'] == 'request_count':
                    stats['request_count_records'] += 1

                    # Check if cluster_name contains any software development keywords
                    cluster_name = row['cluster_name'].lower()
                    is_software = any(keyword.lower() in cluster_name for keyword in software_keywords)

                    if is_software:
                        stats['software_records'] += 1

                        # Track by region and level
                        region = row['region']
                        level = row['level']

                        stats['regions'][region] = stats['regions'].get(region, 0) + 1
                        stats['levels'][level] = stats['levels'].get(level, 0) + 1

                        # Write to output file
                        writer.writerow(row)

        # Generate summary report
        logger.info(f"Filtering completed successfully!")
        logger.info(f"Total input records: {stats['total_records']}")
        logger.info(f"Request count records: {stats['request_count_records']}")
        logger.info(f"Software development records found: {stats['software_records']}")
        logger.info(f"Software percentage: {stats['software_records']/stats['request_count_records']*100:.1f}%")

        print("\nFiltering Results Summary:")
        print("=" * 40)
        print(f"Total input records: {stats['total_records']}")
        print(f"Request count records: {stats['request_count_records']}")
        print(f"Software development records: {stats['software_records']}")
        print(f"Software percentage: {stats['software_records']/stats['request_count_records']*100:.1f}%")

        print(f"\nRecords by Region:")
        for region, count in sorted(stats['regions'].items()):
            print(f"  {region}: {count} records")

        print(f"\nRecords by Level:")
        for level, count in sorted(stats['levels'].items()):
            print(f"  Level {level}: {count} records ({count/stats['software_records']*100:.1f}%)")

        print(f"\nOutput file created: {output_file}")

    except Exception as e:
        logger.error(f"Error during filtering: {str(e)}")
        raise

def main():
    """Main execution function"""
    try:
        filter_software_requests()
        print("\n✅ Software development filtering completed successfully!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())