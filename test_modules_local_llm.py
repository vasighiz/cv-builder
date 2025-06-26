"""
Test Modules 1, 2, 3, and 5 on Job1 using Local LLM
Purpose: Run all modules on job1.txt using the local GGUF model
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import LLM interface
from modules.llm_interface import create_llm_interface

# Load environment variables
load_dotenv()

class LocalLLMTestRunner:
    """Test runner for modules using local LLM"""
    
    def __init__(self):
        self.samples_dir = Path("src/data/samples")
        self.output_dir = Path("tests/output")
        self.job_name = "job1"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize LLM interface
        print("🔄 Initializing local LLM...")
        self.llm = create_llm_interface("local")
        
        # Test LLM connection
        if not self.llm.test_connection():
            raise RuntimeError("Local LLM not available")
        
        print("✅ Local LLM initialized successfully")
    
    def read_job_description(self) -> str:
        """Read job1 description"""
        job_file = self.samples_dir / f"{self.job_name}.txt"
        with open(job_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def create_sample_cv_data(self) -> Dict[str, Any]:
        """Create sample CV data for testing"""
        return {
            "personal_info": {
                "name": "John Doe",
                "email": "john.doe@email.com",
                "phone": "+1 (555) 123-4567",
                "location": "San Francisco, CA",
                "linkedin": "linkedin.com/in/johndoe"
            },
            "education": [
                {
                    "degree": "PhD in Machine Learning",
                    "institution": "Stanford University",
                    "year": "2020",
                    "gpa": "3.9/4.0"
                },
                {
                    "degree": "MSc in Computer Science",
                    "institution": "MIT",
                    "year": "2018",
                    "gpa": "3.8/4.0"
                }
            ],
            "work_experience": [
                {
                    "title": "Senior Machine Learning Scientist",
                    "company": "TechCorp",
                    "dates": "2020-2023",
                    "achievements": [
                        "Developed deep learning models for drug discovery",
                        "Led team of 5 researchers",
                        "Published 10 papers in top conferences"
                    ]
                },
                {
                    "title": "Machine Learning Engineer",
                    "company": "AI Startup",
                    "dates": "2018-2020",
                    "achievements": [
                        "Built production ML pipelines",
                        "Improved model accuracy by 25%",
                        "Deployed models to AWS"
                    ]
                }
            ],
            "projects": [
                {
                    "name": "Drug Discovery ML Platform",
                    "description": "Developed end-to-end ML platform for drug discovery",
                    "technologies": ["PyTorch", "Python", "AWS", "Docker"],
                    "outcomes": ["Reduced drug discovery time by 40%", "Identified 5 novel drug candidates"]
                },
                {
                    "name": "Genomics Analysis Tool",
                    "description": "Built tool for analyzing large genomic datasets",
                    "technologies": ["Python", "TensorFlow", "Bioinformatics", "HPC"],
                    "outcomes": ["Processed 1TB of genomic data", "Published in Nature"]
                }
            ],
            "technical_skills": [
                "Machine Learning", "Deep Learning", "Python", "PyTorch", "TensorFlow",
                "JAX", "Bioinformatics", "Computational Biology", "AWS", "Docker",
                "Statistics", "Linear Algebra", "Optimization", "Git", "Linux"
            ],
            "certifications": [
                "AWS Certified Machine Learning - Specialty",
                "Google Cloud Professional Data Engineer"
            ]
        }
    
    def run_module1_local(self) -> Dict[str, Any]:
        """Run Module 1: Job Description Analyzer using local LLM"""
        print("\n" + "="*60)
        print("🧪 RUNNING MODULE 1: Job Description Analyzer (Local LLM)")
        print("="*60)
        
        job_description = self.read_job_description()
        
        try:
            print("🔄 Analyzing job description with local LLM...")
            
            # Extract keywords using local LLM
            keywords_prompt = f"""
            Analyze this job description and extract relevant keywords for a tech resume.
            
            Job Description:
            {job_description}
            
            Extract and categorize the following:
            1. Technical Skills (programming languages, frameworks, libraries)
            2. Soft Skills (communication, leadership, problem-solving)
            3. Tools & Technologies (specific tools, platforms, software)
            4. Key Responsibilities (main duties and tasks)
            5. Requirements (qualifications, experience, education)
            
            Also count how many times important keywords appear.
            
            Return ONLY a JSON object with this exact structure:
            {{
                "technical_skills": ["skill1", "skill2"],
                "soft_skills": ["skill1", "skill2"],
                "tools_technologies": ["tool1", "tool2"],
                "responsibilities": ["responsibility1", "responsibility2"],
                "requirements": ["requirement1", "requirement2"],
                "keywords_frequency": {{"keyword1": count1, "keyword2": count2}}
            }}
            """
            
            keywords_response = self.llm.generate_text(keywords_prompt, max_tokens=800)
            
            # Parse keywords
            try:
                # Find JSON in response
                start = keywords_response.find('{')
                end = keywords_response.rfind('}') + 1
                if start != -1 and end != 0:
                    keywords_json = keywords_response[start:end]
                    keywords_data = json.loads(keywords_json)
                else:
                    raise ValueError("No JSON found in response")
            except Exception as e:
                print(f"❌ Error parsing keywords JSON: {e}")
                keywords_data = {
                    "technical_skills": [],
                    "soft_skills": [],
                    "tools_technologies": [],
                    "responsibilities": [],
                    "requirements": [],
                    "keywords_frequency": {}
                }
            
            # Classify role using local LLM
            role_prompt = f"""
            Analyze this job description and classify the role:
            
            {job_description}
            
            Determine:
            1. Primary role category (Data Scientist, ML Engineer, Software Engineer, etc.)
            2. Seniority level (Junior, Mid-level, Senior, Lead, etc.)
            3. Industry focus (AI/ML, Web Development, Data Analytics, etc.)
            4. Required experience level (years)
            
            Return ONLY a JSON object:
            {{
                "role_category": "string",
                "seniority_level": "string", 
                "industry_focus": "string",
                "experience_years": "string"
            }}
            """
            
            role_response = self.llm.generate_text(role_prompt, max_tokens=300)
            
            # Parse role analysis
            try:
                start = role_response.find('{')
                end = role_response.rfind('}') + 1
                if start != -1 and end != 0:
                    role_json = role_response[start:end]
                    role_data = json.loads(role_json)
                else:
                    raise ValueError("No JSON found in response")
            except Exception as e:
                print(f"❌ Error parsing role JSON: {e}")
                role_data = {
                    "role_category": "Unknown",
                    "seniority_level": "Unknown",
                    "industry_focus": "Unknown",
                    "experience_years": "Unknown"
                }
            
            # Create analysis results
            analysis = {
                "keywords": keywords_data,
                "role_analysis": role_data,
                "insights": {
                    "total_technical_skills": len(keywords_data.get("technical_skills", [])),
                    "total_soft_skills": len(keywords_data.get("soft_skills", [])),
                    "total_tools": len(keywords_data.get("tools_technologies", [])),
                    "most_frequent_keywords": sorted(
                        keywords_data.get("keywords_frequency", {}).items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:10]
                },
                "recommendations": [
                    "Focus on machine learning and computational biology skills",
                    "Highlight experience with drug discovery or bioinformatics",
                    "Emphasize research and publication experience"
                ]
            }
            
            # Save results
            self.save_module_results(1, analysis)
            
            print("✅ Module 1 completed successfully")
            return analysis
            
        except Exception as e:
            print(f"❌ Module 1 failed: {e}")
            return {}
    
    def run_module2_local(self, module1_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run Module 2: Keyword Matcher using local LLM"""
        print("\n" + "="*60)
        print("🧪 RUNNING MODULE 2: Keyword Matcher (Local LLM)")
        print("="*60)
        
        cv_data = self.create_sample_cv_data()
        
        try:
            print("🔄 Matching keywords with local LLM...")
            
            # Extract keywords from CV
            cv_skills = cv_data.get("technical_skills", [])
            cv_tools = []
            for project in cv_data.get("projects", []):
                cv_tools.extend(project.get("technologies", []))
            
            # Get job keywords
            job_keywords = module1_results.get("keywords", {})
            job_technical = job_keywords.get("technical_skills", [])
            job_tools = job_keywords.get("tools_technologies", [])
            job_requirements = job_keywords.get("requirements", [])
            
            # Create matching prompt
            matching_prompt = f"""
            Analyze the match between job requirements and candidate skills.
            
            JOB REQUIREMENTS:
            Technical Skills: {job_technical}
            Tools & Technologies: {job_tools}
            Requirements: {job_requirements}
            
            CANDIDATE SKILLS:
            Technical Skills: {cv_skills}
            Tools & Technologies: {cv_tools}
            
            Determine:
            1. Which skills match between job and candidate
            2. Which skills are missing from candidate
            3. Overall match percentage
            4. Recommendations for improvement
            
            Return ONLY a JSON object:
            {{
                "matching_keywords": [{{"keyword": "skill", "job_context": "context", "cv_context": "context"}}],
                "missing_keywords": [{{"keyword": "skill", "importance": "high/medium/low", "suggestion": "how to acquire"}}],
                "match_score": 85.5,
                "recommendations": ["rec1", "rec2"]
            }}
            """
            
            matching_response = self.llm.generate_text(matching_prompt, max_tokens=600)
            
            # Parse matching results
            try:
                start = matching_response.find('{')
                end = matching_response.rfind('}') + 1
                if start != -1 and end != 0:
                    matching_json = matching_response[start:end]
                    matching_data = json.loads(matching_json)
                else:
                    raise ValueError("No JSON found in response")
            except Exception as e:
                print(f"❌ Error parsing matching JSON: {e}")
                matching_data = {
                    "matching_keywords": [],
                    "missing_keywords": [],
                    "match_score": 0.0,
                    "recommendations": []
                }
            
            # Create gap analysis
            gap_analysis = {
                "matching_keywords": matching_data.get("matching_keywords", []),
                "missing_keywords": matching_data.get("missing_keywords", []),
                "match_score": matching_data.get("match_score", 0.0),
                "recommendations": matching_data.get("recommendations", [])
            }
            
            # Create results
            results = {
                "cv_data": cv_data,
                "gap_analysis": gap_analysis,
                "keyword_matching": {
                    "job_keywords": job_keywords,
                    "cv_keywords": {
                        "technical_skills": cv_skills,
                        "tools_technologies": cv_tools
                    }
                }
            }
            
            # Save results
            self.save_module_results(2, results)
            
            print("✅ Module 2 completed successfully")
            return results
            
        except Exception as e:
            print(f"❌ Module 2 failed: {e}")
            return {}
    
    def run_module3_local(self, module1_results: Dict[str, Any], module2_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run Module 3: Resume Sections Generator using local LLM"""
        print("\n" + "="*60)
        print("🧪 RUNNING MODULE 3: Resume Sections Generator (Local LLM)")
        print("="*60)
        
        try:
            print("🔄 Generating resume sections with local LLM...")
            
            # Get data from previous modules
            job_keywords = module1_results.get("keywords", {})
            cv_data = module2_results.get("cv_data", {})
            gap_analysis = module2_results.get("gap_analysis", {})
            
            # Generate skills section
            skills_prompt = f"""
            Create a skills section for a resume based on this job and candidate data.
            
            JOB REQUIREMENTS:
            {job_keywords.get('technical_skills', [])}
            {job_keywords.get('tools_technologies', [])}
            
            CANDIDATE SKILLS:
            {cv_data.get('technical_skills', [])}
            
            MATCHING SKILLS:
            {[item.get('keyword', '') for item in gap_analysis.get('matching_keywords', [])]}
            
            Create a skills section that:
            1. Prioritizes skills that match job requirements
            2. Groups skills by category (Programming, ML/AI, Tools, etc.)
            3. Uses professional formatting
            
            Return ONLY a JSON array of skill objects:
            [{{"category": "Programming Languages", "skills": ["Python", "R"]}}, {{"category": "ML/AI", "skills": ["PyTorch", "TensorFlow"]}}]
            """
            
            skills_response = self.llm.generate_text(skills_prompt, max_tokens=400)
            
            # Parse skills
            try:
                start = skills_response.find('[')
                end = skills_response.rfind(']') + 1
                if start != -1 and end != 0:
                    skills_json = skills_response[start:end]
                    skills_data = json.loads(skills_json)
                else:
                    raise ValueError("No JSON array found in response")
            except Exception as e:
                print(f"❌ Error parsing skills JSON: {e}")
                skills_data = []
            
            # Generate experience bullets
            experience_prompt = f"""
            Create professional experience bullet points for a resume based on this work experience.
            
            WORK EXPERIENCE:
            {cv_data.get('work_experience', [])}
            
            JOB REQUIREMENTS:
            {job_keywords.get('responsibilities', [])}
            
            Create 3-4 bullet points that:
            1. Start with action verbs
            2. Include quantifiable achievements
            3. Match the job requirements
            4. Are specific and relevant
            
            Return ONLY a JSON array of experience objects:
            [{{"company": "Company", "title": "Title", "bullet": "Achievement", "result": "Impact"}}]
            """
            
            experience_response = self.llm.generate_text(experience_prompt, max_tokens=500)
            
            # Parse experience
            try:
                start = experience_response.find('[')
                end = experience_response.rfind(']') + 1
                if start != -1 and end != 0:
                    experience_json = experience_response[start:end]
                    experience_data = json.loads(experience_json)
                else:
                    raise ValueError("No JSON array found in response")
            except Exception as e:
                print(f"❌ Error parsing experience JSON: {e}")
                experience_data = []
            
            # Create results
            results = {
                "skills": skills_data,
                "experience": experience_data,
                "projects": cv_data.get("projects", []),
                "education": cv_data.get("education", [])
            }
            
            # Save results
            self.save_module_results(3, results)
            
            print("✅ Module 3 completed successfully")
            return results
            
        except Exception as e:
            print(f"❌ Module 3 failed: {e}")
            return {}
    
    def run_module5_local(self, module1_results: Dict[str, Any], module2_results: Dict[str, Any], module3_results: Dict[str, Any]) -> Dict[str, Any]:
        """Run Module 5: Final Resume Generator using local LLM"""
        print("\n" + "="*60)
        print("🧪 RUNNING MODULE 5: Final Resume Generator (Local LLM)")
        print("="*60)
        
        try:
            print("🔄 Generating final resume with local LLM...")
            
            # Get data from previous modules
            job_analysis = module1_results
            cv_data = module2_results.get("cv_data", {})
            gap_analysis = module2_results.get("gap_analysis", {})
            sections_data = module3_results
            
            # Generate professional summary
            summary_prompt = f"""
            Create a compelling professional summary for a resume based on this data.
            
            JOB INFORMATION:
            Role: {job_analysis.get('role_analysis', {}).get('role_category', 'Professional')}
            Industry: {job_analysis.get('role_analysis', {}).get('industry_focus', 'Technology')}
            Requirements: {job_analysis.get('keywords', {}).get('requirements', [])}
            
            CANDIDATE INFORMATION:
            Experience: {len(cv_data.get('work_experience', []))} positions
            Education: {[edu.get('degree', '') for edu in cv_data.get('education', [])]}
            Skills: {cv_data.get('technical_skills', [])}
            
            Create a professional summary that:
            1. Opens with role and experience level
            2. Highlights relevant skills and achievements
            3. Matches the job requirements
            4. Is 2-3 sentences long
            5. Uses professional language
            """
            
            summary_response = self.llm.generate_text(summary_prompt, max_tokens=150)
            
            # Create final resume structure
            final_resume = {
                "job_name": self.job_name,
                "timestamp": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                "sections": [
                    {
                        "title": "PROFESSIONAL SUMMARY",
                        "content": [summary_response.strip()],
                        "order": 1
                    },
                    {
                        "title": "TECHNICAL SKILLS",
                        "content": [f"{cat.get('category', '')}: {', '.join(cat.get('skills', []))}" 
                                   for cat in sections_data.get("skills", [])],
                        "order": 2
                    },
                    {
                        "title": "PROFESSIONAL EXPERIENCE",
                        "content": [f"• {exp.get('bullet', '')} {exp.get('result', '')}" 
                                   for exp in sections_data.get("experience", [])],
                        "order": 3
                    },
                    {
                        "title": "EDUCATION",
                        "content": [f"{edu.get('degree', '')} | {edu.get('institution', '')} | {edu.get('year', '')}" 
                                   for edu in cv_data.get("education", [])],
                        "order": 4
                    }
                ],
                "summary": f"Professional resume for {job_analysis.get('role_analysis', {}).get('role_category', 'target role')} position",
                "total_sections": 4
            }
            
            # Save results
            self.save_module_results(5, {"resume": final_resume})
            
            print("✅ Module 5 completed successfully")
            return {"resume": final_resume}
            
        except Exception as e:
            print(f"❌ Module 5 failed: {e}")
            return {}
    
    def save_module_results(self, module_num: int, results: Dict[str, Any]):
        """Save module results to output directory"""
        # Create job-specific output directory
        job_output_dir = self.output_dir / "jobs" / self.job_name
        job_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create module-specific subdirectory
        module_dir = job_output_dir / f"module{module_num}"
        module_dir.mkdir(exist_ok=True)
        
        # Generate timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        if module_num == 1:
            filename = f"analysis_{timestamp}.json"
        elif module_num == 2:
            filename = f"keyword_matching_{timestamp}.json"
        elif module_num == 3:
            filename = f"resume_sections_{timestamp}.json"
        elif module_num == 5:
            filename = f"final_resume_{timestamp}.json"
        
        json_file = module_dir / filename
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {json_file}")
    
    def generate_summary_report(self, all_results: Dict[str, Any]):
        """Generate a summary report of all module results"""
        print("\n" + "="*60)
        print("📊 GENERATING SUMMARY REPORT")
        print("="*60)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"local_llm_test_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("LOCAL LLM MODULE TEST REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Job: {self.job_name}\n")
            f.write(f"Test Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"LLM Provider: Local (GGUF)\n\n")
            
            # Module 1 Summary
            module1_results = all_results.get("module1", {})
            f.write("MODULE 1 - Job Analysis:\n")
            f.write("-" * 25 + "\n")
            keywords = module1_results.get("keywords", {})
            f.write(f"• Technical Skills: {len(keywords.get('technical_skills', []))}\n")
            f.write(f"• Soft Skills: {len(keywords.get('soft_skills', []))}\n")
            f.write(f"• Tools & Technologies: {len(keywords.get('tools_technologies', []))}\n")
            f.write(f"• Requirements: {len(keywords.get('requirements', []))}\n\n")
            
            # Module 2 Summary
            module2_results = all_results.get("module2", {})
            f.write("MODULE 2 - Keyword Matching:\n")
            f.write("-" * 25 + "\n")
            gap_analysis = module2_results.get("gap_analysis", {})
            f.write(f"• Matching Keywords: {len(gap_analysis.get('matching_keywords', []))}\n")
            f.write(f"• Missing Keywords: {len(gap_analysis.get('missing_keywords', []))}\n")
            f.write(f"• Match Score: {gap_analysis.get('match_score', 0):.2f}%\n\n")
            
            # Module 3 Summary
            module3_results = all_results.get("module3", {})
            f.write("MODULE 3 - Resume Sections:\n")
            f.write("-" * 25 + "\n")
            f.write(f"• Skills Generated: {len(module3_results.get('skills', []))}\n")
            f.write(f"• Experience Bullets: {len(module3_results.get('experience', []))}\n")
            f.write(f"• Projects: {len(module3_results.get('projects', []))}\n\n")
            
            # Module 5 Summary
            module5_results = all_results.get("module5", {})
            f.write("MODULE 5 - Final Resume:\n")
            f.write("-" * 25 + "\n")
            if "resume" in module5_results:
                resume = module5_results["resume"]
                f.write(f"• Total Sections: {resume.get('total_sections', 0)}\n")
                f.write(f"• Job Name: {resume.get('job_name', 'Unknown')}\n")
                f.write(f"• Timestamp: {resume.get('timestamp', 'Unknown')}\n\n")
            
            # LLM Usage Stats
            usage_stats = self.llm.get_usage_stats()
            f.write("LLM USAGE STATISTICS:\n")
            f.write("-" * 25 + "\n")
            for provider, stats in usage_stats.items():
                f.write(f"{provider.upper()}:\n")
                f.write(f"  • Calls: {stats.get('calls', 0)}\n")
                f.write(f"  • Total Tokens: {stats.get('total_tokens', 0)}\n")
                f.write(f"  • Errors: {stats.get('errors', 0)}\n\n")
        
        print(f"📄 Summary report saved to: {report_file}")
    
    def run_all_modules(self):
        """Run all modules in sequence"""
        print("🚀 STARTING LOCAL LLM MODULE TESTS")
        print("="*60)
        print(f"Job: {self.job_name}")
        print(f"LLM Provider: Local (GGUF)")
        print(f"Output Directory: {self.output_dir}")
        print("="*60)
        
        all_results = {}
        
        # Run Module 1
        module1_results = self.run_module1_local()
        all_results["module1"] = module1_results
        
        if not module1_results:
            print("❌ Module 1 failed, stopping execution")
            return
        
        # Run Module 2
        module2_results = self.run_module2_local(module1_results)
        all_results["module2"] = module2_results
        
        if not module2_results:
            print("❌ Module 2 failed, stopping execution")
            return
        
        # Run Module 3
        module3_results = self.run_module3_local(module1_results, module2_results)
        all_results["module3"] = module3_results
        
        if not module3_results:
            print("❌ Module 3 failed, stopping execution")
            return
        
        # Run Module 5
        module5_results = self.run_module5_local(module1_results, module2_results, module3_results)
        all_results["module5"] = module5_results
        
        # Generate summary report
        self.generate_summary_report(all_results)
        
        print("\n" + "="*60)
        print("🎉 ALL MODULES COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        # Print final statistics
        usage_stats = self.llm.get_usage_stats()
        print(f"📊 LLM Usage:")
        for provider, stats in usage_stats.items():
            print(f"   {provider}: {stats.get('calls', 0)} calls, {stats.get('total_tokens', 0)} tokens")

def main():
    """Main function"""
    try:
        runner = LocalLLMTestRunner()
        runner.run_all_modules()
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 