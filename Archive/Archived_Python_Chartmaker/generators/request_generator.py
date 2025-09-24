#!/usr/bin/env python3
"""
Software Request Analysis Chart Generator

Generates publication-quality charts for the Software Request Analysis.
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

class RequestAnalysisGenerator:
    """Generate all charts for Software Request Analysis."""

    def __init__(self, output_dir=None):
        """Initialize with output directory."""
        self.output_dir = output_dir or os.path.join(parent_dir, 'outputs', 'request_analysis')
        os.makedirs(self.output_dir, exist_ok=True)

        # Load data
        self.data = pd.read_csv(get_data_path('software_requests'))
        print(f"📊 Loaded software request data: {self.data.shape[0]} records")

    def generate_sdlc_distribution_chart(self):
        """Generate SDLC stage distribution by region chart."""
        print("📊 Generating SDLC distribution chart...")

        # Aggregate by SDLC stage and region
        sdlc_data = self.data.groupby(['region', 'sdlc_stage'])['value'].sum().reset_index()

        # Calculate percentages within each region
        region_totals = sdlc_data.groupby('region')['value'].sum()
        sdlc_data['percentage'] = sdlc_data.apply(
            lambda row: (row['value'] / region_totals[row['region']]) * 100, axis=1
        )

        chart = SDLCDistributionChart(
            title="Software Development Lifecycle Stage Distribution\\nRequest Types by SDLC Stage and Region",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=sdlc_data,
            region_col='region',
            stage_col='sdlc_stage',
            percentage_col='percentage',
            xlabel='Region',
            ylabel='Percentage of Requests (%)'
        )

        # Save in multiple formats
        saved_files = chart.save('01_sdlc_distribution', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_request_volume_ranking(self):
        """Generate regional request volume ranking chart."""
        print("🏆 Generating request volume ranking chart...")

        # Calculate total request volume by region
        volume_data = self.data.groupby('region')['value'].sum().reset_index()
        volume_data.columns = ['region', 'total_requests']
        volume_data = volume_data.sort_values('total_requests', ascending=False)
        volume_data['rank'] = range(1, len(volume_data) + 1)

        chart = RegionalRankingChart(
            title="Regional Software Request Volume Rankings\\nTotal Number of Software Development Requests",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=volume_data,
            score_col='total_requests',
            rank_col='rank',
            region_col='region',
            xlabel='Total Requests (thousands)',
            ylabel='Region'
        )

        saved_files = chart.save('02_request_volume_ranking', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_testing_focus_analysis(self):
        """Generate testing and QA focus analysis."""
        print("📊 Generating testing focus analysis chart...")

        # Calculate testing percentage by region
        testing_data = self.data[self.data['sdlc_stage'] == '4_Testing_QA'].groupby('region')['value'].sum()
        total_data = self.data.groupby('region')['value'].sum()

        testing_percentages = (testing_data / total_data * 100).reset_index()
        testing_percentages.columns = ['region', 'testing_percentage']
        testing_percentages = testing_percentages.sort_values('testing_percentage', ascending=False)
        testing_percentages['rank'] = range(1, len(testing_percentages) + 1)

        chart = RegionalRankingChart(
            title="Regional Testing & QA Focus Rankings\\nPercentage of Requests in Testing/QA Stage",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=testing_percentages,
            score_col='testing_percentage',
            rank_col='rank',
            region_col='region',
            xlabel='Testing & QA Focus (%)',
            ylabel='Region'
        )

        saved_files = chart.save('03_testing_focus', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_top_request_types(self):
        """Generate top request types across regions."""
        print("📊 Generating top request types chart...")

        # Get top request types globally
        global_requests = self.data.groupby('cluster_name')['value'].sum().sort_values(ascending=False)
        top_requests = global_requests.head(8).index.tolist()

        # Get data for top request types by region
        top_request_data = self.data[self.data['cluster_name'].isin(top_requests)]
        regional_summary = top_request_data.groupby(['region', 'cluster_name'])['value'].sum().reset_index()

        chart = TopRequestTypesChart(
            title="Top Software Request Types by Region\\nMost Common Software Development Task Categories",
            figsize='wide',
            output_dir=self.output_dir
        )

        chart.generate(
            data=regional_summary,
            region_col='region',
            request_col='cluster_name',
            value_col='value',
            top_requests=top_requests[:6],  # Limit for readability
            xlabel='Request Type',
            ylabel='Number of Requests'
        )

        saved_files = chart.save('04_top_request_types', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_request_profiles_table(self):
        """Generate detailed request profiles summary table."""
        print("📋 Generating request profiles table...")

        # Create comprehensive summary by region
        regional_profiles = []

        for region in self.data['region'].unique():
            region_data = self.data[self.data['region'] == region]

            # Calculate SDLC stage percentages
            total_requests = region_data['value'].sum()
            sdlc_percentages = region_data.groupby('sdlc_stage')['value'].sum() / total_requests * 100

            # Get top request type
            top_request = region_data.groupby('cluster_name')['value'].sum().idxmax()
            top_request_count = region_data.groupby('cluster_name')['value'].sum().max()

            profile = {
                'Region': region,
                'Total Requests': f"{int(total_requests):,}",
                'Planning %': f"{sdlc_percentages.get('1_Planning_Requirements', 0):.1f}%",
                'Design %': f"{sdlc_percentages.get('2_Design_Architecture', 0):.1f}%",
                'Implementation %': f"{sdlc_percentages.get('3_Implementation_Coding', 0):.1f}%",
                'Testing %': f"{sdlc_percentages.get('4_Testing_QA', 0):.1f}%",
                'Deployment %': f"{sdlc_percentages.get('5_Deployment_Maintenance', 0):.1f}%",
                'Top Request Type': top_request[:50] + "..." if len(top_request) > 50 else top_request,
                'Top Request Count': f"{int(top_request_count):,}"
            }
            regional_profiles.append(profile)

        # Sort by total requests
        profiles_df = pd.DataFrame(regional_profiles)
        profiles_df['sort_key'] = profiles_df['Total Requests'].str.replace(',', '').astype(int)
        profiles_df = profiles_df.sort_values('sort_key', ascending=False).drop('sort_key', axis=1)
        profiles_df.insert(0, 'Rank', range(1, len(profiles_df) + 1))

        # Save as CSV
        csv_path = os.path.join(self.output_dir, '05_request_profiles.csv')
        profiles_df.to_csv(csv_path, index=False)
        print(f"   ✅ Saved: {os.path.basename(csv_path)}")

        return csv_path

    def generate_insights_summary(self):
        """Generate key insights and findings summary."""
        print("💡 Generating insights summary...")

        # Calculate key insights
        total_requests = self.data['value'].sum()
        volume_leader = self.data.groupby('region')['value'].sum().idxmax()
        highest_volume = self.data.groupby('region')['value'].sum().max()

        # SDLC stage analysis
        sdlc_totals = self.data.groupby('sdlc_stage')['value'].sum()
        dominant_stage = sdlc_totals.idxmax()

        # Testing focus analysis
        testing_data = self.data[self.data['sdlc_stage'] == '4_Testing_QA'].groupby('region')['value'].sum()
        total_by_region = self.data.groupby('region')['value'].sum()
        testing_leader = (testing_data / total_by_region).idxmax()

        insights = {
            'Analysis': 'Software Request Analysis',
            'Methodology': 'SDLC-based classification of software development requests',
            'Total Regions': self.data['region'].nunique(),
            'Total Requests': f"{int(total_requests):,}",
            'Volume Leader': volume_leader,
            'Highest Volume': f"{int(highest_volume):,}",
            'Dominant SDLC Stage': dominant_stage.replace('_', ' '),
            'Testing Focus Leader': testing_leader,
            'Average Requests per Region': f"{int(total_requests / self.data['region'].nunique()):,}",
            'Unique Request Types': self.data['cluster_name'].nunique()
        }

        # Save insights
        insights_path = os.path.join(self.output_dir, '06_request_insights.txt')
        with open(insights_path, 'w') as f:
            f.write("SOFTWARE REQUEST ANALYSIS - KEY INSIGHTS\\n")
            f.write("=" * 50 + "\\n\\n")
            for key, value in insights.items():
                f.write(f"{key}: {value}\\n")

        print(f"   ✅ Saved: {os.path.basename(insights_path)}")
        return insights_path

    def generate_all_charts(self):
        """Generate all charts for Software Request Analysis."""
        print("\\n🚀 GENERATING SOFTWARE REQUEST ANALYSIS CHARTS")
        print("=" * 60)

        generated_files = []

        try:
            # Generate all chart types
            generated_files.extend(self.generate_sdlc_distribution_chart())
            generated_files.extend(self.generate_request_volume_ranking())
            generated_files.extend(self.generate_testing_focus_analysis())
            generated_files.extend(self.generate_top_request_types())
            generated_files.append(self.generate_request_profiles_table())
            generated_files.append(self.generate_insights_summary())

            print(f"\\n✅ Successfully generated {len(generated_files)} files")
            print(f"📁 Output directory: {self.output_dir}")

            return generated_files

        except Exception as e:
            print(f"\\n❌ Error generating charts: {str(e)}")
            raise

class SDLCDistributionChart(BaseChart):
    """Stacked bar chart for SDLC stage distribution by region."""

    def generate(self, data, region_col='region', stage_col='sdlc_stage',
                percentage_col='percentage', **kwargs):
        """Generate stacked SDLC distribution chart."""

        # Pivot data for stacked bar chart
        pivot_data = data.pivot_table(
            index=region_col,
            columns=stage_col,
            values=percentage_col,
            fill_value=0
        )

        # Define SDLC stage order and colors
        stage_order = [
            '1_Planning_Requirements',
            '2_Design_Architecture',
            '3_Implementation_Coding',
            '4_Testing_QA',
            '5_Deployment_Maintenance'
        ]

        available_stages = [s for s in stage_order if s in pivot_data.columns]

        # SDLC stage colors (progression from planning to deployment)
        stage_colors = {
            '1_Planning_Requirements': '#2E86AB',    # Blue - Planning
            '2_Design_Architecture': '#5C946E',      # Green - Design
            '3_Implementation_Coding': '#F18F01',    # Orange - Implementation
            '4_Testing_QA': '#A23B72',               # Purple - Testing
            '5_Deployment_Maintenance': '#C73E1D'    # Red - Deployment
        }

        colors = [stage_colors.get(stage, '#BDC3C7') for stage in available_stages]

        # Create stacked bar chart
        ax = pivot_data[available_stages].plot(
            kind='bar',
            stacked=True,
            ax=self.ax,
            color=colors,
            width=0.7,
            **BAR_SETTINGS
        )

        # Customize legend labels
        stage_labels = {
            '1_Planning_Requirements': 'Planning & Requirements',
            '2_Design_Architecture': 'Design & Architecture',
            '3_Implementation_Coding': 'Implementation & Coding',
            '4_Testing_QA': 'Testing & QA',
            '5_Deployment_Maintenance': 'Deployment & Maintenance'
        }

        ax.legend([stage_labels.get(s, s.replace('_', ' ').title()) for s in available_stages],
                 title='SDLC Stages',
                 loc='upper right')

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

class TopRequestTypesChart(BaseChart):
    """Grouped bar chart for top request types comparison."""

    def generate(self, data, region_col='region', request_col='cluster_name',
                value_col='value', top_requests=None, **kwargs):
        """Generate top request types comparison chart."""

        if top_requests is None:
            top_requests = data[request_col].unique()

        # Filter and pivot data
        filtered_data = data[data[request_col].isin(top_requests)]
        pivot_data = filtered_data.pivot_table(
            index=request_col,
            columns=region_col,
            values=value_col,
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
            xlabel=kwargs.get('xlabel', 'Request Type'),
            ylabel=kwargs.get('ylabel', 'Number of Requests'),
            grid=kwargs.get('grid', True)
        )

        # Improve x-axis labels (truncate long request names)
        request_labels = []
        for req in top_requests:
            if len(req) > 30:
                request_labels.append(req[:27] + "...")
            else:
                request_labels.append(req)

        ax.set_xticklabels(request_labels, rotation=45, ha='right')

        self._generated = True
        return self

def main():
    """Generate all Software Request Analysis charts."""
    generator = RequestAnalysisGenerator()
    return generator.generate_all_charts()

if __name__ == "__main__":
    main()