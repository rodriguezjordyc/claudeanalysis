#!/usr/bin/env python3
"""
AI Software Maturity Score Chart Generator

Generates publication-quality charts for the AI Software Maturity Score analysis.
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
from chart_base import BaseChart, RegionalRankingChart, ComponentBreakdownChart

class MaturityAnalysisGenerator:
    """Generate all charts for AI Software Maturity Score analysis."""

    def __init__(self, output_dir=None):
        """Initialize with output directory."""
        self.output_dir = output_dir or os.path.join(parent_dir, 'outputs', 'maturity_analysis')
        os.makedirs(self.output_dir, exist_ok=True)

        # Load data
        self.data = pd.read_csv(get_data_path('maturity_scores'))
        print(f"📊 Loaded maturity data: {self.data.shape[0]} regions")

    def generate_regional_rankings(self):
        """Generate the main regional rankings chart."""
        print("🏆 Generating regional rankings chart...")

        chart = RegionalRankingChart(
            title="AI Software Development Maturity Score by Region\nComposite Index (0-100 Scale)",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=self.data,
            score_col='maturity_score',
            rank_col='maturity_rank',
            region_col='region',
            xlabel='Maturity Score',
            ylabel='Region'
        )

        # Save in multiple formats
        saved_files = chart.save('01_regional_rankings', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_component_breakdown(self):
        """Generate component breakdown stacked bar chart."""
        print("📊 Generating component breakdown chart...")

        # Component weights (40% Collaboration, 20% Efficiency, 40% Complexity)
        weights = {
            'collaboration_score': 0.40,
            'efficiency_score': 0.20,
            'complexity_score': 0.40
        }

        chart = ComponentBreakdownChart(
            title="AI Software Maturity Score - Component Breakdown\nWeighted Contributions to Final Score (Balanced Weighting)",
            figsize='large',
            output_dir=self.output_dir
        )

        chart.generate(
            data=self.data,
            components=['collaboration_score', 'efficiency_score', 'complexity_score'],
            weights=weights,
            total_col='maturity_score',
            region_col='region',
            xlabel='Region (Ranked by Overall Score)',
            ylabel='Score Contribution (Weighted)'
        )

        saved_files = chart.save('02_component_breakdown', formats=['png', 'pdf', 'svg'])
        print(f"   ✅ Saved: {[os.path.basename(f) for f in saved_files]}")

        chart.close()
        return saved_files

    def generate_regional_profiles_table(self):
        """Generate detailed regional profiles summary."""
        print("📋 Generating regional profiles table...")

        # Sort by maturity score
        data_ranked = self.data.sort_values('maturity_score', ascending=False)

        # Create summary table
        profiles = []
        for _, row in data_ranked.iterrows():
            profile = {
                'Rank': int(row['maturity_rank']),
                'Region': row['region'],
                'Overall Score': f"{row['maturity_score']:.1f}",
                'Collaboration': f"{row['collaboration_score']:.1f}",
                'Efficiency': f"{row['efficiency_score']:.1f}",
                'Complexity': f"{row['complexity_score']:.1f}",
                'Software Requests': f"{int(row['total_sw_requests']):,}",
                'Level 0 Tasks': f"{int(row['level0_sw_requests']):,}",
                'Level 0 %': f"{row['level0_sw_pct']:.1f}%",
                'Augmentation %': f"{row['collaboration_raw']:.1f}%"
            }
            profiles.append(profile)

        profiles_df = pd.DataFrame(profiles)

        # Save as CSV
        csv_path = os.path.join(self.output_dir, '03_regional_profiles.csv')
        profiles_df.to_csv(csv_path, index=False)
        print(f"   ✅ Saved: {os.path.basename(csv_path)}")

        return csv_path

    def generate_insights_summary(self):
        """Generate key insights and findings summary."""
        print("💡 Generating insights summary...")

        insights = {
            'Analysis': 'AI Software Maturity Score',
            'Methodology': '40% Collaboration + 20% Efficiency + 40% Complexity',
            'Total Regions': len(self.data),
            'Leader': self.data.loc[self.data['maturity_score'].idxmax(), 'region'],
            'Leader Score': f"{self.data['maturity_score'].max():.1f}",
            'Collaboration Leader': self.data.loc[self.data['collaboration_score'].idxmax(), 'region'],
            'Efficiency Leader': self.data.loc[self.data['efficiency_score'].idxmax(), 'region'],
            'Complexity Leader': self.data.loc[self.data['complexity_score'].idxmax(), 'region'],
            'Highest Volume Region': self.data.loc[self.data['total_sw_requests'].idxmax(), 'region'],
            'Highest Volume': f"{int(self.data['total_sw_requests'].max()):,}",
            'Average Maturity Score': f"{self.data['maturity_score'].mean():.1f}",
            'Score Range': f"{self.data['maturity_score'].min():.1f} - {self.data['maturity_score'].max():.1f}"
        }

        # Save insights
        insights_path = os.path.join(self.output_dir, '04_key_insights.txt')
        with open(insights_path, 'w') as f:
            f.write("AI SOFTWARE MATURITY SCORE - KEY INSIGHTS\n")
            f.write("=" * 50 + "\n\n")
            for key, value in insights.items():
                f.write(f"{key}: {value}\n")

        print(f"   ✅ Saved: {os.path.basename(insights_path)}")
        return insights_path

    def generate_all_charts(self):
        """Generate all charts for AI Software Maturity Score analysis."""
        print("\n🚀 GENERATING AI SOFTWARE MATURITY SCORE CHARTS")
        print("=" * 60)

        generated_files = []

        try:
            # Generate all chart types
            generated_files.extend(self.generate_regional_rankings())
            generated_files.extend(self.generate_component_breakdown())
            generated_files.append(self.generate_regional_profiles_table())
            generated_files.append(self.generate_insights_summary())

            print(f"\n✅ Successfully generated {len(generated_files)} files")
            print(f"📁 Output directory: {self.output_dir}")

            return generated_files

        except Exception as e:
            print(f"\n❌ Error generating charts: {str(e)}")
            raise

def main():
    """Generate all AI Software Maturity Score charts."""
    generator = MaturityAnalysisGenerator()
    return generator.generate_all_charts()

if __name__ == "__main__":
    main()