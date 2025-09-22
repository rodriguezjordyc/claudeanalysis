#!/usr/bin/env python3
"""
Regional Aggregation Pipeline

This script aggregates country-level Claude usage data to regional level following
a specific methodology for different facets:
- Country facet: Simple sum for counts, recalculate percentages
- Onet_task facet: Weighted average for percentages using country usage_count as weights
- Collaboration facet: Weighted average for percentages using country usage_count as weights

Author: Regional Analysis Pipeline
Date: 2025-09-19
"""

import csv
import logging
from typing import Dict, Tuple, List, Any
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegionalAggregator:
    """Main class for regional data aggregation"""

    def __init__(self, claude_csv_path: str, regions_csv_path: str, output_dir: str = "."):
        """
        Initialize the aggregator with data paths

        Args:
            claude_csv_path: Path to claude.csv file
            regions_csv_path: Path to regions.csv file
            output_dir: Directory for output files
        """
        self.claude_csv_path = claude_csv_path
        self.regions_csv_path = regions_csv_path
        self.output_dir = Path(output_dir)

        # Target facets for processing
        self.target_facets = ["country", "onet_task", "collaboration"]

        # Initialize data containers
        self.claude_data = []
        self.regions_mapping = {}
        self.country_weights = {}
        self.regional_results = []
        self.validation_results = {}

    def load_data(self) -> None:
        """Load and validate input data files"""
        logger.info("Loading input data files...")

        try:
            # Load claude data
            with open(self.claude_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.claude_data = [row for row in reader if row['facet'] in self.target_facets]

            logger.info(f"Loaded {len(self.claude_data)} rows from claude.csv (filtered to target facets)")

            # Load regions mapping
            with open(self.regions_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.regions_mapping[row['country_id']] = row['Region']

            logger.info(f"Loaded {len(self.regions_mapping)} region mappings from regions.csv")

            # Validate that we have data
            if not self.claude_data:
                raise ValueError("No data found with target facets")

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def extract_country_weights(self) -> None:
        """Extract usage_count weights from country facet for weighted averaging"""
        logger.info("Extracting country usage weights...")

        # Get country usage counts for weighting
        for row in self.claude_data:
            if row['facet'] == 'country' and row['variable'] == 'usage_count':
                self.country_weights[row['geo_id']] = float(row['value'])

        if not self.country_weights:
            raise ValueError("No country usage_count data found for weighting")

        logger.info(f"Extracted weights for {len(self.country_weights)} countries")

        # Log sample weights for verification
        sample_weights = dict(list(self.country_weights.items())[:5])
        logger.info(f"Sample country weights: {sample_weights}")

    def aggregate_country_facet(self, region_data: List[Dict], region_name: str) -> List[Dict]:
        """
        Aggregate country facet data - simple sum for counts, recalculate percentages

        Args:
            region_data: Data for specific region
            region_name: Name of the region

        Returns:
            List of aggregated records
        """
        results = []

        # Filter to country facet data
        country_facet_data = [row for row in region_data if row['facet'] == 'country']

        if not country_facet_data:
            logger.warning(f"No country facet data for region {region_name}")
            return results

        # Group by variable
        variables = {}
        for row in country_facet_data:
            variable = row['variable']
            if variable not in variables:
                variables[variable] = []
            variables[variable].append(row)

        # Store regional usage_count for percentage calculation
        regional_usage_count = 0

        for variable, var_data in variables.items():
            if variable == 'usage_count':
                # Sum the counts
                total_value = sum(float(row['value']) for row in var_data)
                regional_usage_count = total_value  # Store for percentage calculation
                contributing_countries = [row['geo_id'] for row in var_data]

                results.append({
                    'region': region_name,
                    'facet': 'country',
                    'level': var_data[0]['level'],
                    'variable': variable,
                    'cluster_name': '',
                    'value': total_value,
                    'calculation_method': 'sum',
                    'contributing_countries': ','.join(contributing_countries),
                    'regional_weight': len(contributing_countries)
                })

        # Store regional usage count for later calculation
        self._regional_usage_counts = getattr(self, '_regional_usage_counts', {})
        self._regional_usage_counts[region_name] = regional_usage_count

        return results

    def calculate_country_facet_percentages(self) -> None:
        """
        Calculate country facet usage_pct after all regions are processed
        This ensures percentages sum to 100% across all regions
        """
        # Calculate total global usage count
        total_global_usage_count = sum(self._regional_usage_counts.values())

        if total_global_usage_count == 0:
            logger.warning("Total global usage count is zero, cannot calculate percentages")
            return

        # Find and update country facet usage_pct records
        for result in self.regional_results:
            if result['facet'] == 'country' and result['variable'] == 'usage_count':
                region_name = result['region']
                regional_usage_count = result['value']

                # Calculate percentage: (regional_usage_count / total_global_usage_count) × 100
                usage_pct = (regional_usage_count / total_global_usage_count) * 100

                # Find the corresponding country facet data and get contributing countries
                contributing_countries = result['contributing_countries']
                level = result['level']

                # Add the usage_pct record
                pct_record = {
                    'region': region_name,
                    'facet': 'country',
                    'level': level,
                    'variable': 'usage_pct',
                    'cluster_name': '',
                    'value': usage_pct,
                    'calculation_method': 'recalculated_percentage',
                    'contributing_countries': contributing_countries,
                    'regional_weight': regional_usage_count
                }

                self.regional_results.append(pct_record)

        logger.info("Country facet usage_pct recalculated based on regional usage counts")

    def aggregate_weighted_facet(self, region_data: List[Dict], region_name: str, facet_name: str) -> List[Dict]:
        """
        Aggregate onet_task or collaboration facets using weighted averages

        Args:
            region_data: Data for specific region
            region_name: Name of the region
            facet_name: Name of the facet (onet_task or collaboration)

        Returns:
            List of aggregated records
        """
        results = []

        # Filter to specific facet data
        facet_data = [row for row in region_data if row['facet'] == facet_name]

        if not facet_data:
            logger.warning(f"No {facet_name} facet data for region {region_name}")
            return results

        # Group by variable and cluster_name
        groups = {}
        for row in facet_data:
            key = (row['variable'], row['cluster_name'])
            if key not in groups:
                groups[key] = []
            groups[key].append(row)

        for (variable, cluster_name), group in groups.items():
            # Get weights for countries in this group
            weights = []
            values = []
            contributing_countries = []

            for row in group:
                weight = self.country_weights.get(row['geo_id'], 0)
                if weight > 0:  # Only include countries with positive weights
                    weights.append(weight)
                    values.append(float(row['value']))
                    contributing_countries.append(row['geo_id'])

            if not weights:
                logger.warning(f"No valid weights for {facet_name} {variable} {cluster_name} in region {region_name}")
                continue

            # Calculate weighted average
            total_weight = sum(weights)
            weighted_avg = sum(val * weight for val, weight in zip(values, weights)) / total_weight

            # Determine calculation method based on variable type
            if variable.endswith('_count'):
                calc_method = 'weighted_sum'
                # For counts, we want weighted sum proportional to regional weight
                region_geo_ids = list(set(row['geo_id'] for row in region_data))
                regional_total_weight = sum(self.country_weights.get(geo_id, 0) for geo_id in region_geo_ids)
                if regional_total_weight > 0:
                    weighted_avg = sum(val * weight for val, weight in zip(values, weights)) / regional_total_weight * total_weight
            else:
                calc_method = 'weighted_average'

            results.append({
                'region': region_name,
                'facet': facet_name,
                'level': group[0]['level'],
                'variable': variable,
                'cluster_name': cluster_name if cluster_name else '',
                'value': weighted_avg,
                'calculation_method': calc_method,
                'contributing_countries': ','.join(contributing_countries),
                'regional_weight': total_weight
            })

        return results

    def aggregate_by_region(self) -> None:
        """Main aggregation logic - process each region"""
        logger.info("Starting regional aggregation...")

        # Initialize regional usage counts storage
        self._regional_usage_counts = {}

        # Group data by region
        regions = {}
        for row in self.claude_data:
            region = row['region']
            if region not in regions:
                regions[region] = []
            regions[region].append(row)

        for region_name, region_data in regions.items():
            logger.info(f"Processing region: {region_name}")

            # Aggregate country facet (usage_count only)
            country_results = self.aggregate_country_facet(region_data, region_name)
            self.regional_results.extend(country_results)

            # Aggregate onet_task facet
            onet_results = self.aggregate_weighted_facet(region_data, region_name, 'onet_task')
            self.regional_results.extend(onet_results)

            # Aggregate collaboration facet
            collab_results = self.aggregate_weighted_facet(region_data, region_name, 'collaboration')
            self.regional_results.extend(collab_results)

            logger.info(f"Completed region {region_name}: {len(country_results + onet_results + collab_results)} records")

        # Calculate country facet percentages after processing all regions
        self.calculate_country_facet_percentages()

        logger.info(f"Total aggregated records: {len(self.regional_results)}")

    def validate_results(self) -> None:
        """Validate aggregated results"""
        logger.info("Validating aggregated results...")

        validation_issues = []

        # Group results by region for validation
        region_results = {}
        for result in self.regional_results:
            region = result['region']
            if region not in region_results:
                region_results[region] = []
            region_results[region].append(result)

        # Check percentage sums for collaboration and onet_task facets
        for region, results in region_results.items():
            for facet in ['collaboration', 'onet_task']:
                pct_results = [r for r in results if r['facet'] == facet and r['variable'].endswith('_pct')]

                if pct_results:
                    pct_sum = sum(float(r['value']) for r in pct_results)
                    if abs(pct_sum - 100.0) > 5.0:  # Allow 5% tolerance
                        validation_issues.append(
                            f"Region {region}, facet {facet}: percentage sum = {pct_sum:.2f}% (expected ~100%)"
                        )

        # Check that country facet usage_pct sums to 100% across all regions
        country_pct_results = [r for r in self.regional_results if r['facet'] == 'country' and r['variable'] == 'usage_pct']
        if country_pct_results:
            total_country_pct = sum(float(r['value']) for r in country_pct_results)
            if abs(total_country_pct - 100.0) > 1.0:  # Allow 1% tolerance for rounding
                validation_issues.append(
                    f"Country facet global percentage sum = {total_country_pct:.2f}% (expected ~100%)"
                )
            else:
                logger.info(f"Country facet usage_pct validation passed: {total_country_pct:.2f}%")

        # Check for missing regions from original data
        original_regions = set(row['region'] for row in self.claude_data)
        result_regions = set(r['region'] for r in self.regional_results)
        missing_regions = original_regions - result_regions

        if missing_regions:
            validation_issues.append(f"Missing regions in results: {missing_regions}")

        # Store validation results
        unique_regions = set(r['region'] for r in self.regional_results)
        unique_facets = set(r['facet'] for r in self.regional_results)

        self.validation_results = {
            'total_records': len(self.regional_results),
            'regions_processed': len(unique_regions),
            'facets_processed': list(unique_facets),
            'validation_issues': validation_issues,
            'percentage_validation_passed': len(validation_issues) == 0
        }

        if validation_issues:
            logger.warning(f"Validation issues found: {len(validation_issues)}")
            for issue in validation_issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("All validation checks passed!")

    def save_results(self) -> None:
        """Save results to output files"""
        logger.info("Saving results to output files...")

        # Save main results
        output_file = self.output_dir / "regionanalysis.csv"
        fieldnames = ['region', 'facet', 'level', 'variable', 'cluster_name', 'value',
                     'calculation_method', 'contributing_countries', 'regional_weight']

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.regional_results)

        logger.info(f"Saved {len(self.regional_results)} records to {output_file}")

        # Save validation report
        validation_file = self.output_dir / "validation_report.txt"
        with open(validation_file, 'w') as f:
            f.write("Regional Aggregation Validation Report\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Processing Date: {datetime.now()}\n")
            f.write(f"Total Records: {self.validation_results['total_records']}\n")
            f.write(f"Regions Processed: {self.validation_results['regions_processed']}\n")
            f.write(f"Facets Processed: {', '.join(self.validation_results['facets_processed'])}\n")
            f.write(f"Validation Status: {'PASSED' if self.validation_results['percentage_validation_passed'] else 'FAILED'}\n\n")

            if self.validation_results['validation_issues']:
                f.write("Validation Issues:\n")
                for issue in self.validation_results['validation_issues']:
                    f.write(f"  - {issue}\n")
            else:
                f.write("No validation issues found.\n")

            # Add summary statistics
            f.write("\nSummary Statistics:\n")
            f.write("-" * 20 + "\n")

            # Count by facet
            facet_counts = {}
            for result in self.regional_results:
                facet = result['facet']
                facet_counts[facet] = facet_counts.get(facet, 0) + 1

            for facet, count in facet_counts.items():
                f.write(f"{facet.capitalize()} records: {count}\n")

            # Count by region
            f.write(f"\nRecords by region:\n")
            region_counts = {}
            for result in self.regional_results:
                region = result['region']
                region_counts[region] = region_counts.get(region, 0) + 1

            for region, count in sorted(region_counts.items()):
                f.write(f"  {region}: {count}\n")

        logger.info(f"Saved validation report to {validation_file}")

    def run_pipeline(self) -> None:
        """Execute the complete aggregation pipeline"""
        logger.info("Starting regional aggregation pipeline...")

        try:
            # Load and validate data
            self.load_data()

            # Extract country weights for weighted averaging
            self.extract_country_weights()

            # Perform regional aggregation
            self.aggregate_by_region()

            # Validate results
            self.validate_results()

            # Save results
            self.save_results()

            logger.info("Regional aggregation pipeline completed successfully!")

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise


def main():
    """Main execution function"""
    # Set up file paths
    claude_csv = "/Users/jordyrodriguez/Downloads/data/claude.csv"
    regions_csv = "/Users/jordyrodriguez/Downloads/data/regions.csv"
    output_dir = "/Users/jordyrodriguez/Downloads/data"

    # Verify input files exist
    if not Path(claude_csv).exists():
        raise FileNotFoundError(f"Claude data file not found: {claude_csv}")
    if not Path(regions_csv).exists():
        raise FileNotFoundError(f"Regions mapping file not found: {regions_csv}")

    # Create aggregator and run pipeline
    aggregator = RegionalAggregator(claude_csv, regions_csv, output_dir)
    aggregator.run_pipeline()

    print("\n" + "="*50)
    print("REGIONAL AGGREGATION COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"Output files created:")
    print(f"  - regionanalysis.csv: {len(aggregator.regional_results)} aggregated records")
    print(f"  - validation_report.txt: Validation summary and statistics")
    print(f"  - regional_aggregation.py: This script")
    print("\nValidation Summary:")
    print(f"  - Regions processed: {aggregator.validation_results['regions_processed']}")
    print(f"  - Facets processed: {', '.join(aggregator.validation_results['facets_processed'])}")
    print(f"  - Validation status: {'PASSED' if aggregator.validation_results['percentage_validation_passed'] else 'FAILED'}")
    if aggregator.validation_results['validation_issues']:
        print(f"  - Issues found: {len(aggregator.validation_results['validation_issues'])}")


if __name__ == "__main__":
    main()