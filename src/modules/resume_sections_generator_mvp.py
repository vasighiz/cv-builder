"""
Module 3 MVP: Resume Sections Generator
Purpose: Auto-generate Skills, Experience, and Projects sections using job-aligned keywords
Simplified version for testing and integration
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()


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
    company: str = ""
    title: str = ""


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


class ResumeSectionsGeneratorMVP:
    """
    MVP version of resume sections generator
    Generates optimized resume sections based on job keywords and user data
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the generator with OpenAI API key
        
        Args:
            api_key (str): OpenAI API key (optional, will use env var if not provided)
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        
        # Action verbs for strong bullet points
        self.action_verbs = [
            "Developed", "Implemented", "Designed", "Built", "Created", "Optimized",
            "Improved", "Increased", "Reduced", "Managed", "Led", "Coordinated",
            "Analyzed", "Researched", "Evaluated", "Enhanced", "Streamlined",
            "Automated", "Deployed", "Maintained", "Troubleshot", "Configured"
        ]
    
    def generate_skills_section(self, job_analysis: Dict[str, Any], user_skills: List[str] = None) -> List[SkillItem]:
        """
        Generate optimized skills section with relevance ranking
        
        Args:
            job_analysis (Dict): Complete job analysis from Module 1
            user_skills (List): User's current skills (optional)
            
        Returns:
            List[SkillItem]: Ranked skills with relevance scores
        """
        
        # Extract keywords from job analysis
        job_keywords = job_analysis.get('keywords', {})
        technical_skills = job_keywords.get('technical_skills', [])
        tools_technologies = job_keywords.get('tools_technologies', [])
        soft_skills = job_keywords.get('soft_skills', [])
        
        # Combine all job skills
        all_job_skills = technical_skills + tools_technologies + soft_skills
        
        # If no user skills provided, use job skills as base
        if user_skills is None:
            user_skills = all_job_skills
        
        prompt = f"""
        Generate an optimized skills section for a resume based on job requirements.
        
        Job Analysis:
        - Role: {job_analysis.get('role_analysis', {}).get('role_category', 'Unknown')}
        - Level: {job_analysis.get('role_analysis', {}).get('seniority_level', 'Unknown')}
        - Industry: {job_analysis.get('role_analysis', {}).get('industry_focus', 'Unknown')}
        
        Job Keywords:
        - Technical Skills: {technical_skills}
        - Tools & Technologies: {tools_technologies}
        - Soft Skills: {soft_skills}
        
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
        Limit to 15-20 most relevant skills.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer specializing in tech industry skills optimization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
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
            # Return fallback skills based on job keywords
            fallback_skills = []
            for skill in all_job_skills[:10]:  # Limit to 10 skills
                fallback_skills.append(SkillItem(
                    skill=skill,
                    category="Technical Skills" if skill in technical_skills else "Tools" if skill in tools_technologies else "Soft Skills",
                    relevance_score=0.8,
                    proficiency_level="Intermediate"
                ))
            return fallback_skills
    
    def generate_experience_bullets(self, job_analysis: Dict[str, Any], user_experience: List[Dict[str, Any]] = None) -> List[ExperienceBullet]:
        """
        Generate optimized work experience bullet points
        
        Args:
            job_analysis (Dict): Complete job analysis from Module 1
            user_experience (List): User's work experience data (optional)
            
        Returns:
            List[ExperienceBullet]: Optimized experience bullet points
        """
        
        # Extract job keywords
        job_keywords = job_analysis.get('keywords', {})
        technical_skills = job_keywords.get('technical_skills', [])
        tools_technologies = job_keywords.get('tools_technologies', [])
        soft_skills = job_keywords.get('soft_skills', [])
        
        # Enhanced action verbs with more variety
        self.action_verbs = [
            "Developed", "Implemented", "Designed", "Built", "Created", "Optimized",
            "Improved", "Increased", "Reduced", "Managed", "Led", "Coordinated",
            "Analyzed", "Researched", "Evaluated", "Enhanced", "Streamlined",
            "Automated", "Deployed", "Maintained", "Troubleshot", "Configured",
            "Architected", "Engineered", "Delivered", "Scaled", "Transformed",
            "Revolutionized", "Pioneered", "Spearheaded", "Orchestrated", "Facilitated",
            "Accelerated", "Maximized", "Minimized", "Boosted", "Elevated", "Amplified",
            "Catalyzed", "Drove", "Generated", "Produced", "Achieved", "Accomplished",
            "Executed", "Launched", "Established", "Founded", "Initiated", "Started"
        ]
        
        # Quantified result templates
        quantified_results = [
            "resulting in a {percentage}% improvement in {metric}",
            "leading to a {percentage}% increase in {metric}",
            "achieving a {percentage}% reduction in {metric}",
            "delivering {percentage}% faster {metric}",
            "boosting {metric} by {percentage}%",
            "improving {metric} efficiency by {percentage}%",
            "reducing {metric} costs by ${amount}",
            "saving ${amount} in {metric}",
            "generating ${amount} in {metric}",
            "processing {number} {items} per {timeframe}",
            "handling {number} {items} simultaneously",
            "supporting {number} {users}",
            "managing {number} {projects}",
            "training {number} {people}",
            "deploying {number} {systems}"
        ]
        
        # Metrics for different roles
        metrics = {
            "performance": ["system performance", "application speed", "processing time", "response time", "throughput"],
            "efficiency": ["operational efficiency", "workflow efficiency", "resource utilization", "productivity"],
            "accuracy": ["model accuracy", "prediction accuracy", "data accuracy", "system reliability"],
            "cost": ["operational costs", "infrastructure costs", "maintenance costs", "development costs"],
            "revenue": ["revenue", "sales", "income", "profit", "ROI"],
            "users": ["user engagement", "user satisfaction", "user adoption", "user retention"],
            "data": ["data processing", "data analysis", "data quality", "data throughput"]
        }
        
        bullets = []
        
        # Generate enhanced bullets from user experience if available
        if user_experience:
            for exp in user_experience:
                company = exp.get('company', 'Company')
                title = exp.get('title', 'Role')
                achievements = exp.get('achievements', [])
                
                # Generate multiple bullets for each experience
                for achievement in achievements[:3]:  # Limit to 3 per role
                    bullet = self._create_enhanced_bullet(
                        achievement, technical_skills, tools_technologies, 
                        quantified_results, metrics, company, title
                    )
                    if bullet:
                        bullets.append(bullet)
        
        # Generate recommended bullets based on job requirements
        recommended_bullets = self._generate_recommended_bullets(
            job_analysis, technical_skills, tools_technologies, 
            quantified_results, metrics
        )
        bullets.extend(recommended_bullets)
        
        # Sort by relevance and limit to top 8-10 bullets
        bullets.sort(key=lambda x: len(x.keywords_used), reverse=True)
        return bullets[:10]
    
    def _create_enhanced_bullet(self, achievement: str, technical_skills: List[str], 
                               tools_technologies: List[str], quantified_results: List[str],
                               metrics: Dict[str, List[str]], company: str, title: str) -> ExperienceBullet:
        """Create enhanced bullet point from user achievement"""
        
        # Extract relevant keywords from achievement
        achievement_lower = achievement.lower()
        relevant_keywords = []
        
        for skill in technical_skills + tools_technologies:
            if skill.lower() in achievement_lower:
                relevant_keywords.append(skill)
        
        # Choose action verb
        action_verb = "Enhanced"  # Default
        if any(word in achievement_lower for word in ["led", "lead", "managed"]):
            action_verb = "Led"
        elif any(word in achievement_lower for word in ["developed", "built", "created"]):
            action_verb = "Developed"
        elif any(word in achievement_lower for word in ["implemented", "deployed"]):
            action_verb = "Implemented"
        elif any(word in achievement_lower for word in ["optimized", "improved"]):
            action_verb = "Optimized"
        elif any(word in achievement_lower for word in ["analyzed", "researched"]):
            action_verb = "Analyzed"
        
        # Clean the description by removing any existing action verbs at the beginning
        cleaned_description = achievement.strip()
        
        # List of common action verbs to remove from the beginning
        action_verbs_to_remove = [
            "led", "lead", "managed", "developed", "built", "created", "implemented", 
            "deployed", "optimized", "improved", "analyzed", "researched", "enhanced",
            "streamlined", "automated", "designed", "coordinated", "evaluated",
            "architected", "engineered", "delivered", "scaled", "transformed",
            "revolutionized", "pioneered", "spearheaded", "orchestrated", "facilitated",
            "accelerated", "maximized", "minimized", "boosted", "elevated", "amplified",
            "catalyzed", "drove", "generated", "produced", "achieved", "accomplished",
            "executed", "launched", "established", "founded", "initiated", "started"
        ]
        
        # Remove action verbs from the beginning of the description
        words = cleaned_description.split()
        if words and words[0].lower() in action_verbs_to_remove:
            # Remove the first word if it's an action verb
            cleaned_description = " ".join(words[1:])
        
        # Create quantified result
        percentage = random.choice([15, 20, 25, 30, 35, 40, 45, 50])
        metric_category = random.choice(list(metrics.keys()))
        metric = random.choice(metrics[metric_category])
        
        quantified_result = quantified_results[0].format(percentage=percentage, metric=metric)
        
        # Create impact statement
        impact = f"Enhanced {metric} at {company} through {title} role"
        
        return ExperienceBullet(
            action_verb=action_verb,
            description=cleaned_description,
            quantified_result=quantified_result,
            keywords_used=relevant_keywords,
            impact=impact,
            company=company,
            title=title
        )
    
    def _generate_recommended_bullets(self, job_analysis: Dict[str, Any], 
                                    technical_skills: List[str], tools_technologies: List[str],
                                    quantified_results: List[str], metrics: Dict[str, List[str]]) -> List[ExperienceBullet]:
        """Generate recommended bullets based on job requirements"""
        
        bullets = []
        role_analysis = job_analysis.get('role_analysis', {})
        role_category = role_analysis.get('role_category', 'Unknown')
        
        # Helper function to clean description by removing action verbs
        def clean_description(description):
            action_verbs_to_remove = [
                "led", "lead", "managed", "developed", "built", "created", "implemented", 
                "deployed", "optimized", "improved", "analyzed", "researched", "enhanced",
                "streamlined", "automated", "designed", "coordinated", "evaluated",
                "architected", "engineered", "delivered", "scaled", "transformed",
                "revolutionized", "pioneered", "spearheaded", "orchestrated", "facilitated",
                "accelerated", "maximized", "minimized", "boosted", "elevated", "amplified",
                "catalyzed", "drove", "generated", "produced", "achieved", "accomplished",
                "executed", "launched", "established", "founded", "initiated", "started"
            ]
            
            words = description.split()
            if words and words[0].lower() in action_verbs_to_remove:
                return " ".join(words[1:])
            return description
        
        # Generate bullets for different role types
        if 'Machine Learning' in role_category or 'ML' in role_category:
            ml_bullets = [
                "Developed and deployed machine learning models using {tech}",
                "Optimized model performance achieving {percentage}% accuracy improvement",
                "Implemented automated ML pipelines reducing training time by {percentage}%",
                "Led cross-functional ML initiatives resulting in {percentage}% efficiency gain",
                "Architected scalable ML infrastructure supporting {number} concurrent users"
            ]
            
            for bullet_template in ml_bullets:
                tech = random.choice(technical_skills) if technical_skills else "Python"
                percentage = random.choice([20, 25, 30, 35, 40])
                number = random.choice([1000, 5000, 10000, 50000])
                
                description = bullet_template.format(tech=tech, percentage=percentage, number=number)
                cleaned_description = clean_description(description)
                quantified_result = f"resulting in a {percentage}% improvement in model performance"
                
                bullets.append(ExperienceBullet(
                    action_verb="Developed",
                    description=cleaned_description,
                    quantified_result=quantified_result,
                    keywords_used=[tech],
                    impact=f"Enhanced ML capabilities for {role_category} role",
                    company="Company",
                    title="Role"
                ))
        
        elif 'Data' in role_category:
            data_bullets = [
                "Analyzed large-scale datasets using {tech}",
                "Built data pipelines processing {number} records daily",
                "Created interactive dashboards improving data visibility by {percentage}%",
                "Optimized database queries reducing query time by {percentage}%",
                "Implemented data quality checks improving accuracy by {percentage}%"
            ]
            
            for bullet_template in data_bullets:
                tech = random.choice(technical_skills) if technical_skills else "SQL"
                percentage = random.choice([25, 30, 35, 40, 45])
                number = random.choice([100000, 500000, 1000000, 5000000])
                
                description = bullet_template.format(tech=tech, percentage=percentage, number=number)
                cleaned_description = clean_description(description)
                quantified_result = f"leading to a {percentage}% increase in data efficiency"
                
                bullets.append(ExperienceBullet(
                    action_verb="Analyzed",
                    description=cleaned_description,
                    quantified_result=quantified_result,
                    keywords_used=[tech],
                    impact=f"Enhanced data capabilities for {role_category} role",
                    company="Company",
                    title="Role"
                ))
        
        return bullets[:5]  # Limit to 5 recommended bullets
    
    def generate_project_descriptions(self, job_analysis: Dict[str, Any], user_projects: List[Dict[str, Any]] = None) -> List[ProjectDescription]:
        """
        Generate optimized project descriptions
        
        Args:
            job_analysis (Dict): Complete job analysis from Module 1
            user_projects (List): User's project data (optional)
            
        Returns:
            List[ProjectDescription]: Optimized project descriptions
        """
        
        job_keywords = job_analysis.get('keywords', {})
        technical_skills = job_keywords.get('technical_skills', [])
        tools_technologies = job_keywords.get('tools_technologies', [])
        role_analysis = job_analysis.get('role_analysis', {})
        role_category = role_analysis.get('role_category', 'Unknown')
        
        projects = []
        
        # Generate enhanced descriptions from user projects
        if user_projects:
            for project in user_projects:
                enhanced_project = self._enhance_user_project(
                    project, technical_skills, tools_technologies, role_category
                )
                if enhanced_project:
                    projects.append(enhanced_project)
        
        # Generate recommended projects based on job requirements and gaps
        recommended_projects = self._generate_recommended_projects(
            job_analysis, technical_skills, tools_technologies, role_category
        )
        projects.extend(recommended_projects)
        
        # Sort by relevance and limit to top 6-8 projects
        projects.sort(key=lambda x: len(x.technologies), reverse=True)
        return projects[:8]
    
    def _enhance_user_project(self, project: Dict[str, Any], technical_skills: List[str], 
                             tools_technologies: List[str], role_category: str) -> ProjectDescription:
        """Enhance user project with job-relevant details"""
        
        name = project.get('name', 'Project')
        current_desc = project.get('description', '')
        technologies = project.get('technologies', [])
        outcomes = project.get('outcomes', [])
        
        # Enhance technologies list with job-relevant skills
        enhanced_techs = list(set(technologies + [tech for tech in technical_skills + tools_technologies 
                                                if tech.lower() in current_desc.lower()]))
        
        # Generate enhanced outcomes if none provided
        if not outcomes:
            outcomes = [
                f"Improved {random.choice(['performance', 'efficiency', 'accuracy'])} by {random.choice([20, 25, 30, 35])}%",
                f"Reduced {random.choice(['processing time', 'costs', 'complexity'])} by {random.choice([15, 20, 25, 30])}%",
                f"Enhanced {random.choice(['user experience', 'system reliability', 'data quality'])}"
            ]
        
        # Create relevance explanation
        relevance = f"This project demonstrates expertise in {', '.join(enhanced_techs[:3])} relevant to {role_category} roles"
        
        return ProjectDescription(
            name=name,
            description=current_desc,
            technologies=enhanced_techs,
            outcomes=outcomes,
            relevance_explanation=relevance
        )
    
    def _generate_recommended_projects(self, job_analysis: Dict[str, Any], 
                                     technical_skills: List[str], tools_technologies: List[str],
                                     role_category: str) -> List[ProjectDescription]:
        """Generate recommended projects based on job requirements and gaps"""
        
        projects = []
        
        # ML/AI focused projects
        if 'Machine Learning' in role_category or 'ML' in role_category:
            ml_projects = [
                {
                    "name": "Advanced ML Model Deployment Pipeline",
                    "description": "Built an end-to-end machine learning pipeline using {tech1} and {tech2} for automated model training, validation, and deployment. Implemented CI/CD practices for ML models with automated testing and monitoring.",
                    "technologies": ["{tech1}", "{tech2}", "Docker", "Kubernetes", "MLflow"],
                    "outcomes": [
                        "Reduced model deployment time by 60%",
                        "Improved model accuracy by 25% through automated hyperparameter tuning",
                        "Enabled real-time model updates with zero downtime"
                    ]
                },
                {
                    "name": "Real-time Recommendation System",
                    "description": "Developed a scalable recommendation engine using {tech1} and {tech2} that processes user behavior data in real-time. Implemented A/B testing framework for continuous model optimization.",
                    "technologies": ["{tech1}", "{tech2}", "Redis", "Apache Kafka", "Elasticsearch"],
                    "outcomes": [
                        "Increased user engagement by 40%",
                        "Reduced recommendation latency by 70%",
                        "Scaled to handle 1M+ daily active users"
                    ]
                },
                {
                    "name": "Computer Vision Application",
                    "description": "Created a computer vision application using {tech1} for image classification and object detection. Implemented transfer learning techniques to achieve high accuracy with limited training data.",
                    "technologies": ["{tech1}", "OpenCV", "TensorFlow", "Flask", "AWS"],
                    "outcomes": [
                        "Achieved 95% accuracy in image classification",
                        "Reduced training time by 50% using transfer learning",
                        "Deployed as a REST API serving 10K+ requests daily"
                    ]
                }
            ]
            
            for project_template in ml_projects:
                tech1 = random.choice(technical_skills) if technical_skills else "PyTorch"
                tech2 = random.choice(tools_technologies) if tools_technologies else "AWS"
                
                project = ProjectDescription(
                    name=project_template["name"],
                    description=project_template["description"].format(tech1=tech1, tech2=tech2),
                    technologies=[tech1, tech2] + project_template["technologies"][2:],
                    outcomes=project_template["outcomes"],
                    relevance_explanation=f"Demonstrates advanced ML capabilities using {tech1} and {tech2} relevant to {role_category} positions"
                )
                projects.append(project)
        
        # Data focused projects
        elif 'Data' in role_category:
            data_projects = [
                {
                    "name": "Big Data Analytics Platform",
                    "description": "Built a comprehensive data analytics platform using {tech1} and {tech2} for processing large-scale datasets. Implemented data pipelines for ETL processes and real-time analytics.",
                    "technologies": ["{tech1}", "{tech2}", "Apache Spark", "Hadoop", "Airflow"],
                    "outcomes": [
                        "Processed 100TB+ of data daily",
                        "Reduced data processing time by 80%",
                        "Enabled real-time analytics for 50+ business metrics"
                    ]
                },
                {
                    "name": "Interactive Data Visualization Dashboard",
                    "description": "Created an interactive dashboard using {tech1} and {tech2} for visualizing complex business metrics. Implemented real-time data updates and user authentication.",
                    "technologies": ["{tech1}", "{tech2}", "React", "D3.js", "PostgreSQL"],
                    "outcomes": [
                        "Improved data accessibility for 500+ users",
                        "Reduced reporting time by 90%",
                        "Increased data-driven decision making by 60%"
                    ]
                },
                {
                    "name": "Predictive Analytics Model",
                    "description": "Developed a predictive analytics model using {tech1} for forecasting business trends. Implemented automated model retraining and performance monitoring.",
                    "technologies": ["{tech1}", "Scikit-learn", "Pandas", "NumPy", "Streamlit"],
                    "outcomes": [
                        "Achieved 85% prediction accuracy",
                        "Reduced forecasting errors by 30%",
                        "Automated 80% of manual forecasting processes"
                    ]
                }
            ]
            
            for project_template in data_projects:
                tech1 = random.choice(technical_skills) if technical_skills else "Python"
                tech2 = random.choice(tools_technologies) if tools_technologies else "Tableau"
                
                project = ProjectDescription(
                    name=project_template["name"],
                    description=project_template["description"].format(tech1=tech1, tech2=tech2),
                    technologies=[tech1, tech2] + project_template["technologies"][2:],
                    outcomes=project_template["outcomes"],
                    relevance_explanation=f"Demonstrates data analytics expertise using {tech1} and {tech2} relevant to {role_category} positions"
                )
                projects.append(project)
        
        # Software Engineering projects
        else:
            sw_projects = [
                {
                    "name": "Microservices Architecture Application",
                    "description": "Designed and implemented a scalable microservices application using {tech1} and {tech2}. Implemented containerization, load balancing, and automated deployment.",
                    "technologies": ["{tech1}", "{tech2}", "Docker", "Kubernetes", "Nginx"],
                    "outcomes": [
                        "Improved system scalability by 300%",
                        "Reduced deployment time by 75%",
                        "Achieved 99.9% uptime"
                    ]
                },
                {
                    "name": "API Gateway and Authentication System",
                    "description": "Built a secure API gateway with authentication and authorization using {tech1} and {tech2}. Implemented rate limiting, logging, and monitoring.",
                    "technologies": ["{tech1}", "{tech2}", "JWT", "Redis", "Prometheus"],
                    "outcomes": [
                        "Secured 100+ microservices",
                        "Reduced API response time by 40%",
                        "Implemented comprehensive security monitoring"
                    ]
                }
            ]
            
            for project_template in sw_projects:
                tech1 = random.choice(technical_skills) if technical_skills else "Python"
                tech2 = random.choice(tools_technologies) if tools_technologies else "AWS"
                
                project = ProjectDescription(
                    name=project_template["name"],
                    description=project_template["description"].format(tech1=tech1, tech2=tech2),
                    technologies=[tech1, tech2] + project_template["technologies"][2:],
                    outcomes=project_template["outcomes"],
                    relevance_explanation=f"Demonstrates software engineering expertise using {tech1} and {tech2} relevant to {role_category} positions"
                )
                projects.append(project)
        
        return projects
    
    def generate_complete_sections(self, job_analysis: Dict[str, Any], user_data: Dict[str, Any] = None) -> GeneratedSections:
        """
        Generate all resume sections at once
        
        Args:
            job_analysis (Dict): Complete job analysis from Module 1
            user_data (Dict): User's resume data (optional)
            
        Returns:
            GeneratedSections: Complete set of generated sections
        """
        
        if user_data is None:
            user_data = {}
        
        # Generate skills section
        user_skills = user_data.get("technical_skills", []) + user_data.get("soft_skills", [])
        skills_section = self.generate_skills_section(job_analysis, user_skills)
        
        # Generate experience bullets
        experience_bullets = self.generate_experience_bullets(job_analysis, user_data.get("work_experience"))
        
        # Generate project descriptions
        project_descriptions = self.generate_project_descriptions(job_analysis, user_data.get("projects"))
        
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
        """Generate a formatted skills summary"""
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
        """Generate a summary of experience bullets"""
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
        """Generate a summary of project descriptions"""
        if not projects:
            return "Projects: [To be generated based on job requirements]"
        
        # Get unique technologies used
        all_technologies = set()
        for project in projects:
            all_technologies.update(project.technologies)
        
        tech_list = list(all_technologies)[:6]  # Limit to 6 technologies
        
        return f"Project technologies: {', '.join(tech_list)}"
    
    def print_sections_summary(self, sections: GeneratedSections):
        """Print a formatted summary of generated sections"""
        print("\n" + "=" * 60)
        print("📄 GENERATED RESUME SECTIONS SUMMARY")
        print("=" * 60)
        
        # Skills Section
        print(f"\n🔧 SKILLS SECTION ({len(sections.skills_section)} skills):")
        print("-" * 40)
        for i, skill in enumerate(sections.skills_section[:10], 1):  # Show top 10
            print(f"{i:2d}. {skill.skill} ({skill.category}) - {skill.proficiency_level} (Relevance: {skill.relevance_score:.2f})")
        
        # Experience Section
        print(f"\n💼 EXPERIENCE SECTION ({len(sections.experience_bullets)} bullets):")
        print("-" * 40)
        for i, bullet in enumerate(sections.experience_bullets[:5], 1):  # Show top 5
            print(f"{i}. {bullet.action_verb} {bullet.description}")
            print(f"   Result: {bullet.quantified_result}")
            print(f"   Keywords: {', '.join(bullet.keywords_used[:3])}")
        
        # Projects Section
        print(f"\n🚀 PROJECTS SECTION ({len(sections.project_descriptions)} projects):")
        print("-" * 40)
        for i, project in enumerate(sections.project_descriptions, 1):
            print(f"{i}. {project.name}")
            print(f"   Technologies: {', '.join(project.technologies)}")
            print(f"   Description: {project.description[:100]}...")
        
        # Summaries
        print(f"\n📋 SECTION SUMMARIES:")
        print("-" * 40)
        print(f"Skills: {sections.skills_summary}")
        print(f"Experience: {sections.experience_summary}")
        print(f"Projects: {sections.projects_summary}")
    
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
    """Example usage of the ResumeSectionsGeneratorMVP"""
    
    # This would typically be loaded from Module 1 output
    sample_job_analysis = {
        "role_analysis": {
            "role_category": "Data Scientist",
            "seniority_level": "Senior",
            "industry_focus": "AI/ML"
        },
        "keywords": {
            "technical_skills": ["Python", "Machine Learning", "SQL", "TensorFlow"],
            "tools_technologies": ["AWS", "Docker", "Git", "Jupyter"],
            "soft_skills": ["Communication", "Problem Solving", "Leadership"]
        }
    }
    
    # Initialize generator
    generator = ResumeSectionsGeneratorMVP()
    
    # Generate complete sections
    sections = generator.generate_complete_sections(sample_job_analysis)
    
    # Print summary
    generator.print_sections_summary(sections)
    
    # Format for ATS
    ats_formatted = generator.format_for_ats(sections)
    
    print(f"\n📄 ATS-FORMATTED SECTIONS:")
    print("=" * 40)
    print("SKILLS:")
    print(ats_formatted["skills"])
    print("\nEXPERIENCE:")
    print(ats_formatted["experience"])
    print("\nPROJECTS:")
    print(ats_formatted["projects"])


if __name__ == "__main__":
    main() 