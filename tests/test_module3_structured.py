"""
Module 3 Test Runner: Resume Sections Generator
Purpose: Test Module 3 with job analysis results from Module 1
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

from modules.resume_sections_generator_mvp import ResumeSectionsGeneratorMVP

# Load environment variables
load_dotenv()

def load_job_analysis(job_name: str) -> Dict[str, Any]:
    """
    Load job analysis results from Module 1
    
    Args:
        job_name (str): Name of the job file (e.g., 'job1')
        
    Returns:
        Dict: Job analysis results
    """
    # Look in new job-specific directory structure first
    output_dir = Path(__file__).parent / "output" / "jobs" / job_name / "module1"
    
    # Find the most recent analysis file for this job
    pattern = f"analysis_*.json"
    files = list(output_dir.glob(pattern))
    
    if not files:
        # Fallback to old location
        output_dir = Path(__file__).parent / "output" / "module1"
        pattern = f"analysis_{job_name}_*.json"
        files = list(output_dir.glob(pattern))
    
    if not files:
        # Fallback to old location without module1 subdirectory
        output_dir = Path(__file__).parent / "output"
        files = list(output_dir.glob(pattern))
    
    if not files:
        print(f"❌ No analysis files found for {job_name}")
        return {}
    
    # Get the most recent file
    latest_file = max(files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading job analysis: {e}")
        return {}

def load_user_data_from_module2() -> Dict[str, Any]:
    """
    Load user data from Module 2 results for personalization
    
    Returns:
        Dict: User data including experience and projects
    """
    # Look for the most recent Module 2 results in new job-specific structure
    output_dir = Path(__file__).parent / "output" / "jobs"
    
    if not output_dir.exists():
        return {}
    
    # Find all job directories
    job_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
    if not job_dirs:
        return {}
    
    # Look for Module 2 results in the most recent job
    latest_job_dir = max(job_dirs, key=lambda x: x.stat().st_mtime)
    module2_dir = latest_job_dir / "module2"
    
    if not module2_dir.exists():
        return {}
    
    # Find the most recent Module 2 JSON file
    json_files = list(module2_dir.glob("keyword_matching_*.json"))
    if not json_files:
        return {}
    
    # Get the most recent file
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            module2_data = json.load(f)
        
        # Extract user data
        cv_data = module2_data.get("cv_data", {})
        return {
            "work_experience": cv_data.get("work_experience", []),
            "projects": cv_data.get("projects", []),
            "technical_skills": cv_data.get("technical_skills", []),
            "soft_skills": cv_data.get("soft_skills", [])
        }
    except Exception as e:
        print(f"Error loading user data from Module 2: {e}")
        return {}

def save_summary_report(sections, job_name: str, timestamp: str) -> None:
    """
    Save summary report to job-specific output directory
    
    Args:
        sections: GeneratedSections dataclass object
        job_name (str): Name of the job
        timestamp (str): Timestamp for file naming
    """
    # Create job-specific output directory
    job_output_dir = Path(__file__).parent / "output" / "jobs" / job_name
    job_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON summary
    summary_file = job_output_dir / f"module3_summary_{timestamp}.json"
    summary_data = {
        "job_name": job_name,
        "timestamp": timestamp,
        "sections_generated": {
            "skills_count": len(sections.skills_section),
            "experience_bullets_count": len(sections.experience_bullets),
            "projects_count": len(sections.project_descriptions)
        },
        "section_summaries": {
            "skills": sections.skills_summary,
            "experience": sections.experience_summary,
            "projects": sections.projects_summary
        }
    }
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    # Save text summary
    summary_text_file = job_output_dir / f"module3_summary_{timestamp}.txt"
    with open(summary_text_file, 'w', encoding='utf-8') as f:
        f.write("MODULE 3 SUMMARY REPORT\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Job: {job_name}\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        f.write("GENERATED SECTIONS SUMMARY:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Skills Generated: {len(sections.skills_section)}\n")
        f.write(f"Experience Bullets: {len(sections.experience_bullets)}\n")
        f.write(f"Projects: {len(sections.project_descriptions)}\n\n")
        
        f.write("SECTION SUMMARIES:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Skills: {sections.skills_summary}\n")
        f.write(f"Experience: {sections.experience_summary}\n")
        f.write(f"Projects: {sections.projects_summary}\n\n")
        
        # Top skills by relevance
        f.write("TOP SKILLS BY RELEVANCE:\n")
        f.write("-" * 25 + "\n")
        sorted_skills = sorted(sections.skills_section, key=lambda x: x.relevance_score, reverse=True)
        for i, skill in enumerate(sorted_skills[:10], 1):
            f.write(f"{i:2d}. {skill.skill} ({skill.category}) - {skill.proficiency_level} (Score: {skill.relevance_score:.2f})\n")
    
    print(f"📋 Summary saved to:")
    print(f"   JSON: {summary_file}")
    print(f"   Text: {summary_text_file}")

def save_results(sections, job_name: str, timestamp: str) -> None:
    """
    Save test results to job-specific output directory
    
    Args:
        sections: GeneratedSections dataclass object
        job_name (str): Name of the job
        timestamp (str): Timestamp for file naming
    """
    # Create job-specific output directory
    job_output_dir = Path(__file__).parent / "output" / "jobs" / job_name
    job_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create module-specific subdirectory
    module_dir = job_output_dir / "module3"
    module_dir.mkdir(exist_ok=True)
    
    # Convert dataclass to dictionary for JSON serialization
    sections_dict = {
        "skills": [
            {
                "name": skill.skill,
                "category": skill.category,
                "level": skill.proficiency_level,
                "relevance": skill.relevance_score
            }
            for skill in sections.skills_section
        ],
        "experience": [
            {
                "bullet": f"{bullet.action_verb} {bullet.description}",
                "result": bullet.quantified_result,
                "keywords": bullet.keywords_used,
                "impact": bullet.impact
            }
            for bullet in sections.experience_bullets
        ],
        "projects": [
            {
                "name": project.name,
                "technologies": project.technologies,
                "description": project.description,
                "outcomes": project.outcomes,
                "relevance": project.relevance_explanation
            }
            for project in sections.project_descriptions
        ],
        "section_summaries": {
            "skills": sections.skills_summary,
            "experience": sections.experience_summary,
            "projects": sections.projects_summary
        }
    }
    
    # Save JSON results
    json_file = module_dir / f"resume_sections_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(sections_dict, f, indent=2, ensure_ascii=False)
    
    # Save text results
    txt_file = module_dir / f"resume_sections_{timestamp}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("GENERATED RESUME SECTIONS\n")
        f.write("=" * 40 + "\n\n")
        
        f.write(f"Job: {job_name}\n")
        f.write(f"Generated Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Skills section
        f.write("SKILLS SECTION:\n")
        f.write("-" * 20 + "\n")
        for i, skill in enumerate(sections.skills_section[:20], 1):  # Show top 20 skills
            f.write(f"{i:2d}. {skill.skill} ({skill.category}) - {skill.proficiency_level} (Relevance: {skill.relevance_score:.2f})\n")
        f.write("\n")
        
        # Experience section
        f.write("EXPERIENCE SECTION:\n")
        f.write("-" * 25 + "\n")
        
        # Group bullets by company and title
        current_company = ""
        current_title = ""
        
        for i, exp in enumerate(sections.experience_bullets, 1):
            # Show company and title if they change
            if exp.company and exp.company != current_company:
                current_company = exp.company
                current_title = exp.title
                f.write(f"\n{exp.title} at {exp.company}\n")
                f.write("-" * (len(exp.title) + len(exp.company) + 4) + "\n")
            elif exp.title and exp.title != current_title:
                current_title = exp.title
                f.write(f"\n{exp.title} at {exp.company}\n")
                f.write("-" * (len(exp.title) + len(exp.company) + 4) + "\n")
            
            f.write(f"{i}. {exp.action_verb} {exp.description}\n")
            f.write(f"   Result: {exp.quantified_result}\n")
            f.write(f"   Keywords: {', '.join(exp.keywords_used)}\n\n")
        
        # Projects section
        f.write("PROJECTS SECTION:\n")
        f.write("-" * 25 + "\n")
        for i, project in enumerate(sections.project_descriptions, 1):
            f.write(f"{i}. {project.name}\n")
            f.write(f"   Technologies: {', '.join(project.technologies)}\n")
            f.write(f"   Description: {project.description}\n")
            f.write(f"   Outcomes: {', '.join(project.outcomes)}\n\n")
        
        # Section summaries
        f.write("SECTION SUMMARIES:\n")
        f.write("-" * 25 + "\n")
        f.write(f"Skills: {sections.skills_summary}\n")
        f.write(f"Experience: {sections.experience_summary}\n")
        f.write(f"Projects: {sections.projects_summary}\n")
    
    # Save ATS-formatted results
    ats_file = module_dir / f"ats_sections_{timestamp}.txt"
    with open(ats_file, 'w', encoding='utf-8') as f:
        f.write("ATS-FORMATTED RESUME SECTIONS\n")
        f.write("=" * 35 + "\n\n")
        
        # Skills
        f.write("SKILLS:\n")
        f.write("SKILLS\n")
        skill_categories = {}
        for skill in sections.skills_section:
            if skill.category not in skill_categories:
                skill_categories[skill.category] = []
            skill_categories[skill.category].append(skill.skill)
        
        for category, skill_list in skill_categories.items():
            f.write(f"{category}: {', '.join(skill_list)}\n")
        f.write("\n")
        
        # Experience
        f.write("WORK EXPERIENCE:\n")
        f.write("WORK EXPERIENCE\n")
        
        # Group bullets by company and title
        current_company = ""
        current_title = ""
        
        for exp in sections.experience_bullets:
            # Show company and title if they change
            if exp.company and exp.company != current_company:
                current_company = exp.company
                current_title = exp.title
                f.write(f"\n{exp.title} at {exp.company}\n")
            elif exp.title and exp.title != current_title:
                current_title = exp.title
                f.write(f"\n{exp.title} at {exp.company}\n")
            
            f.write(f"• {exp.action_verb} {exp.description}\n")
        f.write("\n")
        
        # Projects
        f.write("PROJECTS:\n")
        f.write("PROJECTS\n")
        for project in sections.project_descriptions:
            f.write(f"{project.name}\n")
            f.write(f"Technologies: {', '.join(project.technologies)}\n")
            f.write(f"{project.description}\n")
            f.write(f"Outcomes: {', '.join(project.outcomes)}\n\n")
        
        # Summary
        f.write("SUMMARY:\n")
        f.write(f"Skills: {sections.skills_summary}\n")
        f.write(f"Experience: {sections.experience_summary}\n")
        f.write(f"Projects: {sections.projects_summary}\n")
    
    print(f"💾 Results saved to:")
    print(f"   JSON: {json_file}")
    print(f"   Text: {txt_file}")
    print(f"   ATS: {ats_file}")

def main():
    """
    Main test runner for Module 3
    """
    print("🚀 Module 3 Test Runner: Resume Sections Generator")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    # Initialize generator
    print("🔧 Initializing Module 3...")
    generator = ResumeSectionsGeneratorMVP(api_key)
    
    # Load user data from Module 2 for personalization
    print("📄 Loading user data from Module 2...")
    user_data = load_user_data_from_module2()
    if user_data:
        print(f"✅ Loaded user data: {len(user_data.get('work_experience', []))} experiences, {len(user_data.get('projects', []))} projects")
    else:
        print("⚠️  No user data found, will generate generic sections")
    
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
        print(f"\n🔍 Testing Module 3: {job_name}...")
        print("-" * 50)
        
        # Load job analysis
        job_analysis = load_job_analysis(job_name)
        if not job_analysis:
            print(f"❌ Could not load analysis for {job_name}")
            continue
        
        print(f"📄 Loaded job analysis from: {job_file.name}")
        
        # Step 1: Analyze job description (Module 1)
        print("🚀 Step 1: Analyzing job description (Module 1)...")
        
        # Step 2: Generate resume sections (Module 3) with user data
        print("🚀 Step 2: Generating resume sections (Module 3)...")
        sections = generator.generate_complete_sections(job_analysis, user_data)
        
        if sections:
            print("✅ Resume sections generated!")
            
            # Save results
            save_results(sections, job_name, timestamp)
            
            # Print summary
            print(f"\n📊 Generated Sections Summary:")
            print(f"   Skills: {len(sections.skills_section)} skills")
            print(f"   Experience: {len(sections.experience_bullets)} bullets")
            print(f"   Projects: {len(sections.project_descriptions)} projects")
            
            # Print categorization info
            if user_data:
                print(f"   📋 Personalized with {len(user_data.get('work_experience', []))} experiences from CV")
                print(f"   📋 Enhanced with recommended projects based on job requirements")
        else:
            print("❌ Failed to generate resume sections")
    
    print(f"\n✅ Module 3 testing complete! Processed {len(job_files)} job.")

if __name__ == "__main__":
    main() 