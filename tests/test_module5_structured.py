"""
Module 5 Test Runner: Final Resume Generator
Purpose: Test Module 5 with data from all previous modules to generate professional resumes
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from modules.final_resume_generator import FinalResumeGenerator

# Load environment variables
load_dotenv()

def main():
    """
    Main test runner for Module 5
    """
    print("🚀 Module 5 Test Runner: Final Resume Generator")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    # Initialize generator
    print("🔧 Initializing Module 5...")
    generator = FinalResumeGenerator(api_key)
    
    # Find job analysis files
    output_dir = Path(__file__).parent / "output"
    job_files = []
    
    # Check if a specific job file was provided as command-line argument
    if len(sys.argv) > 1:
        job_name = sys.argv[1].replace('.txt', '')  # Remove .txt extension
        print(f"\n🎯 Processing specific job: {job_name}")
        
        # Look for the specific job analysis file in new structure first
        job_specific_dir = output_dir / "jobs" / job_name / "module1"
        if job_specific_dir.exists():
            files = list(job_specific_dir.glob("analysis_*.json"))
            if files:
                # Get the most recent file
                latest_file = max(files, key=lambda x: x.stat().st_mtime)
                job_files.append((latest_file, job_name))
        
        # Fallback to old structure if not found
        if not job_files:
            for search_dir in [output_dir, output_dir / "module1"]:
                if search_dir.exists():
                    files = list(search_dir.glob(f"analysis_{job_name}_*.json"))
                    if files:
                        # Get the most recent file
                        latest_file = max(files, key=lambda x: x.stat().st_mtime)
                        job_files.append((latest_file, job_name))
                        break
        
        if not job_files:
            print(f"❌ No analysis files found for {job_name}. Please run Module 1 test first.")
            return
    else:
        # Look in new job-specific structure first
        jobs_dir = output_dir / "jobs"
        if jobs_dir.exists():
            for job_dir in jobs_dir.iterdir():
                if job_dir.is_dir():
                    module1_dir = job_dir / "module1"
                    if module1_dir.exists():
                        files = list(module1_dir.glob("analysis_*.json"))
                        if files:
                            job_name = job_dir.name
                            latest_file = max(files, key=lambda x: x.stat().st_mtime)
                            job_files.append((latest_file, job_name))
        
        # Fallback to old structure if no jobs found
        if not job_files:
            for search_dir in [output_dir, output_dir / "module1"]:
                if search_dir.exists():
                    for file in search_dir.glob("analysis_job*.json"):
                        job_name = file.stem.split("_")[1]  # Extract job1, job2, etc.
                        if job_name not in [f[1] for f in job_files]:
                            job_files.append((file, job_name))
        
        # Limit to only 1 job for testing (original behavior)
        job_files = job_files[:1]  # Only test the first job
        print(f"📁 Testing with 1 job: {job_files[0][1]}")
    
    if not job_files:
        print("❌ No job analysis files found. Please run Module 1 tests first.")
        return
    
    # Process the job
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for job_file, job_name in job_files:
        print(f"\n🔍 Testing Module 5: {job_name}...")
        print("-" * 50)
        
        try:
            # Generate final resume
            print("🚀 Generating final professional resume...")
            resume = generator.generate_final_resume(job_name, output_dir)
            
            if resume:
                print("✅ Final resume generated!")
                
                # Save results
                generator.save_resume(resume, output_dir)
                
                # Print summary
                print(f"\n📊 Final Resume Summary:")
                print(f"   Job: {resume.job_name}")
                print(f"   Sections: {resume.total_sections}")
                print(f"   Summary: {resume.summary}")
                
                # Print section overview
                print(f"\n📋 Resume Sections:")
                for section in resume.sections:
                    print(f"   • {section.title}: {len(section.content)} lines")
                
            else:
                print("❌ Failed to generate final resume")
                
        except Exception as e:
            print(f"❌ Error processing {job_name}: {e}")
            continue
    
    print(f"\n✅ Module 5 testing complete! Processed {len(job_files)} job.")

if __name__ == "__main__":
    main() 