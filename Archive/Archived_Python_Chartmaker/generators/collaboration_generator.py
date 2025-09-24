#!/usr/bin/env python3
"""
Collaboration Analysis Chart Generator

Generates publication-quality charts for the Regional Collaboration Analysis.
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

class CollaborationAnalysisGenerator:
    """Generate all charts for Regional Collaboration Analysis."""

    def __init__(self, output_dir=None):
        """Initialize with output directory."""
        self.output_dir = output_dir or os.path.join(parent_dir, 'outputs', 'collaboration_analysis')
        os.makedirs(self.output_dir, exist_ok=True)

        # Load data
        self.data = pd.read_csv(get_data_path('collaboration'))
        print(f"📊 Loaded collaboration data: {self.data.shape[0]} records")

    def generate_regional_patterns_chart(self):
        """Generate regional collaboration patterns chart."""
        print("🏆 Generating regional collaboration patterns chart...")

        # Filter for collaboration percentages
        collab_data = self.data[
            (self.data['variable'] == 'collaboration_pct') &
            (~self.data['cluster_name'].isin(['none', 'not_classified']))
        ].copy()

        # Create stacked bar chart
        chart = CollaborationPatternsChart(
            title="Regional Human-AI Collaboration Patterns\nCollaboration Pattern Distribution by Region",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=collab_data,
            region_col='region',
            pattern_col='cluster_name',
            value_col='value',
            xlabel='Region',
            ylabel='Percentage of Tasks (%)'
        )

        # Save in multiple formats
        saved_files = chart.save('01_regional_patterns', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_augmentation_vs_automation_chart(self):
        """Generate augmentation vs automation comparison chart."""
        print("📊 Generating augmentation vs automation comparison chart...")

        # Define pattern categories
        augmentation_patterns = ['validation', 'task iteration', 'learning']
        automation_patterns = ['directive', 'feedback loop']

        # Calculate augmentation vs automation percentages by region
        collab_data = self.data[
            (self.data['variable'] == 'collaboration_pct') &
            (~self.data['cluster_name'].isin(['none', 'not_classified']))
        ].copy()

        regional_summary = []
        for region in collab_data['region'].unique():
            region_data = collab_data[collab_data['region'] == region]

            aug_pct = region_data[region_data['cluster_name'].isin(augmentation_patterns)]['value'].sum()
            auto_pct = region_data[region_data['cluster_name'].isin(automation_patterns)]['value'].sum()

            regional_summary.extend([
                {'region': region, 'category': 'Augmentation', 'percentage': aug_pct},
                {'region': region, 'category': 'Automation', 'percentage': auto_pct}
            ])

        summary_df = pd.DataFrame(regional_summary)

        chart = AugmentationAutomationChart(
            title="Human-AI Collaboration: Augmentation vs Automation\nRegional Comparison of Collaboration Approaches",
            figsize='wide',
            output_dir=self.output_dir
        )

        chart.generate(
            data=summary_df,
            region_col='region',
            category_col='category',
            value_col='percentage',
            xlabel='Region',
            ylabel='Percentage of Collaborative Tasks (%)'
        )

        saved_files = chart.save('02_augmentation_automation', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_collaboration_intensity_ranking(self):
        """Generate collaboration intensity ranking chart."""
        print("🏆 Generating collaboration intensity ranking chart...")

        # Calculate total collaboration percentage by region (excluding none/not_classified)
        collab_data = self.data[
            (self.data['variable'] == 'collaboration_pct') &
            (~self.data['cluster_name'].isin(['none', 'not_classified']))
        ].copy()

        regional_totals = collab_data.groupby('region')['value'].sum().reset_index()
        regional_totals.columns = ['region', 'total_collaboration_pct']
        regional_totals = regional_totals.sort_values('total_collaboration_pct', ascending=False)
        regional_totals['rank'] = range(1, len(regional_totals) + 1)

        chart = RegionalRankingChart(
            title="Regional Collaboration Intensity Rankings\nTotal Human-AI Collaborative Task Percentage",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=regional_totals,
            score_col='total_collaboration_pct',
            rank_col='rank',
            region_col='region',
            xlabel='Collaboration Intensity (%)',
            ylabel='Region'
        )

        saved_files = chart.save('03_collaboration_intensity', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_collaboration_summary_table(self):
        """Generate detailed collaboration summary table."""
        print("📋 Generating collaboration summary table...")

        # Create comprehensive summary table
        collab_data = self.data[
            (self.data['variable'] == 'collaboration_pct') &
            (~self.data['cluster_name'].isin(['none', 'not_classified']))
        ].copy()

        # Pivot data for easier processing
        pivot_data = collab_data.pivot_table(
            index='region',
            columns='cluster_name',
            values='value',
            fill_value=0
        ).reset_index()

        # Calculate summary metrics
        augmentation_patterns = ['validation', 'task iteration', 'learning']
        automation_patterns = ['directive', 'feedback loop']

        summary_data = []
        for _, row in pivot_data.iterrows():
            aug_total = sum(row.get(pattern, 0) for pattern in augmentation_patterns)
            auto_total = sum(row.get(pattern, 0) for pattern in automation_patterns)

            summary = {
                'Region': row['region'],
                'Total Collaboration %': f"{aug_total + auto_total:.1f}%",
                'Augmentation %': f"{aug_total:.1f}%",
                'Automation %': f"{auto_total:.1f}%",
                'Directive %': f"{row.get('directive', 0):.1f}%",
                'Feedback Loop %': f"{row.get('feedback loop', 0):.1f}%",
                'Learning %': f"{row.get('learning', 0):.1f}%",
                'Task Iteration %': f"{row.get('task iteration', 0):.1f}%",
                'Validation %': f"{row.get('validation', 0):.1f}%"
            }
            summary_data.append(summary)

        # Sort by total collaboration percentage
        summary_df = pd.DataFrame(summary_data)
        summary_df['sort_key'] = summary_df['Total Collaboration %'].str.replace('%', '').astype(float)
        summary_df = summary_df.sort_values('sort_key', ascending=False).drop('sort_key', axis=1)
        summary_df.insert(0, 'Rank', range(1, len(summary_df) + 1))

        # Save as CSV
        csv_path = os.path.join(self.output_dir, '04_collaboration_summary.csv')
        summary_df.to_csv(csv_path, index=False)
        print(f"   ✅ Saved: {os.path.basename(csv_path)}")

        return csv_path

    def generate_insights_summary(self):
        """Generate key insights and findings summary."""
        print("💡 Generating insights summary...")

        # Calculate key insights
        collab_data = self.data[
            (self.data['variable'] == 'collaboration_pct') &
            (~self.data['cluster_name'].isin(['none', 'not_classified']))
        ].copy()

        # Find leaders in each category
        regional_totals = collab_data.groupby('region')['value'].sum()
        leader = regional_totals.idxmax()

        # Find pattern leaders
        pattern_leaders = collab_data.loc[collab_data.groupby('cluster_name')['value'].idxmax()]

        insights = {
            'Analysis': 'Regional Collaboration Analysis',
            'Methodology': 'Human-AI collaboration pattern analysis across software requests',
            'Total Regions': collab_data['region'].nunique(),
            'Collaboration Leader': leader,
            'Highest Collaboration %': f"{regional_totals[leader]:.1f}%",
            'Directive Leader': pattern_leaders[pattern_leaders['cluster_name'] == 'directive']['region'].iloc[0],
            'Learning Leader': pattern_leaders[pattern_leaders['cluster_name'] == 'learning']['region'].iloc[0],
            'Validation Leader': pattern_leaders[pattern_leaders['cluster_name'] == 'validation']['region'].iloc[0],
            'Task Iteration Leader': pattern_leaders[pattern_leaders['cluster_name'] == 'task iteration']['region'].iloc[0],
            'Average Collaboration %': f"{regional_totals.mean():.1f}%",
            'Collaboration Range': f"{regional_totals.min():.1f}% - {regional_totals.max():.1f}%"
        }

        # Save insights
        insights_path = os.path.join(self.output_dir, '05_collaboration_insights.txt')
        with open(insights_path, 'w') as f:
            f.write("REGIONAL COLLABORATION ANALYSIS - KEY INSIGHTS\\n")
            f.write("=" * 55 + "\\n\\n")
            for key, value in insights.items():
                f.write(f"{key}: {value}\\n")

        print(f"   ✅ Saved: {os.path.basename(insights_path)}")
        return insights_path

    def generate_all_charts(self):
        """Generate all charts for Regional Collaboration Analysis."""
        print("\\n🚀 GENERATING REGIONAL COLLABORATION ANALYSIS CHARTS")
        print("=" * 65)

        generated_files = []

        try:
            # Generate all chart types
            generated_files.extend(self.generate_regional_patterns_chart())
            generated_files.extend(self.generate_augmentation_vs_automation_chart())
            generated_files.extend(self.generate_collaboration_intensity_ranking())
            generated_files.append(self.generate_collaboration_summary_table())
            generated_files.append(self.generate_insights_summary())

            print(f"\\n✅ Successfully generated {len(generated_files)} files")
            print(f"📁 Output directory: {self.output_dir}")

            return generated_files

        except Exception as e:
            print(f"\\n❌ Error generating charts: {str(e)}")
            raise

class CollaborationPatternsChart(BaseChart):
    """Stacked bar chart for collaboration patterns by region."""

    def generate(self, data, region_col='region', pattern_col='cluster_name',
                value_col='value', **kwargs):
        """Generate stacked collaboration patterns chart."""

        # Pivot data for stacked bar chart
        pivot_data = data.pivot_table(
            index=region_col,
            columns=pattern_col,
            values=value_col,
            fill_value=0
        )

        # Define pattern order and colors
        pattern_order = ['directive', 'feedback loop', 'validation', 'task iteration', 'learning']
        available_patterns = [p for p in pattern_order if p in pivot_data.columns]

        # Pattern colors (automation vs augmentation)
        pattern_colors = {
            'directive': '#E74C3C',        # Red - Automation
            'feedback loop': '#C0392B',    # Dark Red - Automation
            'validation': '#27AE60',       # Green - Augmentation
            'task iteration': '#2ECC71',   # Light Green - Augmentation
            'learning': '#58D68D'          # Lighter Green - Augmentation
        }

        colors = [pattern_colors.get(pattern, '#BDC3C7') for pattern in available_patterns]

        # Create stacked bar chart
        ax = pivot_data[available_patterns].plot(
            kind='bar',
            stacked=True,
            ax=self.ax,
            color=colors,
            width=0.7,
            **BAR_SETTINGS
        )

        # Customize labels
        pattern_labels = {
            'directive': 'Directive',
            'feedback loop': 'Feedback Loop',
            'validation': 'Validation',
            'task iteration': 'Task Iteration',
            'learning': 'Learning'
        }

        ax.legend([pattern_labels.get(p, p.title()) for p in available_patterns],
                 title='Collaboration Patterns',
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

class AugmentationAutomationChart(BaseChart):
    """Grouped bar chart for augmentation vs automation comparison."""

    def generate(self, data, region_col='region', category_col='category',
                value_col='percentage', **kwargs):
        """Generate augmentation vs automation comparison chart."""

        # Pivot data for grouped bars
        pivot_data = data.pivot_table(
            index=region_col,
            columns=category_col,
            values=value_col,
            fill_value=0
        )

        # Create grouped bar chart
        colors = ['#27AE60', '#E74C3C']  # Green for Augmentation, Red for Automation
        ax = pivot_data.plot(
            kind='bar',
            ax=self.ax,
            color=colors,
            width=0.7,
            **BAR_SETTINGS
        )

        # Add value labels on bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f%%', padding=3)

        # Create legend
        create_legend(self.ax, title='Collaboration Type', loc='upper right')

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

def main():
    """Generate all Regional Collaboration Analysis charts."""
    generator = CollaborationAnalysisGenerator()
    return generator.generate_all_charts()

if __name__ == "__main__":
    main()