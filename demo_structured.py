"""
Structured Demo for Resume Builder - Module 1
Demonstrates the job description analyzer using sample text files
Provides results in both JSON and plain text formats
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from modules.job_analyzer_mvp import JobDescriptionAnalyzerMVP

# Load environment variables
load_dotenv()


def save_analysis_text(analysis, job_type, timestamp, output_dir):
    """Save analysis results to plain text file"""
    filename = f"demo_{job_type}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("JOB DESCRIPTION ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        # Role Analysis
        f.write("ROLE ANALYSIS:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Role Category: {analysis['role_analysis']['role_category']}\n")
        f.write(f"Seniority Level: {analysis['role_analysis']['seniority_level']}\n")
        f.write(f"Industry Focus: {analysis['role_analysis']['industry_focus']}\n")
        f.write(f"Experience Required: {analysis['role_analysis']['experience_years']}\n\n")
        
        # Keywords
        f.write("KEYWORDS EXTRACTED:\n")
        f.write("-" * 20 + "\n")
        
        f.write("Technical Skills:\n")
        for skill in analysis['keywords']['technical_skills']:
            f.write(f"  • {skill}\n")
        f.write("\n")
        
        f.write("Tools & Technologies:\n")
        for tool in analysis['keywords']['tools_technologies']:
            f.write(f"  • {tool}\n")
        f.write("\n")
        
        f.write("Soft Skills:\n")
        for skill in analysis['keywords']['soft_skills']:
            f.write(f"  • {skill}\n")
        f.write("\n")
        
        # Keyword Frequency
        f.write("KEYWORD FREQUENCY:\n")
        f.write("-" * 20 + "\n")
        for keyword, count in analysis['keywords']['keywords_frequency'].items():
            f.write(f"{keyword}: {count} times\n")
        f.write("\n")
        
        # Insights
        f.write("INSIGHTS & RECOMMENDATIONS:\n")
        f.write("-" * 30 + "\n")
        if 'recommendations' in analysis:
            for insight in analysis['recommendations']:
                f.write(f"• {insight}\n")
        f.write("\n")
        
        # ATS Optimization (if available)
        if 'ats_optimization' in analysis:
            f.write("ATS OPTIMIZATION SCORE:\n")
            f.write("-" * 25 + "\n")
            f.write(f"Overall Score: {analysis['ats_optimization']['overall_score']}/100\n")
            f.write(f"Keyword Match: {analysis['ats_optimization']['keyword_match']}/100\n")
            f.write(f"Format Score: {analysis['ats_optimization']['format_score']}/100\n")
            f.write(f"Content Relevance: {analysis['ats_optimization']['content_relevance']}/100\n\n")
            
            f.write("ATS Recommendations:\n")
            for rec in analysis['ats_optimization']['recommendations']:
                f.write(f"• {rec}\n")
        else:
            f.write("ATS OPTIMIZATION:\n")
            f.write("-" * 25 + "\n")
            f.write("ATS optimization analysis not available in this version.\n")
    
    return filepath


def main():
    """Main demo function"""
    print("🚀 Resume Builder - Module 1 Demo (Structured)")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        return
    
    # Initialize analyzer
    analyzer = JobDescriptionAnalyzerMVP(api_key)
    
    # Sample job descriptions from text files
    samples_dir = os.path.join('src', 'data', 'samples')
    output_dir = os.path.join('tests', 'output')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get sample files
    sample_files = [f for f in os.listdir(samples_dir) if f.endswith('.txt')]
    
    if not sample_files:
        print("❌ No sample job description files found!")
        return
    
    print(f"📁 Found {len(sample_files)} sample job descriptions")
    print("\n" + "=" * 60)
    
    # Process each sample
    for filename in sample_files:
        job_type = filename.replace('.txt', '')
        
        print(f"\n🔍 Analyzing: {job_type.replace('_', ' ').title()}")
        print("-" * 40)
        
        # Read job description
        filepath = os.path.join(samples_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        print(f"📄 Loaded from: {filename}")
        
        # Analyze job description
        print("🚀 Running analysis...")
        analysis = analyzer.analyze_job_description(job_description)
        
        # Save results in both formats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON
        json_filename = f"demo_{job_type}_{timestamp}.json"
        json_filepath = os.path.join(output_dir, json_filename)
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Save text
        text_filepath = save_analysis_text(analysis, job_type, timestamp, output_dir)
        
        # Print summary
        print("\n📊 Analysis Summary:")
        analyzer.print_analysis_summary(analysis)
        
        print(f"\n💾 Results saved to:")
        print(f"   JSON: {json_filepath}")
        print(f"   Text: {text_filepath}")
        print("-" * 40)
    
    print(f"\n✅ Demo completed! Check 'tests/output/' for all results")
    print(f"📁 Total files processed: {len(sample_files)}")
    print(f"📄 Both JSON and plain text formats are available")


if __name__ == "__main__":
    main() 