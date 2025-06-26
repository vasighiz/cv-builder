"""
Enhanced Resume Generator with RAG
Purpose: Generate personalized resumes using RAG and personal knowledge base
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnhancedResumeGenerator:
    """
    Enhanced resume generator with RAG capabilities
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the enhanced generator
        
        Args:
            api_key (str): OpenAI API key
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        
        # Load personal data
        self.personal_data = self._load_personal_data()
    
    def _load_personal_data(self) -> Dict[str, Any]:
        """
        Load your personal data from CV and other sources
        """
        return {
            "name": "Your Name",
            "email": "your.email@example.com",
            "phone": "+1 (555) 123-4567",
            "location": "City, State",
            "linkedin": "linkedin.com/in/yourprofile",
            "experience_years": 6,
            "education": [
                {
                    "degree": "Ph.D. in Computer Science",
                    "institution": "University of Windsor, ON, Canada",
                    "dates": "01/2020-04/2024",
                    "gpa": "96/100"
                },
                {
                    "degree": "M.Sc. in Computer Engineering",
                    "institution": "Polytechnic University of Tehran, Tehran, Iran",
                    "dates": "01/2015-04/2017",
                    "gpa": "3.75/4"
                }
            ],
            "work_experience": [
                {
                    "company": "ACTIC-ai",
                    "title": "Machine Learning Engineer",
                    "location": "Remote, Canada",
                    "dates": "11/2023-Present",
                    "achievements": [
                        "Developed multi-agent architectures for automating NGS data analysis resulting in 80% improvement in processing time",
                        "Launched RAG-based system resulting in 15% improvement in text processing time",
                        "Integrated prompt engineering and LLMs fine-tuning to enhance text summarization accuracy by 28%",
                        "Developed scalable data analysis pipelines using LLM models resulting in 15% improvement in data quality",
                        "Developed AI agent-based system resulting in client-ready automations saving 25 hours/week"
                    ]
                },
                {
                    "company": "University of Windsor",
                    "title": "Postdoctoral Fellow",
                    "location": "ON, Canada",
                    "dates": "07/2024-Present",
                    "achievements": [
                        "Developed scalable analysis pipelines for genomic datasets (CRISPR screen) on GPU clusters",
                        "Utilized LLMs to assist in scientific finding interpretation, improving research productivity",
                        "Ensured data quality, reproducibility, and compliance with scientific standards"
                    ]
                }
            ],
            "skills": {
                "frameworks": ["PyTorch", "TensorFlow", "MLOps", "RAG", "Fine-tuning LLMs"],
                "tools": ["Hugging Face Transformers", "LangChain", "Streamlit", "FastAPI", "AWS"],
                "programming": ["Python", "R"],
                "other": ["Communication", "Problem-solving", "JAX"]
            },
            "achievements": [
                "Ph.D. in Computer Science with 96/100 GPA",
                "Published research on SARS-CoV-2 and SCLC",
                "Delivered workshops to 100+ Master students",
                "Developed systems with 99% accuracy"
            ]
        }
    
    def create_enhanced_summary(self, job_description: str) -> str:
        """
        Create enhanced professional summary using personal data
        """
        prompt = f"""
        Create a compelling professional summary for a resume that matches this job description.
        
        JOB DESCRIPTION:
        {job_description}
        
        CANDIDATE PERSONAL INFORMATION:
        - Experience: {self.personal_data['experience_years']} years
        - Education: {[edu['degree'] for edu in self.personal_data['education']]}
        - Current Role: {self.personal_data['work_experience'][0]['title']} at {self.personal_data['work_experience'][0]['company']}
        
        KEY SKILLS:
        - Frameworks: {', '.join(self.personal_data['skills']['frameworks'])}
        - Tools: {', '.join(self.personal_data['skills']['tools'])}
        - Programming: {', '.join(self.personal_data['skills']['programming'])}
        
        TOP ACHIEVEMENTS:
        {chr(10).join([f"• {achievement}" for achievement in self.personal_data['achievements']])}
        
        INSTRUCTIONS:
        1. Use your specific experience years ({self.personal_data['experience_years']} years)
        2. Highlight your PhD and research background
        3. Emphasize your expertise in NGS data analysis and bioinformatics
        4. Mention your specific achievements (publications, workshops, high accuracy results)
        5. Show passion for the specific domain
        6. Use active, results-driven language
        7. Keep it to 3-4 sentences maximum
        8. Make it specific to this job, not generic
        
        Return ONLY the summary text, no additional formatting.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer specializing in creating compelling professional summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            summary_text = response.choices[0].message.content.strip()
            
            # Clean up any markdown or extra formatting
            if summary_text.startswith('"') and summary_text.endswith('"'):
                summary_text = summary_text[1:-1]
            
            return summary_text
            
        except Exception as e:
            print(f"Error generating enhanced summary: {e}")
            return f"Results-driven machine learning scientist with {self.personal_data['experience_years']} years of experience and a Ph.D. in Computer Science, specializing in developing and implementing advanced machine learning models."
    
    def generate_enhanced_resume(self, job_description: str) -> Dict[str, Any]:
        """
        Generate complete enhanced resume
        """
        print("🚀 Generating enhanced resume...")
        
        # Generate enhanced summary
        summary = self.create_enhanced_summary(job_description)
        
        # Create resume structure
        resume = {
            "header": {
                "name": self.personal_data["name"],
                "email": self.personal_data["email"],
                "phone": self.personal_data["phone"],
                "location": self.personal_data["location"],
                "linkedin": self.personal_data["linkedin"]
            },
            "summary": summary,
            "skills": self.personal_data["skills"],
            "experience": self.personal_data["work_experience"],
            "education": self.personal_data["education"]
        }
        
        print("✅ Enhanced resume generated successfully!")
        return resume
    
    def save_enhanced_resume(self, resume: Dict[str, Any], job_name: str, output_dir: Path) -> None:
        """
        Save enhanced resume to file
        """
        # Create job-specific output directory
        job_output_dir = output_dir / "jobs" / job_name / "enhanced"
        job_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_file = job_output_dir / f"enhanced_resume_{job_name}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(resume, f, indent=2, ensure_ascii=False)
        
        # Save text format
        txt_file = job_output_dir / f"enhanced_resume_{job_name}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("ENHANCED PROFESSIONAL RESUME\n")
            f.write("=" * 50 + "\n\n")
            
            # Header
            f.write(f"{resume['header']['name'].upper()}\n")
            f.write(f"{resume['header']['email']} | {resume['header']['phone']} | {resume['header']['location']}\n")
            f.write(f"LinkedIn: {resume['header']['linkedin']}\n\n")
            
            # Summary
            f.write("PROFESSIONAL SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"{resume['summary']}\n\n")
            
            # Skills
            f.write("TECHNICAL SKILLS\n")
            f.write("-" * 15 + "\n")
            f.write(f"Frameworks: {', '.join(resume['skills']['frameworks'])}\n")
            f.write(f"Tools: {', '.join(resume['skills']['tools'])}\n")
            f.write(f"Programming: {', '.join(resume['skills']['programming'])}\n")
            f.write(f"Other: {', '.join(resume['skills']['other'])}\n\n")
            
            # Experience
            f.write("PROFESSIONAL EXPERIENCE\n")
            f.write("-" * 25 + "\n")
            for exp in resume['experience']:
                f.write(f"{exp['title']} | {exp['company']} | {exp['location']} | {exp['dates']}\n")
                for achievement in exp['achievements'][:3]:  # Top 3 achievements
                    f.write(f"• {achievement}\n")
                f.write("\n")
            
            # Education
            f.write("EDUCATION\n")
            f.write("-" * 9 + "\n")
            for edu in resume['education']:
                f.write(f"{edu['degree']} | {edu['institution']} | {edu['dates']}\n")
        
        print(f"💾 Enhanced resume saved to:")
        print(f"   JSON: {json_file}")
        print(f"   Text: {txt_file}") 