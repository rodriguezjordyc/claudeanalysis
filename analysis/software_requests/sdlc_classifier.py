#!/usr/bin/env python3
"""
SDLC Classification Script
Classifies software development requests into 5 SDLC stages based on request content.
"""

import pandas as pd
import re
from typing import Dict, List

class SDLCClassifier:
    def __init__(self):
        # Define 5 SDLC stages with classification keywords and patterns
        self.sdlc_stages = {
            "1_Requirements_Planning": {
                "keywords": [
                    "requirements", "planning", "analysis", "specification", "scope",
                    "feasibility", "research", "strategy", "guidance", "tutoring",
                    "education", "learning", "consultation", "advice", "recommend",
                    "best practices", "architecture planning", "system analysis",
                    "project planning", "technical guidance", "roadmap"
                ],
                "patterns": [
                    r"provide.*guidance", r"help.*plan", r"strategy.*development",
                    r"educational", r"tutoring", r"learning", r"consultation"
                ]
            },

            "2_Design_Architecture": {
                "keywords": [
                    "design", "architecture", "database design", "ui design", "ux",
                    "wireframe", "prototype", "mockup", "schema", "structure",
                    "layout", "styling", "visual", "interface design", "component design",
                    "system design", "api design", "data modeling", "flow design"
                ],
                "patterns": [
                    r"design.*system", r"create.*design", r"ui.*design", r"visual.*design",
                    r"database.*design", r"architecture", r"styling.*layout", r"component.*design"
                ]
            },

            "3_Implementation_Coding": {
                "keywords": [
                    "develop", "code", "implement", "build", "create", "write",
                    "programming", "coding", "development", "application development",
                    "web development", "mobile development", "software development",
                    "feature implementation", "module", "function", "script", "automation"
                ],
                "patterns": [
                    r"develop.*application", r"build.*from scratch", r"create.*complete",
                    r"implement.*feature", r"write.*code", r"programming.*assistance",
                    r"software.*development", r"build.*system"
                ]
            },

            "4_Testing_QA": {
                "keywords": [
                    "debug", "fix", "error", "bug", "test", "troubleshoot", "issue",
                    "problem", "validation", "quality", "review", "optimize",
                    "performance", "security", "vulnerability", "audit"
                ],
                "patterns": [
                    r"debug.*fix", r"fix.*error", r"troubleshoot.*issue", r"fix.*bug",
                    r"solve.*problem", r"error.*handling", r"bug.*fixing",
                    r"review.*improve", r"optimize.*performance"
                ]
            },

            "5_Deployment_Maintenance": {
                "keywords": [
                    "deploy", "deployment", "docker", "container", "cloud", "infrastructure",
                    "environment", "setup", "configuration", "devops", "ci/cd",
                    "monitoring", "maintenance", "support", "operations", "server"
                ],
                "patterns": [
                    r"deploy.*application", r"setup.*environment", r"docker.*container",
                    r"cloud.*deployment", r"infrastructure.*setup", r"environment.*configuration",
                    r"ci/cd", r"devops", r"server.*setup"
                ]
            }
        }

    def classify_request(self, request_text: str) -> str:
        """
        Classify a software request into one of the 5 SDLC stages.

        Args:
            request_text: The cluster_name text to classify

        Returns:
            SDLC stage classification
        """
        if not request_text or pd.isna(request_text):
            return "3_Implementation_Coding"  # Default fallback

        request_lower = request_text.lower()
        stage_scores = {}

        # Score each SDLC stage based on keyword and pattern matches
        for stage, criteria in self.sdlc_stages.items():
            score = 0

            # Check keyword matches
            for keyword in criteria["keywords"]:
                if keyword in request_lower:
                    score += 1

            # Check pattern matches (weighted higher)
            for pattern in criteria["patterns"]:
                if re.search(pattern, request_lower):
                    score += 2

            stage_scores[stage] = score

        # Apply specific classification rules
        if any(word in request_lower for word in ["debug", "fix", "error", "bug", "troubleshoot"]):
            return "4_Testing_QA"

        if any(word in request_lower for word in ["docker", "deploy", "cloud", "infrastructure", "environment setup"]):
            return "5_Deployment_Maintenance"

        if any(word in request_lower for word in ["design", "ui", "visual", "styling", "layout", "architecture"]):
            return "2_Design_Architecture"

        if any(word in request_lower for word in ["guidance", "tutoring", "education", "strategy", "planning", "consultation"]):
            return "1_Requirements_Planning"

        # If no specific rules match, use highest scoring stage
        if max(stage_scores.values()) > 0:
            return max(stage_scores, key=stage_scores.get)

        # Default to Implementation/Coding for general development requests
        return "3_Implementation_Coding"

def main():
    """Main function to process the CSV file and add SDLC classifications."""

    # Load the data
    input_file = 'softwareregionalrequests_clean.csv'
    output_file = 'softwareregionalrequests_with_sdlc.csv'

    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)

    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # Initialize classifier
    classifier = SDLCClassifier()

    # Apply SDLC classification
    print("\nClassifying requests into SDLC stages...")
    df['sdlc_stage'] = df['cluster_name'].apply(classifier.classify_request)

    # Generate classification summary
    print("\nSDLC Stage Distribution:")
    print("=" * 50)
    stage_counts = df['sdlc_stage'].value_counts()
    for stage, count in stage_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{stage}: {count:,} requests ({percentage:.1f}%)")

    # Show examples for each stage
    print("\nSample classifications:")
    print("=" * 80)
    for stage in classifier.sdlc_stages.keys():
        stage_examples = df[df['sdlc_stage'] == stage]['cluster_name'].head(3)
        print(f"\n{stage}:")
        for i, example in enumerate(stage_examples, 1):
            print(f"  {i}. {example}")

    # Save the classified dataset
    df.to_csv(output_file, index=False)
    print(f"\nClassified dataset saved to: {output_file}")

    # Validation summary
    print(f"\nValidation Summary:")
    print(f"Total requests classified: {len(df):,}")
    print(f"Unique request types: {df['cluster_name'].nunique():,}")
    print(f"SDLC stages identified: {df['sdlc_stage'].nunique()}")

    return df

if __name__ == "__main__":
    df_classified = main()