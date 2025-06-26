"""
Test Enhanced Resume Generator with RAG
Purpose: Test the enhanced resume generation with personal data
"""

import os
import sys
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from modules.enhanced_resume_generator import EnhancedResumeGenerator

# Load environment variables
load_dotenv()

def read_job_description(filename: str) -> str:
    """Read job description from file"""
    samples_dir = os.path.join('src', 'data', 'samples')
    filepath = os.path.join(samples_dir, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    """Main test function"""
    print("🚀 Testing Enhanced Resume Generator with RAG")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    # Initialize enhanced generator
    print("🔧 Initializing Enhanced Resume Generator...")
    generator = EnhancedResumeGenerator(api_key)
    
    # Check if a specific job file was provided
    if len(sys.argv) > 1:
        job_file = sys.argv[1]
        print(f"🎯 Testing with specific job: {job_file}")
        
        # Validate that the file exists
        samples_dir = os.path.join('src', 'data', 'samples')
        if not os.path.exists(os.path.join(samples_dir, job_file)):
            print(f"❌ Error: Job file '{job_file}' not found in {samples_dir}")
            return
        
        # Read job description
        job_description = read_job_description(job_file)
        job_name = job_file.replace('.txt', '')
        
        print(f"📄 Loaded job description from: {job_file}")
        print(f"📝 Job description length: {len(job_description)} characters")
        
        # Generate enhanced resume
        print("\n🚀 Generating enhanced resume...")
        enhanced_resume = generator.generate_enhanced_resume(job_description)
        
        # Save enhanced resume
        output_dir = Path(__file__).parent / "output"
        generator.save_enhanced_resume(enhanced_resume, job_name, output_dir)
        
        # Display summary
        print(f"\n📋 Enhanced Resume Summary:")
        print(f"   Job: {job_name}")
        print(f"   Summary: {len(enhanced_resume['summary'])} characters")
        print(f"   Skills: {len(enhanced_resume['skills']['frameworks'])} frameworks, {len(enhanced_resume['skills']['tools'])} tools")
        print(f"   Experience: {len(enhanced_resume['experience'])} positions")
        print(f"   Education: {len(enhanced_resume['education'])} degrees")
        
        # Show enhanced summary
        print(f"\n📄 Enhanced Professional Summary:")
        print("-" * 40)
        print(enhanced_resume['summary'])
        print("-" * 40)
        
    else:
        print("❌ Error: Please provide a job file as argument")
        print("Usage: python test_enhanced_resume_generator.py <job_file>")
        print("Example: python test_enhanced_resume_generator.py job1.txt")
        return
    
    print("\n✅ Enhanced resume generation test completed!")
    print(f"📁 Check the 'tests/output/jobs/{job_name}/enhanced/' directory for results")

if __name__ == "__main__":
    main() 