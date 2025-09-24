#!/usr/bin/env python3
"""
Data Source Configuration

Centralized paths and metadata for all chart data sources across analyses.
"""

import os

# Base data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# ==============================================================================
# DATA FILE PATHS
# ==============================================================================

DATA_SOURCES = {
    # AI Software Maturity Score Analysis
    'maturity_scores': os.path.join(DATA_DIR, 'maturity_scores.csv'),

    # Collaboration Analysis
    'collaboration': os.path.join(DATA_DIR, 'regional_collaboration_analysis.csv'),

    # Onet Analysis
    'domain_regional': os.path.join(DATA_DIR, 'domainregional.csv'),
    'onet_complexity': os.path.join(DATA_DIR, 'onetregionalraw_with_complexity.csv'),

    # Software Request Analysis
    'software_requests': os.path.join(DATA_DIR, 'softwareregionalrequests_with_sdlc.csv')
}

# ==============================================================================
# DATA SCHEMAS & METADATA
# ==============================================================================

# Column mappings for consistent processing
COLUMN_MAPPINGS = {
    'maturity_scores': {
        'region_col': 'region',
        'score_col': 'maturity_score',
        'rank_col': 'maturity_rank',
        'components': ['collaboration_score', 'efficiency_score', 'complexity_score']
    },

    'collaboration': {
        'region_col': 'region',
        'pattern_col': 'cluster_name',
        'percentage_col': 'value',
        'variable_filter': 'collaboration_pct'
    },

    'domain_regional': {
        'region_col': 'region',
        'domain_col': 'domain',
        'count_col': 'value',
        'percentage_col': 'percentage'
    },

    'software_requests': {
        'region_col': 'region',
        'level_col': 'level',
        'request_col': 'cluster_name',
        'count_col': 'value'
    }
}

# Regional standardization
STANDARD_REGIONS = [
    'North America',
    'Latin America',
    'Europe',
    'Middle East & Africa',
    'APAC'
]

# Analysis metadata
ANALYSIS_INFO = {
    'maturity_analysis': {
        'title': 'AI Software Maturity Score',
        'description': 'Regional AI software development maturity rankings',
        'data_source': 'maturity_scores',
        'chart_types': ['rankings', 'components', 'profiles']
    },

    'collaboration_analysis': {
        'title': 'Regional Collaboration Analysis',
        'description': 'Human-AI collaboration patterns by region',
        'data_source': 'collaboration',
        'chart_types': ['patterns', 'regional_comparison']
    },

    'onet_analysis': {
        'title': 'Regional Domain Analysis',
        'description': 'Occupational domain demand patterns',
        'data_source': 'domain_regional',
        'chart_types': ['domain_distribution', 'regional_profiles']
    },

    'request_analysis': {
        'title': 'Software Request Analysis',
        'description': 'Request complexity patterns by region',
        'data_source': 'software_requests',
        'chart_types': ['complexity_distribution', 'sdlc_patterns']
    }
}

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def get_data_path(source_key):
    """Get the full path for a data source."""
    if source_key not in DATA_SOURCES:
        raise ValueError(f"Unknown data source: {source_key}")

    path = DATA_SOURCES[source_key]
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")

    return path

def get_column_mapping(source_key):
    """Get column mappings for a data source."""
    return COLUMN_MAPPINGS.get(source_key, {})

def validate_data_sources():
    """Check that all data sources exist."""
    missing_files = []

    for name, path in DATA_SOURCES.items():
        if not os.path.exists(path):
            missing_files.append(f"{name}: {path}")

    if missing_files:
        print("⚠️  Missing data files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All data sources found!")
        return True

if __name__ == "__main__":
    print("📁 Data Sources Configuration")
    print("=" * 40)

    for name, path in DATA_SOURCES.items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"{exists} {name}: {os.path.basename(path)}")

    validate_data_sources()