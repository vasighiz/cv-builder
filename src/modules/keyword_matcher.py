"""
Module 2: Resume Keyword Matcher
Purpose: Compare user's resume against extracted keywords and provide gap analysis
"""

import json
import re
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from openai import OpenAI
import pandas as pd


@dataclass
class KeywordMatch:
    """Data structure for keyword matching results"""
    keyword: str
    category: str
    found_in_resume: bool
    frequency_in_jd: int
    frequency_in_resume: int
    relevance_score: float


@dataclass
class GapAnalysis:
    """Data structure for gap analysis results"""
    covered_keywords: List[KeywordMatch]
    missing_keywords: List[KeywordMatch]
    coverage_percentage: float
    recommendations: List[str]
    priority_keywords: List[str]


class ResumeKeywordMatcher:
    """
    Compares user's resume against job keywords and provides gap analysis
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the matcher with OpenAI API key
        
        Args:
            api_key (str): OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        
    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse resume text to extract sections and keywords
        
        Args:
            resume_text (str): Raw resume text
            
        Returns:
            Dict: Parsed resume sections and keywords
        """
        
        prompt = f"""
        Parse the following resume and extract structured information:
        
        Resume:
        {resume_text}
        
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
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume parser specializing in tech industry resumes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Error parsing resume: {e}")
            return {
                "technical_skills": [],
                "soft_skills": [],
                "work_experience": [],
                "projects": [],
                "education": [],
                "certifications": [],
                "extracted_keywords": []
            }
    
    def match_keywords(self, job_keywords: Dict[str, Any], resume_data: Dict[str, Any]) -> GapAnalysis:
        """
        Match job keywords against resume content
        
        Args:
            job_keywords (Dict): Keywords extracted from job description
            resume_data (Dict): Parsed resume data
            
        Returns:
            GapAnalysis: Comprehensive gap analysis results
        """
        
        # Combine all resume keywords
        resume_keywords = set()
        resume_keywords.update(resume_data.get("technical_skills", []))
        resume_keywords.update(resume_data.get("soft_skills", []))
        resume_keywords.update(resume_data.get("extracted_keywords", []))
        
        # Add keywords from projects and work experience
        for project in resume_data.get("projects", []):
            resume_keywords.update(project.get("technologies", []))
        
        for exp in resume_data.get("work_experience", []):
            for achievement in exp.get("achievements", []):
                # Extract potential keywords from achievements
                keywords = self._extract_keywords_from_text(achievement)
                resume_keywords.update(keywords)
        
        # Convert to lowercase for matching
        resume_keywords_lower = {kw.lower() for kw in resume_keywords}
        
        # Match against job keywords
        covered_keywords = []
        missing_keywords = []
        
        # Technical skills matching
        for skill in job_keywords.get("technical_skills", []):
            match = self._create_keyword_match(
                skill, "technical_skills", 
                job_keywords.get("keywords_frequency", {}).get(skill, 1),
                resume_keywords_lower
            )
            if match.found_in_resume:
                covered_keywords.append(match)
            else:
                missing_keywords.append(match)
        
        # Soft skills matching
        for skill in job_keywords.get("soft_skills", []):
            match = self._create_keyword_match(
                skill, "soft_skills",
                job_keywords.get("keywords_frequency", {}).get(skill, 1),
                resume_keywords_lower
            )
            if match.found_in_resume:
                covered_keywords.append(match)
            else:
                missing_keywords.append(match)
        
        # Tools and technologies matching
        for tool in job_keywords.get("tools_technologies", []):
            match = self._create_keyword_match(
                tool, "tools_technologies",
                job_keywords.get("keywords_frequency", {}).get(tool, 1),
                resume_keywords_lower
            )
            if match.found_in_resume:
                covered_keywords.append(match)
            else:
                missing_keywords.append(match)
        
        # Calculate coverage percentage
        total_keywords = len(covered_keywords) + len(missing_keywords)
        coverage_percentage = (len(covered_keywords) / total_keywords * 100) if total_keywords > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(covered_keywords, missing_keywords, resume_data)
        
        # Identify priority keywords (high frequency in JD, missing in resume)
        priority_keywords = self._identify_priority_keywords(missing_keywords)
        
        return GapAnalysis(
            covered_keywords=covered_keywords,
            missing_keywords=missing_keywords,
            coverage_percentage=coverage_percentage,
            recommendations=recommendations,
            priority_keywords=priority_keywords
        )
    
    def _create_keyword_match(self, keyword: str, category: str, jd_frequency: int, resume_keywords: set) -> KeywordMatch:
        """
        Create a keyword match object
        """
        
        # Check if keyword is found in resume (with fuzzy matching)
        found = self._fuzzy_match(keyword, resume_keywords)
        resume_frequency = 1 if found else 0
        
        # Calculate relevance score based on JD frequency
        relevance_score = min(jd_frequency / 5.0, 1.0)  # Normalize to 0-1
        
        return KeywordMatch(
            keyword=keyword,
            category=category,
            found_in_resume=found,
            frequency_in_jd=jd_frequency,
            frequency_in_resume=resume_frequency,
            relevance_score=relevance_score
        )
    
    def _fuzzy_match(self, keyword: str, resume_keywords: set) -> bool:
        """
        Perform fuzzy matching between keyword and resume keywords
        """
        
        keyword_lower = keyword.lower()
        
        # Exact match
        if keyword_lower in resume_keywords:
            return True
        
        # Partial match (keyword is part of resume keyword or vice versa)
        for resume_kw in resume_keywords:
            if keyword_lower in resume_kw or resume_kw in keyword_lower:
                return True
        
        # Common variations
        variations = [
            keyword_lower.replace(" ", ""),
            keyword_lower.replace("-", ""),
            keyword_lower.replace("_", ""),
            keyword_lower.replace(".", "")
        ]
        
        for variation in variations:
            if variation in resume_keywords:
                return True
        
        return False
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """
        Extract potential keywords from text
        """
        
        # Simple keyword extraction (can be enhanced with NLP)
        keywords = []
        
        # Common tech keywords
        tech_keywords = [
            'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'angular',
            'node.js', 'django', 'flask', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'matplotlib', 'seaborn', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'git', 'jenkins', 'agile', 'scrum'
        ]
        
        text_lower = text.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return keywords
    
    def _generate_recommendations(self, covered: List[KeywordMatch], missing: List[KeywordMatch], resume_data: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on gap analysis
        """
        
        recommendations = []
        
        # Coverage recommendations
        coverage_percentage = len(covered) / (len(covered) + len(missing)) * 100 if (len(covered) + len(missing)) > 0 else 0
        
        if coverage_percentage < 60:
            recommendations.append("Your resume has low keyword coverage. Consider adding more relevant skills and experiences.")
        elif coverage_percentage < 80:
            recommendations.append("Your resume has moderate keyword coverage. Focus on adding missing high-priority skills.")
        else:
            recommendations.append("Great keyword coverage! Focus on optimizing your existing content.")
        
        # Missing skills recommendations
        missing_technical = [kw for kw in missing if kw.category == "technical_skills"]
        missing_tools = [kw for kw in missing if kw.category == "tools_technologies"]
        
        if missing_technical:
            top_missing = sorted(missing_technical, key=lambda x: x.relevance_score, reverse=True)[:3]
            recommendations.append(f"Add these technical skills: {', '.join([kw.keyword for kw in top_missing])}")
        
        if missing_tools:
            top_missing = sorted(missing_tools, key=lambda x: x.relevance_score, reverse=True)[:3]
            recommendations.append(f"Add these tools/technologies: {', '.join([kw.keyword for kw in top_missing])}")
        
        # Experience recommendations
        if not resume_data.get("work_experience"):
            recommendations.append("Add relevant work experience or internships to your resume")
        
        if not resume_data.get("projects"):
            recommendations.append("Include personal or academic projects that demonstrate relevant skills")
        
        # Quantification recommendations
        work_exp = resume_data.get("work_experience", [])
        has_quantified = any(
            any(any(char.isdigit() for char in achievement) for achievement in exp.get("achievements", []))
            for exp in work_exp
        )
        
        if not has_quantified and work_exp:
            recommendations.append("Add quantified achievements (numbers, percentages, metrics) to your work experience")
        
        return recommendations
    
    def _identify_priority_keywords(self, missing_keywords: List[KeywordMatch]) -> List[str]:
        """
        Identify high-priority missing keywords
        """
        
        # Sort by relevance score and frequency
        priority_keywords = sorted(
            missing_keywords,
            key=lambda x: (x.relevance_score, x.frequency_in_jd),
            reverse=True
        )
        
        return [kw.keyword for kw in priority_keywords[:10]]
    
    def generate_enhanced_resume_suggestions(self, gap_analysis: GapAnalysis, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate specific suggestions for enhancing resume sections
        """
        
        suggestions = {
            "skills_section": self._suggest_skills_enhancements(gap_analysis, resume_data),
            "experience_section": self._suggest_experience_enhancements(gap_analysis, resume_data),
            "projects_section": self._suggest_projects_enhancements(gap_analysis, resume_data),
            "overall_improvements": gap_analysis.recommendations
        }
        
        return suggestions
    
    def _suggest_skills_enhancements(self, gap_analysis: GapAnalysis, resume_data: Dict[str, Any]) -> List[str]:
        """
        Suggest enhancements for skills section
        """
        
        suggestions = []
        
        # Add missing high-priority skills
        missing_skills = [kw for kw in gap_analysis.missing_keywords if kw.category == "technical_skills"]
        if missing_skills:
            top_skills = sorted(missing_skills, key=lambda x: x.relevance_score, reverse=True)[:5]
            suggestions.append(f"Add these technical skills: {', '.join([kw.keyword for kw in top_skills])}")
        
        # Suggest skill organization
        current_skills = resume_data.get("technical_skills", [])
        if len(current_skills) > 10:
            suggestions.append("Consider organizing skills by category (Programming Languages, Frameworks, Tools, etc.)")
        
        return suggestions
    
    def _suggest_experience_enhancements(self, gap_analysis: GapAnalysis, resume_data: Dict[str, Any]) -> List[str]:
        """
        Suggest enhancements for experience section
        """
        
        suggestions = []
        
        # Check for quantified achievements
        work_exp = resume_data.get("work_experience", [])
        for exp in work_exp:
            achievements = exp.get("achievements", [])
            quantified_count = sum(1 for achievement in achievements if any(char.isdigit() for char in achievement))
            
            if quantified_count < len(achievements) * 0.5:
                suggestions.append(f"Add more quantified achievements to your role at {exp.get('company', 'Unknown')}")
        
        # Suggest adding missing keywords to experience
        missing_keywords = [kw.keyword for kw in gap_analysis.missing_keywords[:5]]
        if missing_keywords and work_exp:
            suggestions.append(f"Incorporate these keywords into your work experience: {', '.join(missing_keywords)}")
        
        return suggestions
    
    def _suggest_projects_enhancements(self, gap_analysis: GapAnalysis, resume_data: Dict[str, Any]) -> List[str]:
        """
        Suggest enhancements for projects section
        """
        
        suggestions = []
        
        projects = resume_data.get("projects", [])
        
        if not projects:
            suggestions.append("Add personal or academic projects that demonstrate relevant technical skills")
        else:
            # Check if projects use relevant technologies
            project_techs = set()
            for project in projects:
                project_techs.update(project.get("technologies", []))
            
            missing_techs = [kw.keyword for kw in gap_analysis.missing_keywords if kw.category == "tools_technologies"][:3]
            if missing_techs:
                suggestions.append(f"Consider adding projects that use: {', '.join(missing_techs)}")
        
        return suggestions


def main():
    """
    Example usage of the ResumeKeywordMatcher
    """
    
    # Sample job keywords (from Module 1 output)
    job_keywords = {
        "technical_skills": ["Python", "Machine Learning", "SQL", "TensorFlow", "Data Analysis"],
        "soft_skills": ["Communication", "Problem Solving", "Teamwork"],
        "tools_technologies": ["AWS", "Docker", "Git", "Jupyter"],
        "keywords_frequency": {
            "Python": 3,
            "Machine Learning": 2,
            "SQL": 2,
            "TensorFlow": 1,
            "Data Analysis": 2
        }
    }
    
    # Sample resume data
    sample_resume = """
    John Doe
    Software Engineer
    
    SKILLS:
    Python, JavaScript, React, Node.js, Git
    
    EXPERIENCE:
    Software Engineer at TechCorp (2020-2023)
    - Developed web applications using React and Node.js
    - Collaborated with team members on various projects
    - Improved application performance by 20%
    
    PROJECTS:
    E-commerce Platform
    - Built using React and Node.js
    - Implemented user authentication and payment processing
    """
    
    # Initialize matcher
    api_key = "your_openai_api_key_here"  # Replace with actual API key
    matcher = ResumeKeywordMatcher(api_key)
    
    # Parse resume
    resume_data = matcher.parse_resume(sample_resume)
    
    # Match keywords
    gap_analysis = matcher.match_keywords(job_keywords, resume_data)
    
    # Print results
    print("=== Keyword Matching Results ===")
    print(f"Coverage: {gap_analysis.coverage_percentage:.1f}%")
    
    print("\n=== Covered Keywords ===")
    for kw in gap_analysis.covered_keywords[:5]:
        print(f"✓ {kw.keyword} ({kw.category})")
    
    print("\n=== Missing Keywords ===")
    for kw in gap_analysis.missing_keywords[:5]:
        print(f"✗ {kw.keyword} ({kw.category}) - Priority: {kw.relevance_score:.2f}")
    
    print("\n=== Recommendations ===")
    for rec in gap_analysis.recommendations:
        print(f"- {rec}")
    
    # Generate enhancement suggestions
    suggestions = matcher.generate_enhanced_resume_suggestions(gap_analysis, resume_data)
    
    print("\n=== Enhancement Suggestions ===")
    for section, section_suggestions in suggestions.items():
        if section_suggestions:
            print(f"\n{section.upper()}:")
            for suggestion in section_suggestions:
                print(f"  - {suggestion}")


if __name__ == "__main__":
    main() 