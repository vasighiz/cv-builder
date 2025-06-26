"""
Module 2 Test Runner: Resume Keyword Matcher with Personal CV
Purpose: Test Module 2 with user's personal CV data against job descriptions
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

from modules.keyword_matcher import ResumeKeywordMatcher
from modules.job_analyzer_mvp import JobDescriptionAnalyzerMVP

# Load environment variables
load_dotenv()

def read_docx_file(file_path: str) -> str:
    """
    Read content from a .docx file
    
    Args:
        file_path (str): Path to the .docx file
        
    Returns:
        str: Extracted text content
    """
    try:
        from docx import Document
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text.strip())
        return '\n'.join(text)
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return ""

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

def save_summary_report(results: Dict[str, Any], job_name: str, timestamp: str) -> None:
    """
    Save summary report to job-specific output directory
    
    Args:
        results (Dict): Test results
        job_name (str): Name of the job
        timestamp (str): Timestamp for file naming
    """
    # Create job-specific output directory
    job_output_dir = Path(__file__).parent / "output" / "jobs" / job_name
    job_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON summary
    summary_file = job_output_dir / f"module2_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save text summary
    summary_text_file = job_output_dir / f"module2_summary_{timestamp}.txt"
    with open(summary_text_file, 'w', encoding='utf-8') as f:
        f.write("MODULE 2 SUMMARY REPORT\n")
        f.write("=" * 30 + "\n\n")
        f.write(f"Job: {job_name}\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        # CV Summary
        cv_data = results.get("cv_data", {})
        f.write("CV SUMMARY:\n")
        f.write("-" * 15 + "\n")
        f.write(f"Technical Skills: {len(cv_data.get('technical_skills', []))}\n")
        f.write(f"Soft Skills: {len(cv_data.get('soft_skills', []))}\n")
        f.write(f"Work Experience: {len(cv_data.get('work_experience', []))}\n")
        f.write(f"Projects: {len(cv_data.get('projects', []))}\n\n")
        
        # Gap Analysis Summary
        gap_analysis = results.get("gap_analysis", {})
        f.write("GAP ANALYSIS SUMMARY:\n")
        f.write("-" * 25 + "\n")
        f.write(f"Coverage: {gap_analysis.get('coverage_percentage', 0):.1f}%\n")
        f.write(f"Covered Keywords: {len(gap_analysis.get('covered_keywords', []))}\n")
        f.write(f"Missing Keywords: {len(gap_analysis.get('missing_keywords', []))}\n")
        f.write(f"Recommendations: {len(gap_analysis.get('recommendations', []))}\n\n")
        
        # Top missing keywords
        missing_keywords = gap_analysis.get('missing_keywords', [])
        if missing_keywords:
            f.write("TOP MISSING KEYWORDS:\n")
            f.write("-" * 25 + "\n")
            for i, kw in enumerate(missing_keywords[:5], 1):
                f.write(f"{i}. {kw.get('keyword', '')} ({kw.get('category', '')}) - Score: {kw.get('relevance_score', 0):.2f}\n")
    
    print(f"📋 Summary saved to:")
    print(f"   JSON: {summary_file}")
    print(f"   Text: {summary_text_file}")

def save_results(results: Dict[str, Any], job_name: str, timestamp: str) -> None:
    """
    Save test results to job-specific output directory
    
    Args:
        results (Dict): Test results to save
        job_name (str): Name of the job
        timestamp (str): Timestamp for file naming
    """
    # Create job-specific output directory
    job_output_dir = Path(__file__).parent / "output" / "jobs" / job_name
    job_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create module-specific subdirectory
    module_dir = job_output_dir / "module2"
    module_dir.mkdir(exist_ok=True)
    
    # Save JSON results
    json_file = module_dir / f"keyword_matching_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save text results
    txt_file = module_dir / f"keyword_matching_{timestamp}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("MODULE 2 TEST RESULTS: RESUME KEYWORD MATCHER\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Job: {job_name}\n")
        f.write(f"Test Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # CV Summary
        f.write("PERSONAL CV SUMMARY:\n")
        f.write("-" * 30 + "\n")
        cv_data = results.get("cv_data", {})
        f.write(f"Technical Skills: {len(cv_data.get('technical_skills', []))} skills\n")
        f.write(f"Soft Skills: {len(cv_data.get('soft_skills', []))} skills\n")
        f.write(f"Work Experience: {len(cv_data.get('work_experience', []))} positions\n")
        f.write(f"Projects: {len(cv_data.get('projects', []))} projects\n")
        f.write(f"Education: {len(cv_data.get('education', []))} entries\n")
        f.write(f"Certifications: {len(cv_data.get('certifications', []))} certifications\n\n")
        
        # Gap Analysis
        gap_analysis = results.get("gap_analysis", {})
        f.write("GAP ANALYSIS:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Coverage Percentage: {gap_analysis.get('coverage_percentage', 0):.1f}%\n")
        f.write(f"Covered Keywords: {len(gap_analysis.get('covered_keywords', []))}\n")
        f.write(f"Missing Keywords: {len(gap_analysis.get('missing_keywords', []))}\n\n")
        
        # Covered Keywords
        f.write("COVERED KEYWORDS:\n")
        f.write("-" * 20 + "\n")
        for kw in gap_analysis.get("covered_keywords", [])[:10]:
            f.write(f"✓ {kw.get('keyword', '')} ({kw.get('category', '')}) - Score: {kw.get('relevance_score', 0):.2f}\n")
        f.write("\n")
        
        # Missing Keywords
        f.write("MISSING KEYWORDS (Top Priority):\n")
        f.write("-" * 35 + "\n")
        for kw in gap_analysis.get("missing_keywords", [])[:10]:
            f.write(f"✗ {kw.get('keyword', '')} ({kw.get('category', '')}) - Score: {kw.get('relevance_score', 0):.2f}\n")
        f.write("\n")
        
        # Recommendations
        f.write("RECOMMENDATIONS:\n")
        f.write("-" * 20 + "\n")
        for rec in gap_analysis.get("recommendations", []):
            f.write(f"• {rec}\n")
        f.write("\n")
        
        # Enhancement Suggestions
        suggestions = results.get("enhancement_suggestions", {})
        f.write("ENHANCEMENT SUGGESTIONS:\n")
        f.write("-" * 30 + "\n")
        for section, section_suggestions in suggestions.items():
            if section_suggestions:
                f.write(f"\n{section.upper()}:\n")
                for suggestion in section_suggestions:
                    f.write(f"  - {suggestion}\n")
    
    print(f"💾 Results saved to:")
    print(f"   JSON: {json_file}")
    print(f"   Text: {txt_file}")

def parse_resume_with_debug(matcher: ResumeKeywordMatcher, cv_text: str) -> Dict[str, Any]:
    """
    Parse resume with robust error handling and debugging
    
    Args:
        matcher: ResumeKeywordMatcher instance
        cv_text: CV text content
        
    Returns:
        Dict: Parsed resume data
    """
    print("🔍 Parsing CV content with debug mode...")
    
    try:
        # Get the raw LLM response for debugging
        prompt = f"""
        Parse the following resume and extract structured information:
        
        Resume:
        {cv_text}
        
        Extract and categorize the following:
        
        1. Technical Skills (programming languages, frameworks, tools, etc.)
        2. Soft Skills (communication, leadership, problem-solving, etc.)
        3. Work Experience (companies, titles, dates, key achievements)
        4. Projects (project names, technologies used, outcomes)
        5. Education (degrees, institutions, relevant coursework)
        6. Certifications (if any)
        
        Also extract any keywords that might be relevant for job applications.
        
        Return as JSON:
        {{
            "technical_skills": ["skill1", "skill2", ...],
            "soft_skills": ["skill1", "skill2", ...],
            "work_experience": [
                {{
                    "company": "string",
                    "title": "string", 
                    "dates": "string",
                    "achievements": ["achievement1", "achievement2", ...]
                }}
            ],
            "projects": [
                {{
                    "name": "string",
                    "technologies": ["tech1", "tech2", ...],
                    "description": "string",
                    "outcomes": ["outcome1", "outcome2", ...]
                }}
            ],
            "education": [
                {{
                    "degree": "string",
                    "institution": "string",
                    "dates": "string",
                    "relevant_coursework": ["course1", "course2", ...]
                }}
            ],
            "certifications": ["cert1", "cert2", ...],
            "extracted_keywords": ["keyword1", "keyword2", ...]
        }}
        """
        
        response = matcher.client.chat.completions.create(
            model=matcher.model,
            messages=[
                {"role": "system", "content": "You are an expert resume parser specializing in tech industry resumes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=4000  # Increased token limit for longer CVs
        )
        
        content = response.choices[0].message.content
        print(f"📄 Raw LLM Response Length: {len(content)} characters")
        print("📄 Raw LLM Response Preview (first 500 chars):")
        print("-" * 50)
        print(content[:500])
        print("-" * 50)
        
        # Try to parse the JSON
        try:
            parsed_data = json.loads(content)
            print("✅ JSON parsing successful!")
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("🔧 Attempting to fix JSON...")
            
            # Try to clean up common JSON issues
            cleaned_content = content.strip()
            
            # Remove markdown code blocks if present
            if cleaned_content.startswith("```json"):
                cleaned_content = cleaned_content[7:]
            elif cleaned_content.startswith("```"):
                cleaned_content = cleaned_content[3:]
            
            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content[:-3]
            
            # Try parsing again
            try:
                parsed_data = json.loads(cleaned_content)
                print("✅ JSON parsing successful after cleanup!")
                return parsed_data
            except json.JSONDecodeError as e2:
                print(f"❌ JSON parsing still failed after cleanup: {e2}")
                
                # Try to extract partial data from the response
                print("🔧 Attempting to extract partial data...")
                partial_data = extract_partial_data_from_response(cleaned_content)
                if partial_data:
                    print("✅ Partial data extraction successful!")
                    return partial_data
                
                print("📄 Full raw response for manual inspection:")
                print(content)
                
                # Return empty structure as fallback
                return {
                    "technical_skills": [],
                    "soft_skills": [],
                    "work_experience": [],
                    "projects": [],
                    "education": [],
                    "certifications": [],
                    "extracted_keywords": []
                }
        
    except Exception as e:
        print(f"❌ Error in resume parsing: {e}")
        return {
            "technical_skills": [],
            "soft_skills": [],
            "work_experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "extracted_keywords": []
        }

def extract_partial_data_from_response(content: str) -> Dict[str, Any]:
    """
    Extract partial data from malformed JSON response
    
    Args:
        content: Raw LLM response content
        
    Returns:
        Dict: Partially extracted data
    """
    try:
        # Try to find and extract individual sections
        data = {
            "technical_skills": [],
            "soft_skills": [],
            "work_experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "extracted_keywords": []
        }
        
        # Extract technical skills
        if '"technical_skills"' in content:
            start = content.find('"technical_skills"')
            end = content.find(']', start)
            if end > start:
                skills_section = content[start:end+1]
                try:
                    # Try to parse just this section
                    skills_data = json.loads("{" + skills_section + "}")
                    data["technical_skills"] = skills_data.get("technical_skills", [])
                except:
                    # Extract skills manually
                    skills_text = skills_section[skills_section.find('[')+1:skills_section.rfind(']')]
                    skills = [s.strip().strip('"') for s in skills_text.split(',') if s.strip()]
                    data["technical_skills"] = [s for s in skills if s and not s.startswith('"')]
        
        # Extract soft skills
        if '"soft_skills"' in content:
            start = content.find('"soft_skills"')
            end = content.find(']', start)
            if end > start:
                skills_section = content[start:end+1]
                try:
                    skills_data = json.loads("{" + skills_section + "}")
                    data["soft_skills"] = skills_data.get("soft_skills", [])
                except:
                    skills_text = skills_section[skills_section.find('[')+1:skills_section.rfind(']')]
                    skills = [s.strip().strip('"') for s in skills_text.split(',') if s.strip()]
                    data["soft_skills"] = [s for s in skills if s and not s.startswith('"')]
        
        # Extract work experience (simplified)
        if '"work_experience"' in content:
            start = content.find('"work_experience"')
            end = content.find(']', start)
            if end > start:
                # Try to extract at least the company names
                exp_section = content[start:end+1]
                companies = []
                # Look for company names in quotes
                import re
                company_matches = re.findall(r'"company":\s*"([^"]+)"', exp_section)
                for company in company_matches:
                    companies.append({
                        "company": company,
                        "title": "Unknown",
                        "dates": "Unknown",
                        "achievements": []
                    })
                data["work_experience"] = companies
        
        # Extract projects (simplified)
        if '"projects"' in content:
            start = content.find('"projects"')
            end = content.find(']', start)
            if end > start:
                proj_section = content[start:end+1]
                projects = []
                # Look for project names
                import re
                name_matches = re.findall(r'"name":\s*"([^"]+)"', proj_section)
                for name in name_matches:
                    projects.append({
                        "name": name,
                        "technologies": [],
                        "description": "",
                        "outcomes": []
                    })
                data["projects"] = projects
        
        return data
        
    except Exception as e:
        print(f"❌ Partial data extraction failed: {e}")
        return {
            "technical_skills": [],
            "soft_skills": [],
            "work_experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "extracted_keywords": []
        }

def main():
    """
    Main test runner for Module 2
    """
    print("🚀 Module 2 Test Runner: Resume Keyword Matcher with Personal CV")
    print("=" * 70)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    # Check for CV file (use cv.docx instead of ai_cv.docx)
    cv_path = Path("cv.docx")
    if not cv_path.exists():
        print("❌ Error: cv.docx not found in workspace root")
        return
    
    print(f"📄 Found CV file: {cv_path}")
    
    # Read CV content
    print("📖 Reading CV content...")
    cv_text = read_docx_file(str(cv_path))
    if not cv_text:
        print("❌ Error: Could not read CV content")
        return
    
    print(f"✅ CV content loaded ({len(cv_text)} characters)")
    
    # Initialize modules
    print("🔧 Initializing modules...")
    matcher = ResumeKeywordMatcher(api_key)
    analyzer = JobDescriptionAnalyzerMVP(api_key)
    
    # Parse CV with debug mode
    cv_data = parse_resume_with_debug(matcher, cv_text)
    print("✅ CV parsing complete!")
    
    # Print CV summary
    print(f"\n📊 CV Summary:")
    print(f"   Technical Skills: {len(cv_data.get('technical_skills', []))}")
    print(f"   Soft Skills: {len(cv_data.get('soft_skills', []))}")
    print(f"   Work Experience: {len(cv_data.get('work_experience', []))}")
    print(f"   Projects: {len(cv_data.get('projects', []))}")
    print(f"   Education: {len(cv_data.get('education', []))}")
    print(f"   Certifications: {len(cv_data.get('certifications', []))}")
    
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
    
    if not job_files:
        print("❌ No job analysis files found. Please run Module 1 tests first.")
        return
    
    print(f"📁 Found {len(job_files)} job analysis files")
    
    # Process each job
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for job_file, job_name in job_files:
        print(f"\n🔍 Testing Module 2: {job_name}...")
        print("-" * 50)
        
        # Load job analysis
        job_analysis = load_job_analysis(job_name)
        if not job_analysis:
            print(f"❌ Could not load analysis for {job_name}")
            continue
        
        # Extract keywords from job analysis
        keywords_data = job_analysis.get("keywords", {})
        job_keywords = {
            "technical_skills": keywords_data.get("technical_skills", []),
            "soft_skills": keywords_data.get("soft_skills", []),
            "tools_technologies": keywords_data.get("tools_technologies", []),
            "keywords_frequency": keywords_data.get("keywords_frequency", {})
        }
        
        print(f"📊 Job keywords loaded: {len(job_keywords['technical_skills'])} technical, {len(job_keywords['soft_skills'])} soft skills")
        
        # Perform keyword matching
        print("🔍 Performing keyword matching...")
        gap_analysis = matcher.match_keywords(job_keywords, cv_data)
        
        # Generate enhancement suggestions
        print("💡 Generating enhancement suggestions...")
        enhancement_suggestions = matcher.generate_enhanced_resume_suggestions(gap_analysis, cv_data)
        
        # Prepare results
        results = {
            "job_name": job_name,
            "timestamp": timestamp,
            "cv_data": cv_data,
            "job_keywords": job_keywords,
            "gap_analysis": {
                "coverage_percentage": gap_analysis.coverage_percentage,
                "covered_keywords": [
                    {
                        "keyword": kw.keyword,
                        "category": kw.category,
                        "frequency_in_jd": kw.frequency_in_jd,
                        "frequency_in_resume": kw.frequency_in_resume,
                        "relevance_score": kw.relevance_score
                    }
                    for kw in gap_analysis.covered_keywords
                ],
                "missing_keywords": [
                    {
                        "keyword": kw.keyword,
                        "category": kw.category,
                        "frequency_in_jd": kw.frequency_in_jd,
                        "frequency_in_resume": kw.frequency_in_resume,
                        "relevance_score": kw.relevance_score
                    }
                    for kw in gap_analysis.missing_keywords
                ],
                "recommendations": gap_analysis.recommendations,
                "priority_keywords": gap_analysis.priority_keywords
            },
            "enhancement_suggestions": enhancement_suggestions
        }
        
        # Save results
        save_results(results, job_name, timestamp)
        
        # Print summary
        print(f"\n📊 Results Summary for {job_name}:")
        print(f"   Coverage: {gap_analysis.coverage_percentage:.1f}%")
        print(f"   Covered: {len(gap_analysis.covered_keywords)} keywords")
        print(f"   Missing: {len(gap_analysis.missing_keywords)} keywords")
        print(f"   Recommendations: {len(gap_analysis.recommendations)} suggestions")
    
    print(f"\n✅ Module 2 testing complete! Processed {len(job_files)} jobs.")

if __name__ == "__main__":
    main() 