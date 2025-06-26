"""
Module 4: Enhanced Resume Generator with Local/API LLM Support
Purpose: Generate enhanced resume sections using local or API LLM models
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Import our LLM interface
from .llm_interface import LLMInterface, create_llm_interface

# Load environment variables
load_dotenv()

@dataclass
class EnhancedSection:
    """Data class for enhanced resume sections"""
    title: str
    content: List[str]
    enhancement_type: str
    original_content: List[str]
    improvements: List[str]

class EnhancedResumeGenerator:
    """Generate enhanced resume sections using local or API LLM models"""
    
    def __init__(self, llm_provider: str = "local"):
        """
        Initialize enhanced resume generator
        
        Args:
            llm_provider (str): 'local' or 'api' for LLM provider
        """
        self.llm = create_llm_interface(llm_provider)
        self.enhancement_history = []
        
    def enhance_professional_summary(self, original_summary: str, job_requirements: List[str], 
                                   candidate_skills: List[str]) -> EnhancedSection:
        """Enhance professional summary using LLM"""
        
        prompt = f"""
        Enhance this professional summary for a resume to better match the job requirements.
        
        ORIGINAL SUMMARY:
        {original_summary}
        
        JOB REQUIREMENTS:
        {', '.join(job_requirements)}
        
        CANDIDATE SKILLS:
        {', '.join(candidate_skills)}
        
        Create an enhanced professional summary that:
        1. Maintains the core message of the original
        2. Incorporates relevant job requirements
        3. Highlights matching skills
        4. Uses stronger action verbs
        5. Is 3-4 sentences maximum
        6. Maintains professional tone
        
        Return ONLY the enhanced summary text.
        """
        
        enhanced_content = self.llm.generate_response(prompt)
        
        if not enhanced_content:
            # Fallback to original content
            enhanced_content = original_summary
        
        # Identify improvements
        improvements = self._identify_improvements(original_summary, enhanced_content)
        
        return EnhancedSection(
            title="PROFESSIONAL SUMMARY",
            content=[enhanced_content],
            enhancement_type="summary_enhancement",
            original_content=[original_summary],
            improvements=improvements
        )
    
    def enhance_work_experience(self, experience_bullets: List[str], job_keywords: List[str]) -> EnhancedSection:
        """Enhance work experience bullets using LLM"""
        
        enhanced_bullets = []
        improvements = []
        
        for i, bullet in enumerate(experience_bullets):
            prompt = f"""
            Enhance this work experience bullet point to better match the job requirements.
            
            ORIGINAL BULLET:
            {bullet}
            
            JOB KEYWORDS TO INCORPORATE:
            {', '.join(job_keywords)}
            
            Create an enhanced bullet point that:
            1. Uses stronger action verbs
            2. Incorporates relevant keywords naturally
            3. Quantifies achievements where possible
            4. Maintains the core achievement
            5. Is one sentence maximum
            
            Return ONLY the enhanced bullet point.
            """
            
            enhanced_bullet = self.llm.generate_response(prompt)
            
            if enhanced_bullet:
                enhanced_bullets.append(enhanced_bullet)
                improvements.append(f"Enhanced bullet {i+1}: {bullet[:50]}... → {enhanced_bullet[:50]}...")
            else:
                enhanced_bullets.append(bullet)
                improvements.append(f"Kept original bullet {i+1} (enhancement failed)")
        
        return EnhancedSection(
            title="WORK EXPERIENCE",
            content=enhanced_bullets,
            enhancement_type="experience_enhancement",
            original_content=experience_bullets,
            improvements=improvements
        )
    
    def enhance_skills_section(self, skills: List[str], job_requirements: List[str]) -> EnhancedSection:
        """Enhance skills section using LLM"""
        
        prompt = f"""
        Enhance this skills section to better match the job requirements.
        
        CURRENT SKILLS:
        {', '.join(skills)}
        
        JOB REQUIREMENTS:
        {', '.join(job_requirements)}
        
        Create an enhanced skills list that:
        1. Prioritizes skills that match job requirements
        2. Groups related skills together
        3. Uses industry-standard terminology
        4. Includes relevant skill levels where appropriate
        5. Maintains all original skills
        
        Return the enhanced skills as a comma-separated list.
        """
        
        enhanced_skills_text = self.llm.generate_response(prompt)
        
        if enhanced_skills_text:
            # Parse the enhanced skills
            enhanced_skills = [skill.strip() for skill in enhanced_skills_text.split(',')]
        else:
            enhanced_skills = skills
        
        improvements = [f"Enhanced skills section with {len(enhanced_skills)} skills"]
        
        return EnhancedSection(
            title="SKILLS",
            content=enhanced_skills,
            enhancement_type="skills_enhancement",
            original_content=skills,
            improvements=improvements
        )
    
    def generate_ats_optimized_content(self, original_content: str, job_description: str) -> EnhancedSection:
        """Generate ATS-optimized content using LLM"""
        
        prompt = f"""
        Optimize this resume content for ATS (Applicant Tracking System) compatibility.
        
        ORIGINAL CONTENT:
        {original_content}
        
        JOB DESCRIPTION:
        {job_description}
        
        Create ATS-optimized content that:
        1. Uses relevant keywords from the job description
        2. Maintains natural language flow
        3. Avoids keyword stuffing
        4. Uses standard formatting
        5. Includes quantifiable achievements
        6. Matches job requirements
        
        Return ONLY the optimized content.
        """
        
        optimized_content = self.llm.generate_response(prompt)
        
        if not optimized_content:
            optimized_content = original_content
        
        improvements = ["ATS optimization applied", "Keywords integrated naturally"]
        
        return EnhancedSection(
            title="ATS OPTIMIZED CONTENT",
            content=[optimized_content],
            enhancement_type="ats_optimization",
            original_content=[original_content],
            improvements=improvements
        )
    
    def _identify_improvements(self, original: str, enhanced: str) -> List[str]:
        """Identify specific improvements made"""
        improvements = []
        
        # Check for action verbs
        action_verbs = ['developed', 'implemented', 'managed', 'led', 'created', 'designed', 'optimized']
        enhanced_lower = enhanced.lower()
        
        for verb in action_verbs:
            if verb in enhanced_lower:
                improvements.append(f"Added strong action verb: {verb}")
        
        # Check for quantification
        import re
        numbers = re.findall(r'\d+', enhanced)
        if numbers:
            improvements.append(f"Added quantification: {len(numbers)} numbers")
        
        # Check for keywords
        if len(enhanced) > len(original):
            improvements.append("Enhanced content length")
        
        return improvements
    
    def switch_llm_provider(self, provider: str) -> bool:
        """Switch between local and API LLM providers"""
        return self.llm.set_provider(provider)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get LLM usage statistics"""
        return self.llm.get_usage_stats()
    
    def generate_enhanced_resume(self, job_name: str, output_dir: Path, 
                                llm_provider: str = "local") -> Dict[str, Any]:
        """
        Generate enhanced resume using specified LLM provider
        
        Args:
            job_name (str): Name of the job
            output_dir (Path): Output directory path
            llm_provider (str): 'local' or 'api' for LLM provider
            
        Returns:
            Dict: Enhanced resume data
        """
        # Switch to specified provider
        self.switch_llm_provider(llm_provider)
        
        # Load existing resume data
        job_dir = output_dir / "jobs" / job_name
        module5_dir = job_dir / "module5"
        
        if not module5_dir.exists():
            raise ValueError(f"No existing resume found for job: {job_name}")
        
        # Load the most recent resume
        resume_files = list(module5_dir.glob("final_resume_*.json"))
        if not resume_files:
            raise ValueError(f"No resume files found for job: {job_name}")
        
        latest_resume = max(resume_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_resume, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        
        # Enhance each section
        enhanced_sections = []
        
        for section in resume_data.get('sections', []):
            section_title = section.get('title', '')
            section_content = section.get('content', [])
            
            if section_title == "PROFESSIONAL SUMMARY":
                # Enhance summary
                enhanced_section = self.enhance_professional_summary(
                    section_content[0] if section_content else "",
                    ["machine learning", "data analysis", "python"],  # Example requirements
                    ["python", "sql", "machine learning"]  # Example skills
                )
                enhanced_sections.append(enhanced_section)
                
            elif section_title == "PROFESSIONAL EXPERIENCE":
                # Enhance experience
                enhanced_section = self.enhance_work_experience(
                    section_content,
                    ["python", "machine learning", "data analysis"]
                )
                enhanced_sections.append(enhanced_section)
                
            elif section_title == "TECHNICAL SKILLS":
                # Enhance skills
                enhanced_section = self.enhance_skills_section(
                    section_content,
                    ["python", "machine learning", "data analysis", "sql"]
                )
                enhanced_sections.append(enhanced_section)
                
            else:
                # Keep other sections as-is
                enhanced_sections.append(EnhancedSection(
                    title=section_title,
                    content=section_content,
                    enhancement_type="no_enhancement",
                    original_content=section_content,
                    improvements=["No enhancement applied"]
                ))
        
        # Create enhanced resume data
        enhanced_resume = {
            "job_name": job_name,
            "timestamp": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            "llm_provider": llm_provider,
            "enhanced_sections": [
                {
                    "title": section.title,
                    "content": section.content,
                    "enhancement_type": section.enhancement_type,
                    "original_content": section.original_content,
                    "improvements": section.improvements
                }
                for section in enhanced_sections
            ],
            "usage_stats": self.get_usage_stats()
        }
        
        # Save enhanced resume
        enhanced_dir = job_dir / "enhanced"
        enhanced_dir.mkdir(exist_ok=True)
        
        enhanced_file = enhanced_dir / f"enhanced_resume_{enhanced_resume['timestamp']}.json"
        with open(enhanced_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_resume, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Enhanced resume saved to: {enhanced_file}")
        print(f"🤖 Used LLM provider: {llm_provider}")
        
        return enhanced_resume

# Example usage
def test_enhanced_generator():
    """Test the enhanced resume generator"""
    print("🚀 Testing Enhanced Resume Generator")
    print("=" * 50)
    
    # Create generator with local LLM
    generator = EnhancedResumeGenerator(llm_provider="local")
    
    # Test summary enhancement
    original_summary = "Experienced data scientist with Python skills."
    enhanced_section = generator.enhance_professional_summary(
        original_summary,
        ["machine learning", "data analysis", "python"],
        ["python", "sql", "machine learning"]
    )
    
    print(f"Original: {enhanced_section.original_content[0]}")
    print(f"Enhanced: {enhanced_section.content[0]}")
    print(f"Improvements: {enhanced_section.improvements}")
    
    # Show usage stats
    stats = generator.get_usage_stats()
    print(f"\n📊 Usage Stats: {stats}")

if __name__ == "__main__":
    test_enhanced_generator() 