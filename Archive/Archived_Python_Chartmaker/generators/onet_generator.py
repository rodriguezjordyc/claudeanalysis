#!/usr/bin/env python3
"""
ONET Domain Analysis Chart Generator

Generates publication-quality charts for the Regional Domain Analysis.
"""

import pandas as pd
import numpy as np
import os
import sys

# Add parent directories to path for imports
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.extend([parent_dir, os.path.join(parent_dir, 'config'), os.path.join(parent_dir, 'core')])

from branding import *
from data_sources import get_data_path
from chart_base import BaseChart, RegionalRankingChart
import matplotlib.pyplot as plt

class OnetAnalysisGenerator:
    """Generate all charts for Regional Domain Analysis."""

    def __init__(self, output_dir=None):
        """Initialize with output directory."""
        self.output_dir = output_dir or os.path.join(parent_dir, 'outputs', 'onet_analysis')
        os.makedirs(self.output_dir, exist_ok=True)

        # Load data
        self.data = pd.read_csv(get_data_path('domain_regional'))
        print(f"📊 Loaded domain data: {self.data.shape[0]} records")

    def generate_domain_distribution_chart(self):
        """Generate domain distribution by region chart."""
        print("📊 Generating domain distribution chart...")

        # Filter for domain data with meaningful percentages
        domain_data = self.data[
            (self.data['variable'] == 'domain_count') &
            (~self.data['domain'].isin(['none', 'not_classified'])) &
            (self.data['percentage'] > 0)
        ].copy()

        chart = DomainDistributionChart(
            title="Regional Domain Distribution\\nOccupational Domain Demand by Region",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=domain_data,
            region_col='region',
            domain_col='domain',
            percentage_col='percentage',
            xlabel='Region',
            ylabel='Percentage of Domain Tasks (%)'
        )

        # Save in multiple formats
        saved_files = chart.save('01_domain_distribution', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_software_development_focus_ranking(self):
        """Generate software development focus ranking chart."""
        print("🏆 Generating software development focus ranking chart...")

        # Get software development percentages by region
        sw_dev_data = self.data[
            (self.data['variable'] == 'domain_count') &
            (self.data['domain'] == 'Software_Development')
        ].copy()

        sw_dev_data = sw_dev_data.sort_values('percentage', ascending=False)
        sw_dev_data['rank'] = range(1, len(sw_dev_data) + 1)

        chart = RegionalRankingChart(
            title="Regional Software Development Focus Rankings\\nPercentage of Tasks in Software Development Domain",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=sw_dev_data,
            score_col='percentage',
            rank_col='rank',
            region_col='region',
            xlabel='Software Development Focus (%)',
            ylabel='Region'
        )

        saved_files = chart.save('02_software_development_ranking', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_top_domains_comparison(self):
        """Generate top domains comparison across regions."""
        print("📊 Generating top domains comparison chart...")

        # Get top domains overall
        domain_totals = self.data[
            (self.data['variable'] == 'domain_count') &
            (~self.data['domain'].isin(['none', 'not_classified']))
        ].groupby('domain')['value'].sum().sort_values(ascending=False)

        top_domains = domain_totals.head(6).index.tolist()

        # Filter data for top domains
        top_domain_data = self.data[
            (self.data['variable'] == 'domain_count') &
            (self.data['domain'].isin(top_domains))
        ].copy()

        chart = TopDomainsChart(
            title="Top Domain Categories by Region\\nComparison of Most Demanded Occupational Domains",
            figsize='wide',
            output_dir=self.output_dir
        )

        chart.generate(
            data=top_domain_data,
            region_col='region',
            domain_col='domain',
            percentage_col='percentage',
            domains=top_domains,
            xlabel='Domain Category',
            ylabel='Percentage (%)'
        )

        saved_files = chart.save('03_top_domains_comparison', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_domain_diversity_analysis(self):
        """Generate domain diversity analysis chart."""
        print("📊 Generating domain diversity analysis chart...")

        # Calculate domain diversity metrics for each region
        domain_data = self.data[
            (self.data['variable'] == 'domain_count') &
            (~self.data['domain'].isin(['none', 'not_classified'])) &
            (self.data['percentage'] > 0)
        ].copy()

        diversity_metrics = []
        for region in domain_data['region'].unique():
            region_data = domain_data[domain_data['region'] == region]

            # Calculate Shannon diversity index
            percentages = region_data['percentage'] / 100.0  # Convert to proportions
            shannon_index = -sum(p * np.log(p) for p in percentages if p > 0)

            # Count of domains with >5% representation
            significant_domains = len(region_data[region_data['percentage'] >= 5.0])

            diversity_metrics.append({
                'region': region,
                'shannon_diversity': shannon_index,
                'significant_domains': significant_domains,
                'total_domains': len(region_data)
            })

        diversity_df = pd.DataFrame(diversity_metrics)
        diversity_df = diversity_df.sort_values('shannon_diversity', ascending=False)
        diversity_df['diversity_rank'] = range(1, len(diversity_df) + 1)

        chart = RegionalRankingChart(
            title="Regional Domain Diversity Rankings\\nShannon Diversity Index for Occupational Domains",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=diversity_df,
            score_col='shannon_diversity',
            rank_col='diversity_rank',
            region_col='region',
            xlabel='Shannon Diversity Index',
            ylabel='Region'
        )

        saved_files = chart.save('04_domain_diversity', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_domain_profiles_table(self):
        """Generate detailed domain profiles summary table."""
        print("📋 Generating domain profiles table...")

        # Create comprehensive summary table
        domain_data = self.data[
            (self.data['variable'] == 'domain_count') &
            (~self.data['domain'].isin(['none', 'not_classified']))
        ].copy()

        # Pivot data for easier processing
        pivot_data = domain_data.pivot_table(
            index='region',
            columns='domain',
            values='percentage',
            fill_value=0
        ).reset_index()

        # Select top domains for the summary
        domain_totals = domain_data.groupby('domain')['value'].sum().sort_values(ascending=False)
        top_domains = domain_totals.head(8).index.tolist()

        summary_data = []
        for _, row in pivot_data.iterrows():
            summary = {
                'Region': row['region'],
                'Software Development %': f"{row.get('Software_Development', 0):.1f}%",
                'Education Training %': f"{row.get('Education_Training', 0):.1f}%",
                'Research Analysis %': f"{row.get('Research_Analysis', 0):.1f}%",
                'Administrative Support %': f"{row.get('Administrative_Support', 0):.1f}%",
                'Customer Service %': f"{row.get('Customer_Service', 0):.1f}%",
                'Business Management %': f"{row.get('Business_Management', 0):.1f}%",
                'Creative Communications %': f"{row.get('Creative_Communications', 0):.1f}%",
                'Healthcare %': f"{row.get('Healthcare', 0):.1f}%"
            }
            summary_data.append(summary)

        # Sort by software development percentage
        summary_df = pd.DataFrame(summary_data)
        summary_df['sort_key'] = summary_df['Software Development %'].str.replace('%', '').astype(float)
        summary_df = summary_df.sort_values('sort_key', ascending=False).drop('sort_key', axis=1)
        summary_df.insert(0, 'Rank', range(1, len(summary_df) + 1))

        # Save as CSV
        csv_path = os.path.join(self.output_dir, '05_domain_profiles.csv')
        summary_df.to_csv(csv_path, index=False)
        print(f"   ✅ Saved: {os.path.basename(csv_path)}")

        return csv_path

    def generate_insights_summary(self):
        """Generate key insights and findings summary."""
        print("💡 Generating insights summary...")

        domain_data = self.data[
            (self.data['variable'] == 'domain_count') &
            (~self.data['domain'].isin(['none', 'not_classified']))
        ].copy()

        # Find leaders in key domains
        sw_dev_leader = domain_data[domain_data['domain'] == 'Software_Development'].loc[
            domain_data[domain_data['domain'] == 'Software_Development']['percentage'].idxmax(), 'region'
        ]

        education_leader = domain_data[domain_data['domain'] == 'Education_Training'].loc[
            domain_data[domain_data['domain'] == 'Education_Training']['percentage'].idxmax(), 'region'
        ]

        # Calculate totals
        total_tasks = domain_data['value'].sum()
        sw_dev_total = domain_data[domain_data['domain'] == 'Software_Development']['value'].sum()

        insights = {
            'Analysis': 'Regional Domain Analysis',
            'Methodology': 'Occupational domain classification of software development requests',
            'Total Regions': domain_data['region'].nunique(),
            'Total Domain Categories': domain_data['domain'].nunique(),
            'Software Development Leader': sw_dev_leader,
            'Highest SW Dev %': f"{domain_data[domain_data['domain'] == 'Software_Development']['percentage'].max():.1f}%",
            'Education Training Leader': education_leader,
            'Total Tasks Analyzed': f"{int(total_tasks):,}",
            'Software Development Tasks': f"{int(sw_dev_total):,}",
            'SW Dev Overall %': f"{(sw_dev_total/total_tasks)*100:.1f}%"
        }

        # Save insights
        insights_path = os.path.join(self.output_dir, '06_domain_insights.txt')
        with open(insights_path, 'w') as f:
            f.write("REGIONAL DOMAIN ANALYSIS - KEY INSIGHTS\\n")
            f.write("=" * 50 + "\\n\\n")
            for key, value in insights.items():
                f.write(f"{key}: {value}\\n")

        print(f"   ✅ Saved: {os.path.basename(insights_path)}")
        return insights_path

    def generate_all_charts(self):
        """Generate all charts for Regional Domain Analysis."""
        print("\\n🚀 GENERATING REGIONAL DOMAIN ANALYSIS CHARTS")
        print("=" * 60)

        generated_files = []

        try:
            # Generate all chart types
            generated_files.extend(self.generate_domain_distribution_chart())
            generated_files.extend(self.generate_software_development_focus_ranking())
            generated_files.extend(self.generate_top_domains_comparison())
            generated_files.extend(self.generate_domain_diversity_analysis())
            generated_files.append(self.generate_domain_profiles_table())
            generated_files.append(self.generate_insights_summary())

            print(f"\\n✅ Successfully generated {len(generated_files)} files")
            print(f"📁 Output directory: {self.output_dir}")

            return generated_files

        except Exception as e:
            print(f"\\n❌ Error generating charts: {str(e)}")
            raise

class DomainDistributionChart(BaseChart):
    """Stacked bar chart for domain distribution by region."""

    def generate(self, data, region_col='region', domain_col='domain',
                percentage_col='percentage', **kwargs):
        """Generate stacked domain distribution chart."""

        # Pivot data for stacked bar chart
        pivot_data = data.pivot_table(
            index=region_col,
            columns=domain_col,
            values=percentage_col,
            fill_value=0
        )

        # Get top domains to limit chart complexity
        domain_sums = pivot_data.sum().sort_values(ascending=False)
        top_domains = domain_sums.head(8).index.tolist()

        # Domain colors (using component colors for variety)
        domain_colors = {
            'Software_Development': '#2E86AB',
            'Education_Training': '#5C946E',
            'Research_Analysis': '#F18F01',
            'Administrative_Support': '#A23B72',
            'Customer_Service': '#C73E1D',
            'Business_Management': '#8B2F5E',
            'Creative_Communications': '#2ECC71',
            'Healthcare': '#E74C3C'
        }

        colors = [domain_colors.get(domain, '#BDC3C7') for domain in top_domains]

        # Create stacked bar chart
        ax = pivot_data[top_domains].plot(
            kind='bar',
            stacked=True,
            ax=self.ax,
            color=colors,
            width=0.7,
            **BAR_SETTINGS
        )

        # Customize legend labels
        domain_labels = {
            'Software_Development': 'Software Development',
            'Education_Training': 'Education & Training',
            'Research_Analysis': 'Research & Analysis',
            'Administrative_Support': 'Administrative Support',
            'Customer_Service': 'Customer Service',
            'Business_Management': 'Business Management',
            'Creative_Communications': 'Creative & Communications',
            'Healthcare': 'Healthcare'
        }

        ax.legend([domain_labels.get(d, d.replace('_', ' ').title()) for d in top_domains],
                 title='Domain Categories',
                 loc='upper right',
                 bbox_to_anchor=(1.0, 1.0))

        # Apply styling
        self.apply_styling(
            xlabel=kwargs.get('xlabel', 'Region'),
            ylabel=kwargs.get('ylabel', 'Percentage (%)'),
            grid=kwargs.get('grid', True)
        )

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')

        self._generated = True
        return self

class TopDomainsChart(BaseChart):
    """Grouped bar chart for top domains comparison."""

    def generate(self, data, region_col='region', domain_col='domain',
                percentage_col='percentage', domains=None, **kwargs):
        """Generate top domains comparison chart."""

        if domains is None:
            domains = data[domain_col].unique()

        # Filter and pivot data
        filtered_data = data[data[domain_col].isin(domains)]
        pivot_data = filtered_data.pivot_table(
            index=domain_col,
            columns=region_col,
            values=percentage_col,
            fill_value=0
        )

        # Get regional colors
        regions = pivot_data.columns.tolist()
        colors = get_regional_colors(regions)

        # Create grouped bar chart
        ax = pivot_data.plot(
            kind='bar',
            ax=self.ax,
            color=colors,
            width=0.8,
            **BAR_SETTINGS
        )

        # Create legend
        create_legend(self.ax, title='Regions', loc='upper right')

        # Apply styling
        self.apply_styling(
            xlabel=kwargs.get('xlabel', 'Domain Category'),
            ylabel=kwargs.get('ylabel', 'Percentage (%)'),
            grid=kwargs.get('grid', True)
        )

        # Improve x-axis labels
        domain_labels = [d.replace('_', ' ').title() for d in domains]
        ax.set_xticklabels(domain_labels, rotation=45, ha='right')

        self._generated = True
        return self

def main():
    """Generate all Regional Domain Analysis charts."""
    generator = OnetAnalysisGenerator()
    return generator.generate_all_charts()

if __name__ == "__main__":
    main()