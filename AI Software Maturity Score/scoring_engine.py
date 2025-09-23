#!/usr/bin/env python3
"""
AI Software Maturity Score - Scoring Engine

Implements the composite scoring function with three dimensions:
1. Collaboration Sophistication Score (C): Augmentation patterns (directive + feedback loop)
2. Length Efficiency Score (L): Inverted software development length indices
3. Complexity Utilization Score (X): Level 0 software request percentage

Composite Index: 0.25×C + 0.25×L + 0.50×X (complexity-focused weighting)
"""

import pandas as pd
import numpy as np

def calculate_collaboration_score(validation_pct, task_iteration_pct, learning_pct):
    """
    Calculate Collaboration Sophistication Score (0-100).

    Measures augmentation-focused collaboration patterns.
    Higher scores for regions with more validation, task iteration, and learning patterns.

    Args:
        validation_pct: Percentage of validation collaboration
        task_iteration_pct: Percentage of task iteration collaboration
        learning_pct: Percentage of learning collaboration

    Returns:
        float: Collaboration score (0-100)
    """
    # Sum augmentation patterns (validation + task iteration + learning)
    augmentation_total = validation_pct + task_iteration_pct + learning_pct

    # Note: This assumes total collaboration is roughly the same across regions
    # We're measuring the proportion of augmentation vs automation patterns
    # Score represents the percentage of augmentation-focused collaboration
    return augmentation_total

def calculate_efficiency_score(prompt_length, completion_length, cost_index):
    """
    Calculate Efficiency Score (0-100).

    Inverted scoring: shorter prompts/completions + lower cost = higher efficiency.
    Normalized against the range of regional values.

    Args:
        prompt_length: Software development prompt length index
        completion_length: Software development completion length index
        cost_index: Software development cost index

    Returns:
        float: Efficiency score (0-100)
    """
    # Combine the three length dimensions
    total_length = prompt_length + completion_length + cost_index

    return total_length  # Return raw value for now, will normalize across regions

def calculate_complexity_score(level0_sw_pct):
    """
    Calculate Complexity Utilization Score (0-100).

    Measures engagement with highest-complexity software development tasks.

    Args:
        level0_sw_pct: Percentage of Level 0 (highest complexity) software requests

    Returns:
        float: Complexity score (0-100)
    """
    return level0_sw_pct

def normalize_scores(scores, invert=False):
    """
    Normalize scores to 0-100 scale using min-max normalization.

    Args:
        scores: List or array of scores to normalize
        invert: If True, invert scores (higher becomes lower)

    Returns:
        np.array: Normalized scores (0-100)
    """
    scores = np.array(scores)
    min_score = scores.min()
    max_score = scores.max()

    if max_score == min_score:
        return np.full_like(scores, 50.0)  # If all equal, return middle score

    # Min-max normalization to 0-100
    normalized = (scores - min_score) / (max_score - min_score) * 100

    if invert:
        normalized = 100 - normalized

    return normalized

def calculate_maturity_scores(data_df, weights=None):
    """
    Calculate AI Software Maturity Scores for all regions.

    Args:
        data_df: DataFrame with regional input metrics
        weights: Dict with 'collaboration', 'efficiency', 'complexity' weights
                Default: {'collaboration': 0.25, 'efficiency': 0.25, 'complexity': 0.50}

    Returns:
        pd.DataFrame: DataFrame with component scores and final maturity scores
    """
    if weights is None:
        weights = {'collaboration': 0.40, 'efficiency': 0.20, 'complexity': 0.40}

    # Calculate raw component scores
    collaboration_raw = []
    efficiency_raw = []
    complexity_raw = []

    for _, row in data_df.iterrows():
        # Collaboration score (augmentation patterns)
        collab_score = calculate_collaboration_score(
            row['validation_pct'],
            row['task_iteration_pct'],
            row['learning_pct']
        )
        collaboration_raw.append(collab_score)

        # Efficiency score (combined length indices - will be inverted)
        eff_score = calculate_efficiency_score(
            row['sw_prompt_length'],
            row['sw_completion_length'],
            row['sw_cost_index']
        )
        efficiency_raw.append(eff_score)

        # Complexity score (Level 0 percentage)
        complex_score = calculate_complexity_score(row['level0_sw_pct'])
        complexity_raw.append(complex_score)

    # Normalize all scores to 0-100 scale
    collaboration_normalized = normalize_scores(collaboration_raw)
    efficiency_normalized = normalize_scores(efficiency_raw, invert=True)  # Invert for efficiency
    complexity_normalized = normalize_scores(complexity_raw)

    # Calculate composite maturity scores
    maturity_scores = (
        weights['collaboration'] * collaboration_normalized +
        weights['efficiency'] * efficiency_normalized +
        weights['complexity'] * complexity_normalized
    )

    # Create results DataFrame
    results = data_df.copy()
    results['collaboration_score'] = collaboration_normalized
    results['efficiency_score'] = efficiency_normalized
    results['complexity_score'] = complexity_normalized
    results['maturity_score'] = maturity_scores
    results['maturity_rank'] = results['maturity_score'].rank(ascending=False, method='min').astype(int)

    # Add raw values for interpretation
    results['collaboration_raw'] = collaboration_raw
    results['efficiency_raw'] = efficiency_raw
    results['complexity_raw'] = complexity_raw

    return results

def print_scoring_summary(results_df):
    """Print detailed scoring summary for all regions."""
    print("AI SOFTWARE MATURITY SCORE - RESULTS")
    print("=" * 80)

    # Sort by maturity score (descending)
    results_sorted = results_df.sort_values('maturity_score', ascending=False)

    print("\n🏆 REGIONAL RANKINGS:")
    print("-" * 80)
    print(f"{'Rank':<4} {'Region':<20} {'Score':<8} {'Collab':<8} {'Effic':<8} {'Complex':<8}")
    print("-" * 80)

    for _, row in results_sorted.iterrows():
        print(f"{row['maturity_rank']:^4} {row['region']:<20} " +
              f"{row['maturity_score']:6.1f}   " +
              f"{row['collaboration_score']:6.1f}   " +
              f"{row['efficiency_score']:6.1f}   " +
              f"{row['complexity_score']:6.1f}")

    print("\n📊 COMPONENT ANALYSIS:")
    print("-" * 80)

    # Find leaders in each dimension
    collab_leader = results_df.loc[results_df['collaboration_score'].idxmax(), 'region']
    efficiency_leader = results_df.loc[results_df['efficiency_score'].idxmax(), 'region']
    complexity_leader = results_df.loc[results_df['complexity_score'].idxmax(), 'region']

    print(f"🤝 Collaboration Leader: {collab_leader}")
    print(f"⚡ Efficiency Leader: {efficiency_leader}")
    print(f"🧠 Complexity Leader: {complexity_leader}")

    # Biggest surprises
    overall_leader = results_sorted.iloc[0]['region']
    print(f"🎯 Overall Leader: {overall_leader}")

    return results_sorted

if __name__ == "__main__":
    # Load regional inputs
    data = pd.read_csv("regional_inputs.csv")

    print("AI SOFTWARE MATURITY SCORE CALCULATION")
    print("=" * 60)
    print("Methodology: Collaboration (40%) + Efficiency (20%) + Complexity (40%)")
    print("=" * 60)

    # Calculate scores
    results = calculate_maturity_scores(data)

    # Print summary
    summary = print_scoring_summary(results)

    # Save results
    results.to_csv("maturity_scores.csv", index=False)
    print(f"\n✅ Results saved to: maturity_scores.csv")

    print(f"\n🎯 Next step: Create analysis notebook with visualizations!")