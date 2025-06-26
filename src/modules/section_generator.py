"""
Module 3: Resume Sections Generator
Purpose: Auto-generate Skills, Experience, and Projects sections using job-aligned keywords
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from anthropic import Anthropic


@dataclass
class SkillItem:
    """Data structure for skill items with relevance ranking"""
    skill: str
    category: str
    relevance_score: float
    proficiency_level: str


@dataclass
class ExperienceBullet:
    """Data structure for work experience bullet points"""
    action_verb: str
    description: str
    quantified_result: str
    keywords_used: List[str]
    impact: str


@dataclass
class ProjectDescription:
    """Data structure for project descriptions"""
    name: str
    description: str
    technologies: List[str]
    outcomes: List[str]
    relevance_explanation: str


@dataclass
class GeneratedSections:
    """Data structure for generated resume sections"""
    skills_section: List[SkillItem]
    experience_bullets: List[ExperienceBullet]
    project_descriptions: List[ProjectDescription]
    skills_summary: str
    experience_summary: str
    projects_summary: str


class ResumeSectionGenerator:
    """
    Generates optimized resume sections based on job keywords and user data
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the generator with Anthropic API key
        
        Args:
            api_key (str): Anthropic API key
        """
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-haiku-20240307"
        
        # Action verbs for strong bullet points
        self.action_verbs = [
            "Developed", "Implemented", "Designed", "Built", "Created", "Optimized",
            "Improved", "Increased", "Reduced", "Managed", "Led", "Coordinated",
            "Analyzed", "Researched", "Evaluated", "Enhanced", "Streamlined",
            "Automated", "Deployed", "Maintained", "Troubleshot", "Configured"
        ]
        
    def generate_skills_section(self, job_keywords: Dict[str, Any], user_skills: List[str]) -> List[SkillItem]:
        """
        Generate optimized skills section with relevance ranking
        
        Args:
            job_keywords (Dict): Keywords from job description
            user_skills (List): User's current skills
            
        Returns:
            List[SkillItem]: Ranked skills with relevance scores
        """
        
        prompt = f"""
        Generate an optimized skills section for a resume based on job requirements.
        
        Job Keywords:
        Technical Skills: {job_keywords.get('technical_skills', [])}
        Tools & Technologies: {job_keywords.get('tools_technologies', [])}
        Soft Skills: {job_keywords.get('soft_skills', [])}
        
        User's Current Skills: {user_skills}
        
        Create a skills section that:
        1. Prioritizes skills that match job requirements
        2. Includes relevant skills from user's current set
        3. Suggests additional skills that would be valuable
        4. Categorizes skills appropriately
        5. Assigns relevance scores (0.0-1.0) based on job match
        
        Return as JSON:
        {{
            "skills": [
                {{
                    "skill": "string",
                    "category": "string (Programming Languages|Frameworks|Tools|Soft Skills)",
                    "relevance_score": float (0.0-1.0),
                    "proficiency_level": "string (Beginner|Intermediate|Advanced|Expert)"
                }}
            ]
        }}
        
        Focus on tech industry skills and ensure ATS-friendly formatting.
        """
        
        try:
            response = self.client.completion(
                prompt=prompt,
                model=self.model,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            parsed_data = json.loads(content)
            
            skills = []
            for skill_data in parsed_data.get("skills", []):
                skills.append(SkillItem(
                    skill=skill_data["skill"],
                    category=skill_data["category"],
                    relevance_score=skill_data["relevance_score"],
                    proficiency_level=skill_data["proficiency_level"]
                ))
            
            # Sort by relevance score
            skills.sort(key=lambda x: x.relevance_score, reverse=True)
            
            return skills
            
        except Exception as e:
            print(f"Error generating skills section: {e}")
            return []
    
    def generate_experience_bullets(self, job_keywords: Dict[str, Any], user_experience: List[Dict[str, Any]]) -> List[ExperienceBullet]:
        """
        Generate optimized work experience bullet points
        
        Args:
            job_keywords (Dict): Keywords from job description
            user_experience (List): User's work experience data
            
        Returns:
            List[ExperienceBullet]: Optimized bullet points
        """
        
        bullets = []
        
        for exp in user_experience:
            company = exp.get("company", "Unknown Company")
            title = exp.get("title", "Unknown Title")
            dates = exp.get("dates", "")
            achievements = exp.get("achievements", [])
            
            # Generate enhanced bullet points for this experience
            enhanced_bullets = self._generate_bullets_for_experience(
                job_keywords, company, title, dates, achievements
            )
            
            bullets.extend(enhanced_bullets)
        
        return bullets
    
    def _generate_bullets_for_experience(self, job_keywords: Dict[str, Any], company: str, title: str, dates: str, achievements: List[str]) -> List[ExperienceBullet]:
        """
        Generate bullet points for a specific work experience
        """
        
        prompt = f"""
        Generate optimized resume bullet points for this work experience:
        
        Company: {company}
        Title: {title}
        Dates: {dates}
        Current Achievements: {achievements}
        
        Job Keywords to incorporate:
        Technical Skills: {job_keywords.get('technical_skills', [])}
        Tools & Technologies: {job_keywords.get('tools_technologies', [])}
        Responsibilities: {job_keywords.get('responsibilities', [])}
        
        Create 3-4 bullet points that:
        1. Use strong action verbs
        2. Include quantified results (%, $, numbers)
        3. Incorporate relevant job keywords
        4. Follow ATS-friendly format
        5. Highlight impact and outcomes
        
        Return as JSON:
        {{
            "bullets": [
                {{
                    "action_verb": "string",
                    "description": "string",
                    "quantified_result": "string",
                    "keywords_used": ["keyword1", "keyword2"],
                    "impact": "string"
                }}
            ]
        }}
        
        Make each bullet point concise (1-2 lines) and impactful.
        """
        
        try:
            response = self.client.completion(
                prompt=prompt,
                model=self.model,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            parsed_data = json.loads(content)
            
            bullets = []
            for bullet_data in parsed_data.get("bullets", []):
                bullets.append(ExperienceBullet(
                    action_verb=bullet_data["action_verb"],
                    description=bullet_data["description"],
                    quantified_result=bullet_data["quantified_result"],
                    keywords_used=bullet_data["keywords_used"],
                    impact=bullet_data["impact"]
                ))
            
            return bullets
            
        except Exception as e:
            print(f"Error generating bullets for {company}: {e}")
            return []
    
    def generate_project_descriptions(self, job_keywords: Dict[str, Any], user_projects: List[Dict[str, Any]]) -> List[ProjectDescription]:
        """
        Generate optimized project descriptions
        
        Args:
            job_keywords (Dict): Keywords from job description
            user_projects (List): User's project data
            
        Returns:
            List[ProjectDescription]: Optimized project descriptions
        """
        
        descriptions = []
        
        for project in user_projects:
            name = project.get("name", "Unknown Project")
            current_desc = project.get("description", "")
            technologies = project.get("technologies", [])
            outcomes = project.get("outcomes", [])
            
            # Generate enhanced project description
            enhanced_desc = self._generate_project_description(
                job_keywords, name, current_desc, technologies, outcomes
            )
            
            descriptions.append(enhanced_desc)
        
        return descriptions
    
    def _generate_project_description(self, job_keywords: Dict[str, Any], name: str, current_desc: str, technologies: List[str], outcomes: List[str]) -> ProjectDescription:
        """
        Generate enhanced project description
        """
        
        prompt = f"""
        Generate an optimized project description for a resume:
        
        Project Name: {name}
        Current Description: {current_desc}
        Technologies Used: {technologies}
        Current Outcomes: {outcomes}
        
        Job Keywords to incorporate:
        Technical Skills: {job_keywords.get('technical_skills', [])}
        Tools & Technologies: {job_keywords.get('tools_technologies', [])}
        
        Create an enhanced project description that:
        1. Highlights relevant technologies and skills
        2. Emphasizes quantifiable outcomes and impact
        3. Uses job-relevant language
        4. Explains relevance to the target role
        5. Follows ATS-friendly formatting
        
        Return as JSON:
        {{
            "name": "string",
            "description": "string",
            "technologies": ["tech1", "tech2"],
            "outcomes": ["outcome1", "outcome2"],
            "relevance_explanation": "string"
        }}
        
        Make the description compelling and relevant to the job requirements.
        """
        
        try:
            response = self.client.completion(
                prompt=prompt,
                model=self.model,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            parsed_data = json.loads(content)
            
            return ProjectDescription(
                name=parsed_data["name"],
                description=parsed_data["description"],
                technologies=parsed_data["technologies"],
                outcomes=parsed_data["outcomes"],
                relevance_explanation=parsed_data["relevance_explanation"]
            )
            
        except Exception as e:
            print(f"Error generating project description for {name}: {e}")
            return ProjectDescription(
                name=name,
                description=current_desc,
                technologies=technologies,
                outcomes=outcomes,
                relevance_explanation=""
            )
    
    def generate_complete_sections(self, job_keywords: Dict[str, Any], user_data: Dict[str, Any]) -> GeneratedSections:
        """
        Generate all resume sections at once
        
        Args:
            job_keywords (Dict): Keywords from job description
            user_data (Dict): User's resume data
            
        Returns:
            GeneratedSections: Complete set of generated sections
        """
        
        # Generate skills section
        user_skills = user_data.get("technical_skills", []) + user_data.get("soft_skills", [])
        skills_section = self.generate_skills_section(job_keywords, user_skills)
        
        # Generate experience bullets
        experience_bullets = self.generate_experience_bullets(job_keywords, user_data.get("work_experience", []))
        
        # Generate project descriptions
        project_descriptions = self.generate_project_descriptions(job_keywords, user_data.get("projects", []))
        
        # Generate summaries
        skills_summary = self._generate_skills_summary(skills_section)
        experience_summary = self._generate_experience_summary(experience_bullets)
        projects_summary = self._generate_projects_summary(project_descriptions)
        
        return GeneratedSections(
            skills_section=skills_section,
            experience_bullets=experience_bullets,
            project_descriptions=project_descriptions,
            skills_summary=skills_summary,
            experience_summary=experience_summary,
            projects_summary=projects_summary
        )
    
    def _generate_skills_summary(self, skills: List[SkillItem]) -> str:
        """
        Generate a formatted skills summary
        """
        
        if not skills:
            return "Skills: [To be generated based on job requirements]"
        
        # Group skills by category
        categories = {}
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill)
        
        # Format skills by category
        formatted_sections = []
        for category, category_skills in categories.items():
            skill_names = [skill.skill for skill in category_skills[:8]]  # Limit to 8 per category
            formatted_sections.append(f"{category}: {', '.join(skill_names)}")
        
        return " | ".join(formatted_sections)
    
    def _generate_experience_summary(self, bullets: List[ExperienceBullet]) -> str:
        """
        Generate a summary of experience bullets
        """
        
        if not bullets:
            return "Experience: [To be generated based on job requirements]"
        
        # Count keywords used
        keyword_counts = {}
        for bullet in bullets:
            for keyword in bullet.keywords_used:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # Get top keywords
        top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return f"Experience highlights: {', '.join([kw for kw, _ in top_keywords])}"
    
    def _generate_projects_summary(self, projects: List[ProjectDescription]) -> str:
        """
        Generate a summary of project descriptions
        """
        
        if not projects:
            return "Projects: [To be generated based on job requirements]"
        
        # Get unique technologies used
        all_technologies = set()
        for project in projects:
            all_technologies.update(project.technologies)
        
        tech_list = list(all_technologies)[:6]  # Limit to 6 technologies
        
        return f"Project technologies: {', '.join(tech_list)}"
    
    def format_for_ats(self, sections: GeneratedSections) -> Dict[str, str]:
        """
        Format generated sections for ATS compatibility
        
        Args:
            sections (GeneratedSections): Generated sections
            
        Returns:
            Dict[str, str]: ATS-formatted sections
        """
        
        # Format skills section
        skills_text = "SKILLS\n"
        categories = {}
        for skill in sections.skills_section:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill.skill)
        
        for category, skills in categories.items():
            skills_text += f"{category}: {', '.join(skills)}\n"
        
        # Format experience section
        experience_text = "WORK EXPERIENCE\n"
        for i, bullet in enumerate(sections.experience_bullets, 1):
            experience_text += f"• {bullet.action_verb} {bullet.description} {bullet.quantified_result}\n"
        
        # Format projects section
        projects_text = "PROJECTS\n"
        for project in sections.project_descriptions:
            projects_text += f"{project.name}\n"
            projects_text += f"Technologies: {', '.join(project.technologies)}\n"
            projects_text += f"{project.description}\n"
            if project.outcomes:
                projects_text += f"Outcomes: {', '.join(project.outcomes)}\n"
            projects_text += "\n"
        
        return {
            "skills": skills_text.strip(),
            "experience": experience_text.strip(),
            "projects": projects_text.strip(),
            "summary": f"{sections.skills_summary}\n{sections.experience_summary}\n{sections.projects_summary}"
        }


def main():
    """
    Example usage of the ResumeSectionGenerator
    """
    
    # Sample job keywords
    job_keywords = {
        "technical_skills": ["Python", "Machine Learning", "SQL", "TensorFlow", "Data Analysis", "Deep Learning"],
        "tools_technologies": ["AWS", "Docker", "Git", "Jupyter", "Pandas", "NumPy"],
        "soft_skills": ["Communication", "Problem Solving", "Teamwork", "Leadership"],
        "responsibilities": ["Model Development", "Data Processing", "Algorithm Optimization", "Team Collaboration"]
    }
    
    # Sample user data
    user_data = {
        "technical_skills": ["Python", "JavaScript", "React", "Node.js"],
        "soft_skills": ["Communication", "Teamwork"],
        "work_experience": [
            {
                "company": "TechCorp",
                "title": "Software Engineer",
                "dates": "2020-2023",
                "achievements": [
                    "Developed web applications using React",
                    "Improved application performance",
                    "Collaborated with team members"
                ]
            }
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "description": "Built a full-stack e-commerce application",
                "technologies": ["React", "Node.js", "MongoDB"],
                "outcomes": ["User authentication", "Payment processing"]
            }
        ]
    }
    
    # Initialize generator
    api_key = "your_anthropic_api_key_here"  # Replace with actual API key
    generator = ResumeSectionGenerator(api_key)
    
    # Generate complete sections
    sections = generator.generate_complete_sections(job_keywords, user_data)
    
    # Print results
    print("=== Generated Skills Section ===")
    for skill in sections.skills_section[:5]:
        print(f"• {skill.skill} ({skill.category}) - Relevance: {skill.relevance_score:.2f}")
    
    print("\n=== Generated Experience Bullets ===")
    for bullet in sections.experience_bullets[:3]:
        print(f"• {bullet.action_verb} {bullet.description} {bullet.quantified_result}")
        print(f"  Keywords: {', '.join(bullet.keywords_used)}")
    
    print("\n=== Generated Project Descriptions ===")
    for project in sections.project_descriptions:
        print(f"• {project.name}")
        print(f"  Technologies: {', '.join(project.technologies)}")
        print(f"  Description: {project.description}")
    
    # Format for ATS
    ats_formatted = generator.format_for_ats(sections)
    
    print("\n=== ATS Formatted Sections ===")
    print("SKILLS:")
    print(ats_formatted["skills"])
    print("\nEXPERIENCE:")
    print(ats_formatted["experience"])
    print("\nPROJECTS:")
    print(ats_formatted["projects"])


if __name__ == "__main__":
    main() 