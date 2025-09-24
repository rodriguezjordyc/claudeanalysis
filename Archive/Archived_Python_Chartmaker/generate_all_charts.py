#!/usr/bin/env python3
"""
Master Publication Chart Generator

Generates all publication-quality charts for every analysis in the project:
- AI Software Maturity Score Analysis
- Regional Collaboration Analysis
- Regional Domain Analysis (ONET)
- Software Request Analysis

This script creates a complete set of publication-ready visualizations
with consistent branding and professional quality output.
"""

import os
import sys
import time
from pathlib import Path

# Add generators directory to path
generators_dir = os.path.join(os.path.dirname(__file__), 'generators')
sys.path.append(generators_dir)

# Import all generators
try:
    from maturity_generator import MaturityAnalysisGenerator
    from collaboration_generator import CollaborationAnalysisGenerator
    from onet_generator import OnetAnalysisGenerator
    from request_generator import RequestAnalysisGenerator
except ImportError as e:
    print(f"❌ Error importing generators: {e}")
    print("Make sure all generator files are present in the generators/ directory")
    sys.exit(1)

class MasterChartGenerator:
    """Master controller for generating all publication charts."""

    def __init__(self, base_output_dir=None):
        """Initialize master generator."""
        self.base_output_dir = base_output_dir or os.path.join(os.path.dirname(__file__), 'outputs')
        self.start_time = time.time()

        # Analysis configurations
        self.analyses = {
            'maturity': {
                'name': 'AI Software Maturity Score Analysis',
                'generator_class': MaturityAnalysisGenerator,
                'description': 'Composite maturity rankings combining collaboration, efficiency, and complexity'
            },
            'collaboration': {
                'name': 'Regional Collaboration Analysis',
                'generator_class': CollaborationAnalysisGenerator,
                'description': 'Human-AI collaboration patterns and augmentation vs automation analysis'
            },
            'onet': {
                'name': 'Regional Domain Analysis (ONET)',
                'generator_class': OnetAnalysisGenerator,
                'description': 'Occupational domain distribution and software development focus analysis'
            },
            'requests': {
                'name': 'Software Request Analysis',
                'generator_class': RequestAnalysisGenerator,
                'description': 'SDLC-based request classification and volume analysis'
            }
        }

        self.generated_files = {}
        self.generation_stats = {}

    def print_header(self):
        """Print master generation header."""
        print("\\n" + "=" * 80)
        print("🚀 MASTER PUBLICATION CHART GENERATOR")
        print("=" * 80)
        print(f"📊 Generating charts for {len(self.analyses)} complete analyses")
        print(f"📁 Output directory: {self.base_output_dir}")
        print(f"🕐 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\\n")

    def generate_analysis_charts(self, analysis_key, analysis_config):
        """Generate charts for a single analysis."""
        print(f"\\n📈 STARTING: {analysis_config['name']}")
        print("-" * 60)
        print(f"Description: {analysis_config['description']}")
        print("-" * 60)

        start_time = time.time()

        try:
            # Create generator instance
            generator = analysis_config['generator_class']()

            # Generate all charts
            files = generator.generate_all_charts()

            # Record results
            end_time = time.time()
            self.generated_files[analysis_key] = files
            self.generation_stats[analysis_key] = {
                'files_generated': len(files),
                'generation_time': end_time - start_time,
                'status': 'success'
            }

            print(f"\\n✅ COMPLETED: {analysis_config['name']}")
            print(f"   📊 Generated: {len(files)} files")
            print(f"   ⏱️  Time: {end_time - start_time:.2f} seconds")

        except Exception as e:
            print(f"\\n❌ FAILED: {analysis_config['name']}")
            print(f"   Error: {str(e)}")

            self.generation_stats[analysis_key] = {
                'files_generated': 0,
                'generation_time': 0,
                'status': 'failed',
                'error': str(e)
            }

            # Continue with other analyses instead of stopping
            return False

        return True

    def generate_all_charts(self, specific_analyses=None):
        """Generate charts for all analyses."""
        self.print_header()

        # Filter analyses if specific ones requested
        analyses_to_run = self.analyses
        if specific_analyses:
            analyses_to_run = {k: v for k, v in self.analyses.items() if k in specific_analyses}
            print(f"🎯 Generating charts for specific analyses: {list(analyses_to_run.keys())}\\n")

        successful_analyses = 0
        total_files = 0

        # Generate charts for each analysis
        for analysis_key, analysis_config in analyses_to_run.items():
            success = self.generate_analysis_charts(analysis_key, analysis_config)
            if success:
                successful_analyses += 1
                total_files += self.generation_stats[analysis_key]['files_generated']

        # Print final summary
        self.print_summary(successful_analyses, len(analyses_to_run), total_files)

        return self.generated_files

    def print_summary(self, successful, total, total_files):
        """Print generation summary."""
        end_time = time.time()
        total_time = end_time - self.start_time

        print("\\n" + "=" * 80)
        print("📊 GENERATION SUMMARY")
        print("=" * 80)
        print(f"✅ Successful analyses: {successful}/{total}")
        print(f"📄 Total files generated: {total_files}")
        print(f"⏱️  Total generation time: {total_time:.2f} seconds")
        print(f"🏁 Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Detailed breakdown
        print("\\n📋 DETAILED BREAKDOWN:")
        print("-" * 40)
        for analysis_key, stats in self.generation_stats.items():
            status_icon = "✅" if stats['status'] == 'success' else "❌"
            print(f"{status_icon} {self.analyses[analysis_key]['name']}")
            print(f"   Files: {stats['files_generated']}")
            print(f"   Time: {stats['generation_time']:.2f}s")
            if stats['status'] == 'failed':
                print(f"   Error: {stats['error']}")
            print()

        # Output directories
        print("📁 OUTPUT DIRECTORIES:")
        print("-" * 40)
        for analysis_key in self.analyses.keys():
            if analysis_key in self.generated_files:
                output_dir = os.path.join(self.base_output_dir, f"{analysis_key}_analysis")
                print(f"📂 {self.analyses[analysis_key]['name']}:")
                print(f"   {output_dir}")

        print("=" * 80)

        if successful == total:
            print("🎉 ALL ANALYSES COMPLETED SUCCESSFULLY!")
            print("📊 Publication-quality charts are ready for use.")
        else:
            print(f"⚠️  {total - successful} analyses failed. Check error messages above.")

        print("=" * 80 + "\\n")

    def validate_setup(self):
        """Validate that all required files and directories are present."""
        print("🔍 Validating setup...")

        issues = []

        # Check data sources
        from config.data_sources import validate_data_sources
        if not validate_data_sources():
            issues.append("Missing data source files")

        # Check generators directory
        generators_dir = os.path.join(os.path.dirname(__file__), 'generators')
        required_generators = [
            'maturity_generator.py',
            'collaboration_generator.py',
            'onet_generator.py',
            'request_generator.py'
        ]

        for generator in required_generators:
            if not os.path.exists(os.path.join(generators_dir, generator)):
                issues.append(f"Missing generator: {generator}")

        if issues:
            print("❌ Setup validation failed:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Setup validation passed!")
            return True

def main():
    """Main function to generate all publication charts."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate publication-quality charts for all analyses',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_all_charts.py                    # Generate all charts
  python generate_all_charts.py --validate         # Validate setup only
  python generate_all_charts.py --analyses maturity collaboration  # Specific analyses
  python generate_all_charts.py --output /path/to/output  # Custom output directory
        '''
    )

    parser.add_argument('--output', '-o', type=str,
                       help='Output directory for generated charts')
    parser.add_argument('--analyses', '-a', nargs='+',
                       choices=['maturity', 'collaboration', 'onet', 'requests'],
                       help='Specific analyses to generate (default: all)')
    parser.add_argument('--validate', action='store_true',
                       help='Validate setup and exit (no chart generation)')

    args = parser.parse_args()

    # Create master generator
    generator = MasterChartGenerator(base_output_dir=args.output)

    # Validate setup
    if not generator.validate_setup():
        print("\\n❌ Setup validation failed. Please fix the issues above.")
        sys.exit(1)

    if args.validate:
        print("\\n✅ Setup validation complete. Ready to generate charts.")
        return

    # Generate charts
    try:
        generated_files = generator.generate_all_charts(specific_analyses=args.analyses)

        if generated_files:
            print(f"\\n🎯 All generated files are available in: {generator.base_output_dir}")
            return generated_files
        else:
            print("\\n❌ No files were generated.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\\n\\n⚠️  Chart generation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\\n\\n❌ Unexpected error during chart generation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()