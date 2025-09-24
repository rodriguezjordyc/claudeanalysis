#!/usr/bin/env python3
"""
Base Chart Infrastructure

Shared functionality for all chart generators with consistent branding
and professional quality output.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from abc import ABC, abstractmethod

# Import our branding configuration
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from branding import *

class BaseChart(ABC):
    """
    Abstract base class for all chart types.
    Ensures consistent branding and professional output quality.
    """

    def __init__(self, title=None, figsize='medium', output_dir=None):
        """
        Initialize base chart with branding applied.

        Args:
            title (str): Chart title
            figsize (str or tuple): Figure size key or (width, height) tuple
            output_dir (str): Directory for saving charts
        """
        # Apply global branding
        apply_branding()

        self.title = title
        self.figsize = FIGURE_SIZES.get(figsize, figsize) if isinstance(figsize, str) else figsize
        self.output_dir = output_dir or 'outputs'

        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=self.figsize)

        # Track if chart has been generated
        self._generated = False

    @abstractmethod
    def generate(self, data, **kwargs):
        """
        Generate the chart with provided data.
        Must be implemented by subclasses.
        """
        pass

    def apply_styling(self, **kwargs):
        """Apply consistent styling to the chart."""
        # Chart title
        if self.title:
            style_axes(self.ax, title=self.title,
                      xlabel=kwargs.get('xlabel'),
                      ylabel=kwargs.get('ylabel'),
                      grid=kwargs.get('grid', True))

        # Tight layout for professional appearance
        plt.tight_layout(pad=SPACING['tight_layout_pad'])

    def add_value_labels(self, bars, values, format_str='{:.1f}', offset=1):
        """Add value labels on bars."""
        for bar, value in zip(bars, values):
            height = bar.get_height() if hasattr(bar, 'get_height') else bar.get_width()

            if hasattr(bar, 'get_height'):  # Vertical bars
                x = bar.get_x() + bar.get_width() / 2
                y = height + offset
                ha, va = 'center', 'bottom'
            else:  # Horizontal bars
                x = bar.get_width() + offset
                y = bar.get_y() + bar.get_height() / 2
                ha, va = 'left', 'center'

            self.ax.text(x, y, format_str.format(value),
                        ha=ha, va=va, fontsize=FONT_SIZES['annotation'],
                        fontweight='bold', family=FONT_FAMILY)

    def add_ranking_badges(self, bars, ranks, offset=5):
        """Add ranking badges to bars."""
        for bar, rank in zip(bars, ranks):
            if hasattr(bar, 'get_height'):  # Vertical bars
                x = bar.get_x() + bar.get_width() / 2
                y = offset
            else:  # Horizontal bars
                x = offset
                y = bar.get_y() + bar.get_height() / 2

            self.ax.text(x, y, f'#{int(rank)}',
                        ha='center', va='center',
                        fontsize=FONT_SIZES['small_text'],
                        fontweight='bold', family=FONT_FAMILY,
                        color='white',
                        bbox=dict(boxstyle='round,pad=0.3',
                                facecolor='black', alpha=0.8))

    def save(self, filename=None, formats=['png'], dpi=None):
        """
        Save chart in multiple formats.

        Args:
            filename (str): Base filename without extension
            formats (list): List of formats ['png', 'pdf', 'svg']
            dpi (int): Resolution for raster formats
        """
        if not self._generated:
            raise RuntimeError("Chart must be generated before saving")

        if filename is None:
            filename = self.title.lower().replace(' ', '_') if self.title else 'chart'

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        dpi = dpi or FIGURE_SETTINGS['dpi']
        saved_files = []

        for fmt in formats:
            filepath = os.path.join(self.output_dir, f"{filename}.{fmt}")
            self.fig.savefig(filepath, format=fmt, dpi=dpi,
                           bbox_inches='tight', facecolor='white',
                           edgecolor='none')
            saved_files.append(filepath)

        return saved_files

    def show(self):
        """Display the chart."""
        if not self._generated:
            raise RuntimeError("Chart must be generated before showing")
        plt.show()

    def close(self):
        """Close the chart to free memory."""
        plt.close(self.fig)

class RegionalRankingChart(BaseChart):
    """Professional horizontal bar chart for regional rankings."""

    def generate(self, data, score_col='score', rank_col='rank', region_col='region', **kwargs):
        """
        Generate horizontal ranking chart.

        Args:
            data (pd.DataFrame): Data with regions, scores, and ranks
            score_col (str): Column name for scores
            rank_col (str): Column name for ranks
            region_col (str): Column name for regions
        """
        # Sort by score (ascending for horizontal bars)
        data_sorted = data.sort_values(score_col, ascending=True)

        # Get colors for regions
        colors = get_regional_colors(data_sorted[region_col].tolist())

        # Create horizontal bar chart
        bars = self.ax.barh(data_sorted[region_col], data_sorted[score_col],
                           color=colors, **BAR_SETTINGS)

        # Add value labels
        self.add_value_labels(bars, data_sorted[score_col].values,
                            format_str='{:.1f}', offset=1)

        # Add ranking badges
        self.add_ranking_badges(bars, data_sorted[rank_col].values, offset=5)

        # Set limits and styling
        self.ax.set_xlim(0, max(data_sorted[score_col]) * 1.1)

        # Apply styling
        self.apply_styling(
            xlabel=kwargs.get('xlabel', 'Score'),
            ylabel=kwargs.get('ylabel', 'Region'),
            grid=kwargs.get('grid', True)
        )

        self._generated = True
        return self

class ComponentBreakdownChart(BaseChart):
    """Professional stacked bar chart for component analysis."""

    def generate(self, data, components, weights=None, **kwargs):
        """
        Generate stacked component breakdown chart.

        Args:
            data (pd.DataFrame): Data with component scores
            components (list): List of component column names
            weights (dict): Weights for each component
        """
        # Sort by total score (descending)
        total_col = kwargs.get('total_col', 'total_score')
        if total_col in data.columns:
            data_sorted = data.sort_values(total_col, ascending=False)
        else:
            data_sorted = data.copy()

        # Component colors
        colors = get_component_colors(components)
        width = 0.6
        x = np.arange(len(data_sorted))

        # Create stacked bars
        bottom = np.zeros(len(data_sorted))
        bars_list = []

        for i, (component, color) in enumerate(zip(components, colors)):
            values = data_sorted[component].values
            if weights and component in weights:
                values = values * weights[component]
                label = f"{component.replace('_', ' ').title()} ({weights[component]*100:.0f}%)"
            else:
                label = component.replace('_', ' ').title()

            bars = self.ax.bar(x, values, width, bottom=bottom,
                              label=label, color=color, **BAR_SETTINGS)
            bars_list.append(bars)
            bottom += values

        # Add total score labels
        if total_col in data_sorted.columns:
            totals = data_sorted[total_col].values
            self.add_value_labels(bars_list[-1], totals, offset=2)

        # Set x-axis labels
        region_col = kwargs.get('region_col', 'region')
        if total_col in data_sorted.columns:
            labels = [f"{row[region_col]}\n({row[total_col]:.1f})"
                     for _, row in data_sorted.iterrows()]
        else:
            labels = data_sorted[region_col].tolist()

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels, fontsize=FONT_SIZES['axis_tick'])

        # Create legend
        create_legend(self.ax, title='Components', loc='upper right')

        # Apply styling
        self.apply_styling(
            xlabel=kwargs.get('xlabel', 'Region (Ranked by Overall Score)'),
            ylabel=kwargs.get('ylabel', 'Score Contribution'),
            grid=kwargs.get('grid', True)
        )

        self.ax.set_ylim(0, max(bottom) * 1.1)
        self._generated = True
        return self

# Utility function for quick chart generation
def quick_ranking_chart(data, title, output_path=None, **kwargs):
    """Generate a ranking chart with minimal setup."""
    chart = RegionalRankingChart(title=title, output_dir=output_path)
    chart.generate(data, **kwargs)
    return chart