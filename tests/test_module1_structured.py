"""
Structured Test Runner for Module 1: Job Description Analyzer
Reads sample job descriptions from text files and saves outputs to tests/output/
Provides results in both JSON and plain text formats
"""

import os
import sys
import json
import datetime
from dotenv import load_dotenv
from typing import Dict, Any
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.job_analyzer_mvp import JobDescriptionAnalyzerMVP

# Load environment variables
load_dotenv()


class StructuredTestRunner:
    """Structured test runner for Module 1"""
    
    def __init__(self):
        self.samples_dir = os.path.join('src', 'data', 'samples')
        self.output_dir = os.path.join('tests', 'output')
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.analyzer = JobDescriptionAnalyzerMVP(self.api_key)
    
    def get_sample_files(self):
        """Get all sample job description files"""
        sample_files = []
        for file in os.listdir(self.samples_dir):
            if file.endswith('.txt'):
                sample_files.append(file)
        return sorted(sample_files)
    
    def read_job_description(self, filename):
        """Read job description from text file"""
        filepath = os.path.join(self.samples_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def save_analysis(self, analysis: Dict[str, Any], job_name: str, timestamp: str) -> None:
        """
        Save analysis results to job-specific output directory
        
        Args:
            analysis (Dict): Analysis results to save
            job_name (str): Name of the job
            timestamp (str): Timestamp for file naming
        """
        # Create job-specific output directory
        job_output_dir = Path(__file__).parent / "output" / "jobs" / job_name
        job_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create module-specific subdirectory
        module_dir = job_output_dir / "module1"
        module_dir.mkdir(exist_ok=True)
        
        # Save JSON results
        json_file = module_dir / f"analysis_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Save text results
        txt_file = module_dir / f"analysis_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("JOB DESCRIPTION ANALYSIS RESULTS\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Job: {job_name}\n")
            f.write(f"Analysis Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Keywords summary
            keywords = analysis.get("keywords", {})
            f.write("KEYWORDS SUMMARY:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Technical Skills: {len(keywords.get('technical_skills', []))}\n")
            f.write(f"Soft Skills: {len(keywords.get('soft_skills', []))}\n")
            f.write(f"Tools & Technologies: {len(keywords.get('tools_technologies', []))}\n")
            f.write(f"Responsibilities: {len(keywords.get('responsibilities', []))}\n")
            f.write(f"Requirements: {len(keywords.get('requirements', []))}\n\n")
            
            # Detailed Keywords
            f.write("DETAILED KEYWORDS:\n")
            f.write("-" * 20 + "\n")
            
            # Technical Skills
            technical_skills = keywords.get('technical_skills', [])
            if technical_skills:
                f.write("Technical Skills:\n")
                for i, skill in enumerate(technical_skills, 1):
                    f.write(f"  {i}. {skill}\n")
                f.write("\n")
            
            # Soft Skills
            soft_skills = keywords.get('soft_skills', [])
            if soft_skills:
                f.write("Soft Skills:\n")
                for i, skill in enumerate(soft_skills, 1):
                    f.write(f"  {i}. {skill}\n")
                f.write("\n")
            
            # Tools & Technologies
            tools = keywords.get('tools_technologies', [])
            if tools:
                f.write("Tools & Technologies:\n")
                for i, tool in enumerate(tools, 1):
                    f.write(f"  {i}. {tool}\n")
                f.write("\n")
            
            # Responsibilities
            responsibilities = keywords.get('responsibilities', [])
            if responsibilities:
                f.write("Key Responsibilities:\n")
                for i, resp in enumerate(responsibilities, 1):
                    f.write(f"  {i}. {resp}\n")
                f.write("\n")
            
            # Requirements
            requirements = keywords.get('requirements', [])
            if requirements:
                f.write("Key Requirements:\n")
                for i, req in enumerate(requirements, 1):
                    f.write(f"  {i}. {req}\n")
                f.write("\n")
            
            # Keywords Frequency
            keywords_frequency = keywords.get('keywords_frequency', {})
            if keywords_frequency:
                f.write("KEYWORDS FREQUENCY ANALYSIS:\n")
                f.write("-" * 30 + "\n")
                # Sort by frequency (descending)
                sorted_keywords = sorted(keywords_frequency.items(), key=lambda x: x[1], reverse=True)
                for keyword, frequency in sorted_keywords:
                    f.write(f"  • {keyword}: {frequency} occurrences\n")
                f.write("\n")
            
            # Role analysis
            role_analysis = analysis.get("role_analysis", {})
            f.write("ROLE ANALYSIS:\n")
            f.write("-" * 15 + "\n")
            f.write(f"Category: {role_analysis.get('role_category', 'Unknown')}\n")
            f.write(f"Seniority: {role_analysis.get('seniority_level', 'Unknown')}\n")
            f.write(f"Industry: {role_analysis.get('industry_focus', 'Unknown')}\n")
            f.write(f"Experience: {role_analysis.get('experience_years', 'Unknown')}\n\n")
            
            # Insights
            insights = analysis.get("insights", {})
            f.write("DETAILED INSIGHTS:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Technical Skills: {insights.get('total_technical_skills', 0)}\n")
            f.write(f"Total Soft Skills: {insights.get('total_soft_skills', 0)}\n")
            f.write(f"Total Tools: {insights.get('total_tools', 0)}\n\n")
            
            # Most frequent keywords
            most_frequent = insights.get('most_frequent_keywords', [])
            if most_frequent:
                f.write("Most Frequent Keywords:\n")
                for keyword, frequency in most_frequent:
                    f.write(f"  • {keyword}: {frequency} times\n")
                f.write("\n")
            
            # Skill categories
            skill_categories = insights.get('skill_categories', {})
            if skill_categories:
                f.write("SKILL CATEGORIES:\n")
                f.write("-" * 20 + "\n")
                for category, skills in skill_categories.items():
                    if skills:
                        f.write(f"{category.replace('_', ' ').title()}:\n")
                        for skill in skills:
                            f.write(f"  • {skill}\n")
                        f.write("\n")
            
            # Recommendations
            recommendations = analysis.get("recommendations", [])
            if recommendations:
                f.write("RECOMMENDATIONS:\n")
                f.write("-" * 15 + "\n")
                for rec in recommendations:
                    f.write(f"• {rec}\n")
                f.write("\n")
            
            # Analysis Summary
            f.write("ANALYSIS SUMMARY:\n")
            f.write("-" * 20 + "\n")
            f.write(f"• Total keywords identified: {len(keywords_frequency)}\n")
            f.write(f"• Technical focus: {role_analysis.get('industry_focus', 'Unknown')}\n")
            f.write(f"• Seniority level: {role_analysis.get('seniority_level', 'Unknown')}\n")
            f.write(f"• Key focus areas: {', '.join([kw for kw, freq in most_frequent[:3]]) if most_frequent else 'None identified'}\n")
        
        print(f"💾 Results saved to:")
        print(f"   JSON: {json_file}")
        print(f"   Text: {txt_file}")
    
    def run_single_test(self, filename):
        """Run analysis on a single job description file"""
        job_type = filename.replace('.txt', '')
        
        print(f"\n🔍 Testing {job_type.replace('_', ' ').title()}...")
        print("-" * 50)
        
        # Read job description
        job_description = self.read_job_description(filename)
        print(f"📄 Loaded job description from: {filename}")
        
        # Analyze job description
        print("🚀 Analyzing job description...")
        analysis = self.analyzer.analyze_job_description(job_description)
        
        # Save results in both formats
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.save_analysis(analysis, job_type, timestamp)
        
        return analysis
    
    def run_all_tests(self):
        """Run analysis on all sample job descriptions"""
        print("🚀 Structured Test Runner for Module 1")
        print("=" * 60)
        
        sample_files = self.get_sample_files()
        if not sample_files:
            print("❌ No sample job description files found!")
            return
        
        print(f"📁 Found {len(sample_files)} sample job descriptions:")
        for file in sample_files:
            print(f"   • {file}")
        
        results = {}
        
        for filename in sample_files:
            try:
                analysis = self.run_single_test(filename)
                results[filename] = {
                    'analysis': analysis,
                    'status': 'success'
                }
            except Exception as e:
                print(f"❌ Error testing {filename}: {e}")
                results[filename] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # Generate summary report
        self.generate_summary_report(results)
        
        return results
    
    def generate_summary_report(self, results):
        """Generate a summary report of all tests"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # If we're processing a single job, only show in terminal
        if len(results) == 1:
            print(f"\n📋 Summary Report:")
            print(f"   Total tests: {len(results)}")
            print(f"   Successful: {len([r for r in results.values() if r['status'] == 'success'])}")
            print(f"   Failed: {len([r for r in results.values() if r['status'] == 'error'])}")
            return
        
        # For multiple jobs, save in general output directory
        summary_file = os.path.join(self.output_dir, f"test_summary_{timestamp}.json")
        summary_text_file = os.path.join(self.output_dir, f"test_summary_{timestamp}.txt")
        
        summary = {
            'timestamp': timestamp,
            'total_tests': len(results),
            'successful_tests': len([r for r in results.values() if r['status'] == 'success']),
            'failed_tests': len([r for r in results.values() if r['status'] == 'error']),
            'results': results
        }
        
        # Save JSON summary
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Save text summary
        with open(summary_text_file, 'w', encoding='utf-8') as f:
            f.write("TEST SUMMARY REPORT\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Total Tests: {summary['total_tests']}\n")
            f.write(f"Successful: {summary['successful_tests']}\n")
            f.write(f"Failed: {summary['failed_tests']}\n\n")
            
            f.write("DETAILED RESULTS:\n")
            f.write("-" * 20 + "\n")
            for filename, result in results.items():
                f.write(f"\n{filename}:\n")
                if result['status'] == 'success':
                    f.write(f"  Status: ✅ Success\n")
                    f.write(f"  Analysis completed successfully\n")
                    
                    # Add role info
                    analysis = result['analysis']
                    role_info = analysis.get('role_analysis', {})
                    f.write(f"  Role: {role_info.get('role_category', 'Unknown')} ({role_info.get('seniority_level', 'Unknown')})\n")
                    f.write(f"  Industry: {role_info.get('industry_focus', 'Unknown')}\n")
                    
                    # Add keyword counts
                    keywords = analysis.get('keywords', {})
                    f.write(f"  Technical Skills: {len(keywords.get('technical_skills', []))}\n")
                    f.write(f"  Tools & Technologies: {len(keywords.get('tools_technologies', []))}\n")
                else:
                    f.write(f"  Status: ❌ Failed\n")
                    f.write(f"  Error: {result['error']}\n")
        
        print(f"\n📋 Summary Report:")
        print(f"   Total tests: {summary['total_tests']}")
        print(f"   Successful: {summary['successful_tests']}")
        print(f"   Failed: {summary['failed_tests']}")
        print(f"   Summary saved to: {summary_file}")
        print(f"   Text summary: {summary_text_file}")
    
    def run_comparison_analysis(self, single_job_mode=False, job_name=None):
        """Run comparison analysis across all job types"""
        if single_job_mode:
            print("\n🔍 Skipping comparison analysis for single job mode")
            return {}
            
        print("\n🔍 Running Comparison Analysis...")
        print("=" * 40)
        
        sample_files = self.get_sample_files()
        comparisons = {}
        
        for filename in sample_files:
            job_type = filename.replace('.txt', '')
            job_description = self.read_job_description(filename)
            analysis = self.analyzer.analyze_job_description(job_description)
            
            comparisons[job_type] = {
                'role_category': analysis['role_analysis']['role_category'],
                'seniority_level': analysis['role_analysis']['seniority_level'],
                'industry_focus': analysis['role_analysis']['industry_focus'],
                'technical_skills_count': len(analysis['keywords']['technical_skills']),
                'tools_count': len(analysis['keywords']['tools_technologies']),
                'soft_skills_count': len(analysis['keywords']['soft_skills']),
                'top_technical_skills': analysis['keywords']['technical_skills'][:5],
                'top_tools': analysis['keywords']['tools_technologies'][:5]
            }
        
        # Save comparison in both formats
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        comparison_file = os.path.join(self.output_dir, f"job_comparison_{timestamp}.json")
        comparison_text_file = os.path.join(self.output_dir, f"job_comparison_{timestamp}.txt")
        
        # Save JSON comparison
        with open(comparison_file, 'w', encoding='utf-8') as f:
            json.dump(comparisons, f, indent=2, ensure_ascii=False)
        
        # Save text comparison
        with open(comparison_text_file, 'w', encoding='utf-8') as f:
            f.write("JOB COMPARISON ANALYSIS\n")
            f.write("=" * 30 + "\n\n")
            
            for job_type, data in comparisons.items():
                f.write(f"{job_type.replace('_', ' ').title()}:\n")
                f.write(f"  Role: {data['role_category']} ({data['seniority_level']})\n")
                f.write(f"  Industry: {data['industry_focus']}\n")
                f.write(f"  Skills: {data['technical_skills_count']} technical, {data['tools_count']} tools, {data['soft_skills_count']} soft skills\n")
                f.write(f"  Top Technical Skills: {', '.join(data['top_technical_skills'])}\n")
                f.write(f"  Top Tools: {', '.join(data['top_tools'])}\n\n")
        
        # Print comparison
        print("\n📊 Job Comparison Summary:")
        for job_type, data in comparisons.items():
            print(f"\n{job_type.replace('_', ' ').title()}:")
            print(f"   Role: {data['role_category']} ({data['seniority_level']})")
            print(f"   Industry: {data['industry_focus']}")
            print(f"   Skills: {data['technical_skills_count']} technical, {data['tools_count']} tools")
            print(f"   Top Skills: {', '.join(data['top_technical_skills'])}")
        
        print(f"\n💾 Comparison saved to:")
        print(f"   JSON: {comparison_file}")
        print(f"   Text: {comparison_text_file}")
        
        return comparisons


def main():
    """Main function to run structured tests"""
    try:
        runner = StructuredTestRunner()
        
        # Check if a specific job file was provided as command-line argument
        if len(sys.argv) > 1:
            job_file = sys.argv[1]
            print(f"🚀 Running Module 1 test on specific job: {job_file}")
            print("=" * 60)
            
            # Validate that the file exists
            if not os.path.exists(os.path.join(runner.samples_dir, job_file)):
                print(f"❌ Error: Job file '{job_file}' not found in {runner.samples_dir}")
                print(f"Available files: {runner.get_sample_files()}")
                return
            
            # Run single test
            try:
                analysis = runner.run_single_test(job_file)
                results = {job_file: {'analysis': analysis, 'status': 'success'}}
                
                # Generate summary report for single job
                runner.generate_summary_report(results)
                
            except Exception as e:
                print(f"❌ Error running analysis on {job_file}: {e}")
                results = {job_file: {'status': 'error', 'error': str(e)}}
                runner.generate_summary_report(results)
            
        else:
            # Run all tests (original behavior)
            print("🚀 Running Module 1 tests on all job files")
            print("=" * 60)
            results = runner.run_all_tests()
            
            # Run comparison analysis
            runner.run_comparison_analysis()
        
        print("\n✅ All structured tests completed!")
        print(f"📁 Check the 'tests/output/' directory for results")
        print(f"📄 Both JSON and plain text formats are available")
        
    except Exception as e:
        print(f"❌ Test runner failed: {e}")


if __name__ == "__main__":
    main() 