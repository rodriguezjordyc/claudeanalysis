#!/usr/bin/env python3
"""
Publication-Quality Branding Configuration

Centralized styling for all charts across analyses to ensure consistent,
professional presentation quality.
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# ==============================================================================
# TYPOGRAPHY
# ==============================================================================

# Primary font family (professional, readable)
FONT_FAMILY = 'serif'  # Can be changed to 'Arial', 'Helvetica', etc.

# Font sizes for different elements
FONT_SIZES = {
    'title': 18,
    'subtitle': 16,
    'axis_label': 14,
    'axis_tick': 12,
    'legend': 11,
    'annotation': 10,
    'small_text': 9
}

# Font weights
FONT_WEIGHTS = {
    'title': 'bold',
    'axis_label': 'bold',
    'normal': 'normal'
}

# ==============================================================================
# COLOR PALETTES
# ==============================================================================

# Primary regional colors (consistent across all analyses)
REGIONAL_COLORS = {
    'North America': '#2E86AB',      # Professional Blue
    'APAC': '#5C946E',               # Sophisticated Green
    'Europe': '#F18F01',             # Vibrant Orange
    'Latin America': '#A23B72',      # Rich Purple
    'Middle East & Africa': '#C73E1D' # Strong Red
}

# Alternative regional colors (for variation)
REGIONAL_COLORS_ALT = {
    'North America': '#1f5f7a',
    'APAC': '#4a7759',
    'Europe': '#d17a01',
    'Latin America': '#8b2f5e',
    'Middle East & Africa': '#a52e17'
}

# Component colors (for multi-dimensional charts)
COMPONENT_COLORS = {
    'collaboration': '#E74C3C',      # Red - Human element
    'efficiency': '#3498DB',         # Blue - Technical optimization
    'complexity': '#2ECC71',         # Green - Sophistication
    'volume': '#F39C12'              # Orange - Scale
}

# Quality/performance colors
PERFORMANCE_COLORS = {
    'high': '#27AE60',               # Success Green
    'medium': '#F39C12',             # Warning Orange
    'low': '#E74C3C'                 # Alert Red
}

# Professional grayscale
GRAYSCALE = {
    'black': '#2C3E50',              # Professional Black
    'dark_gray': '#7F8C8D',          # Dark Gray
    'medium_gray': '#BDC3C7',        # Medium Gray
    'light_gray': '#ECF0F1',         # Light Gray
    'white': '#FFFFFF'               # Pure White
}

# ==============================================================================
# CHART STYLING
# ==============================================================================

# Figure settings
FIGURE_SETTINGS = {
    'dpi': 300,                      # High resolution for publication
    'facecolor': 'white',
    'edgecolor': 'none'
}

# Default figure sizes (width, height in inches)
FIGURE_SIZES = {
    'small': (10, 6),               # For simple charts
    'medium': (12, 8),              # Standard size
    'large': (14, 10),              # For complex charts
    'wide': (16, 8),                # For horizontal layouts
    'tall': (10, 12)                # For vertical layouts
}

# Grid styling
GRID_STYLE = {
    'alpha': 0.3,
    'linestyle': '--',
    'linewidth': 0.5
}

# Spine (border) styling
SPINE_STYLE = {
    'linewidth': 1.2,
    'color': GRAYSCALE['dark_gray']
}

# Bar chart settings
BAR_SETTINGS = {
    'alpha': 0.85,                  # Slight transparency
    'edgecolor': 'black',
    'linewidth': 0.8
}

# ==============================================================================
# LAYOUT & SPACING
# ==============================================================================

# Padding and margins
SPACING = {
    'title_pad': 25,
    'axis_label_pad': 15,
    'legend_pad': 10,
    'tight_layout_pad': 1.5
}

# Legend positioning
LEGEND_SETTINGS = {
    'frameon': True,
    'fancybox': True,
    'shadow': True
}

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def apply_branding():
    """Apply consistent branding to matplotlib globally."""
    plt.rcParams.update({
        'font.family': FONT_FAMILY,
        'font.size': FONT_SIZES['axis_tick'],
        'axes.titlesize': FONT_SIZES['title'],
        'axes.labelsize': FONT_SIZES['axis_label'],
        'xtick.labelsize': FONT_SIZES['axis_tick'],
        'ytick.labelsize': FONT_SIZES['axis_tick'],
        'legend.fontsize': FONT_SIZES['legend'],
        'figure.titlesize': FONT_SIZES['title'],
        'figure.dpi': FIGURE_SETTINGS['dpi'],
        'figure.facecolor': FIGURE_SETTINGS['facecolor'],
        'figure.edgecolor': FIGURE_SETTINGS['edgecolor'],
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': SPINE_STYLE['linewidth'],
        'axes.edgecolor': SPINE_STYLE['color'],
        'grid.alpha': GRID_STYLE['alpha'],
        'grid.linestyle': GRID_STYLE['linestyle'],
        'grid.linewidth': GRID_STYLE['linewidth']
    })

def get_regional_colors(regions, alt=False):
    """Get consistent colors for a list of regions."""
    color_dict = REGIONAL_COLORS_ALT if alt else REGIONAL_COLORS
    return [color_dict.get(region, GRAYSCALE['medium_gray']) for region in regions]

def get_component_colors(components):
    """Get consistent colors for chart components."""
    return [COMPONENT_COLORS.get(comp, GRAYSCALE['medium_gray']) for comp in components]

def style_axes(ax, title=None, xlabel=None, ylabel=None, grid=True):
    """Apply consistent styling to chart axes."""
    if title:
        ax.set_title(title, fontsize=FONT_SIZES['title'],
                    fontweight=FONT_WEIGHTS['title'], pad=SPACING['title_pad'],
                    family=FONT_FAMILY)

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=FONT_SIZES['axis_label'],
                     fontweight=FONT_WEIGHTS['axis_label'], family=FONT_FAMILY)

    if ylabel:
        ax.set_ylabel(ylabel, fontsize=FONT_SIZES['axis_label'],
                     fontweight=FONT_WEIGHTS['axis_label'], family=FONT_FAMILY)

    if grid:
        ax.grid(axis='both', **GRID_STYLE)
        ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Style remaining spines
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_linewidth(SPINE_STYLE['linewidth'])
        ax.spines[spine].set_color(SPINE_STYLE['color'])

def create_legend(ax, title=None, **kwargs):
    """Create consistently styled legend."""
    legend_kwargs = LEGEND_SETTINGS.copy()
    if title:
        legend_kwargs['title'] = title
        legend_kwargs['title_fontsize'] = FONT_SIZES['legend']

    legend_kwargs.update(kwargs)
    legend = ax.legend(**legend_kwargs)

    # Style the legend frame
    frame = legend.get_frame()
    frame.set_alpha(0.95)
    frame.set_facecolor('white')
    frame.set_edgecolor(GRAYSCALE['medium_gray'])
    frame.set_linewidth(0.5)
    return legend

# Initialize branding on import
apply_branding()

print("📊 Publication branding loaded successfully!")
print(f"🎨 Regional colors: {len(REGIONAL_COLORS)} regions")
print(f"📐 Font family: {FONT_FAMILY}")
print(f"🔧 DPI: {FIGURE_SETTINGS['dpi']}")