"""
Module 5: Final Resume Generator
Purpose: Generate a professional, standard-format resume by combining insights from all previous modules
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

@dataclass
class ResumeSection:
    """Data class for resume sections"""
    title: str
    content: List[str]
    order: int

@dataclass
class FinalResume:
    """Data class for the final resume"""
    job_name: str
    timestamp: str
    sections: List[ResumeSection]
    summary: str
    total_sections: int

class FinalResumeGenerator:
    """Generate final professional resume from all module outputs"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-haiku-20240307"
        
    def load_module_data(self, job_name: str, output_dir: Path) -> Dict[str, Any]:
        """
        Load data from all previous modules for a specific job
        
        Args:
            job_name (str): Name of the job
            output_dir (Path): Output directory path
            
        Returns:
            Dict: Combined data from all modules
        """
        job_dir = output_dir / "jobs" / job_name
        module_data = {}
        
        # Load Module 1 data (Job Analysis)
        module1_dir = job_dir / "module1"
        if module1_dir.exists():
            analysis_files = list(module1_dir.glob("analysis_*.json"))
            if analysis_files:
                latest_analysis = max(analysis_files, key=lambda x: x.stat().st_mtime)
                with open(latest_analysis, 'r', encoding='utf-8') as f:
                    module_data['module1'] = json.load(f)
        
        # Load Module 2 data (Keyword Matching)
        module2_dir = job_dir / "module2"
        if module2_dir.exists():
            keyword_files = list(module2_dir.glob("keyword_matching_*.json"))
            if keyword_files:
                latest_keywords = max(keyword_files, key=lambda x: x.stat().st_mtime)
                with open(latest_keywords, 'r', encoding='utf-8') as f:
                    module_data['module2'] = json.load(f)
        
        # Load Module 3 data (Resume Sections)
        module3_dir = job_dir / "module3"
        if module3_dir.exists():
            section_files = list(module3_dir.glob("resume_sections_*.json"))
            if section_files:
                latest_sections = max(section_files, key=lambda x: x.stat().st_mtime)
                with open(latest_sections, 'r', encoding='utf-8') as f:
                    module_data['module3'] = json.load(f)
        
        return module_data
    
    def generate_header_section(self, job_analysis: Dict[str, Any], cv_data: Dict[str, Any]) -> ResumeSection:
        """Generate professional header section"""
        role_info = job_analysis.get('role_analysis', {})
        role_category = role_info.get('role_category', 'Professional')
        
        # Extract basic CV info
        name = "Your Name"  # This would come from CV parsing
        email = "your.email@example.com"
        phone = "+1 (555) 123-4567"
        location = "City, State"
        linkedin = "linkedin.com/in/yourprofile"
        
        header_content = [
            f"{name.upper()}",
            f"{email} | {phone} | {location}",
            f"LinkedIn: {linkedin}",
            "",
            f"TARGET ROLE: {role_category}",
            ""
        ]
        
        return ResumeSection(
            title="HEADER",
            content=header_content,
            order=1
        )
    
    def generate_summary_section(self, job_analysis: Dict[str, Any], gap_analysis: Dict[str, Any], cv_data: Dict[str, Any]) -> ResumeSection:
        """Generate comprehensive professional summary tailored to job requirements"""
        
        # Extract key information
        role_info = job_analysis.get('role_analysis', {})
        keywords = job_analysis.get('keywords', {})
        requirements = keywords.get('requirements', [])
        responsibilities = keywords.get('responsibilities', [])
        
        # Get CV information
        education = cv_data.get('education', [])
        work_experience = cv_data.get('work_experience', [])
        projects = cv_data.get('projects', [])
        
        # Calculate experience years
        experience_years = self._calculate_experience_years(work_experience)
        
        # Check for research/PhD requirements
        is_research_role = self._is_research_role(role_info, requirements, responsibilities)
        has_phd = self._has_phd_requirement(requirements)
        has_publications = self._has_publications(cv_data)
        
        # Extract comprehensive domain expertise using API
        domain_analysis = self._extract_domain_expertise(job_analysis, cv_data)
        
        # Get top skills for summary
        technical_skills = keywords.get('technical_skills', [])
        tools = keywords.get('tools_technologies', [])
        
        prompt = f"""
        Create a compelling professional summary for a resume that matches this job description.
        
        JOB INFORMATION:
        - Role: {role_info.get('role_category', 'Professional')}
        - Seniority: {role_info.get('seniority_level', 'Mid-level')}
        - Industry: {role_info.get('industry_focus', 'Technology')}
        - Experience Required: {role_info.get('experience_years', '3-5 years')}
        
        JOB REQUIREMENTS: {requirements}
        JOB RESPONSIBILITIES: {responsibilities}
        
        CANDIDATE INFORMATION:
        - Experience Years: {experience_years} years
        - Education: {[edu.get('degree', '') for edu in education]}
        - Top Technical Skills: {technical_skills[:5]}
        - Key Tools: {tools[:3]}
        - Is Research Role: {is_research_role}
        - PhD Required: {has_phd}
        - Has Publications: {has_publications}
        
        DOMAIN ANALYSIS:
        - Job Domains: {domain_analysis.get('job_domains', [])}
        - Candidate Domains: {domain_analysis.get('candidate_domains', [])}
        - Matching Domains: {domain_analysis.get('matching_domains', [])}
        - Key Projects: {domain_analysis.get('relevant_projects', [])}
        - Domain-Specific Skills: {domain_analysis.get('domain_skills', [])}
        
        Create a professional summary that:
        1. Opens with role and experience level
        2. HIGHLIGHTS ALL RELEVANT DOMAIN EXPERTISE that matches the job requirements
        3. Mentions specific qualifications if required (PhD, research experience, publications)
        4. Shows passion and interest in the specific domains/fields relevant to this job
        5. Connects candidate's background to job requirements
        6. Uses professional, confident tone
        7. Is 3-4 sentences maximum
        
        IMPORTANT: Focus on the domains and skills that are MOST RELEVANT to this specific job. Don't limit to just one domain - highlight ALL relevant expertise areas.
        
        Return ONLY the summary text, no additional formatting.
        """
        
        try:
            response = self.client.completion(
                model=self.model,
                prompt=prompt,
                max_tokens_to_sample=200
            )
            
            summary_text = response.completion.strip()
            
            # Clean up any markdown or extra formatting
            if summary_text.startswith('"') and summary_text.endswith('"'):
                summary_text = summary_text[1:-1]
            
            return ResumeSection(
                title="PROFESSIONAL SUMMARY",
                content=[summary_text],
                order=2
            )
            
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            # Fallback to basic summary
            fallback_summary = f"Results-driven {role_info.get('role_category', 'professional').lower()} with {experience_years} years of experience in {', '.join(technical_skills[:3])}."
            return ResumeSection(
                title="PROFESSIONAL SUMMARY",
                content=[fallback_summary],
                order=2
            )
    
    def _calculate_experience_years(self, work_experience: List[Dict[str, Any]]) -> int:
        """Calculate total years of experience from work history"""
        if not work_experience:
            return 0
        
        total_years = 0
        for exp in work_experience:
            dates = exp.get('dates', '')
            # Simple parsing - could be enhanced
            if 'years' in dates.lower():
                # Extract number of years
                import re
                years_match = re.search(r'(\d+)', dates)
                if years_match:
                    total_years += int(years_match.group(1))
            else:
                # Default to 1 year if can't parse
                total_years += 1
        
        return max(total_years, 1)  # Minimum 1 year
    
    def _is_research_role(self, role_info: Dict[str, Any], requirements: List[str], responsibilities: List[str]) -> bool:
        """Determine if this is a research-focused role"""
        research_keywords = ['research', 'phd', 'publication', 'academic', 'scientist', 'investigation', 'study']
        
        # Check role category
        role_category = role_info.get('role_category', '').lower()
        if any(keyword in role_category for keyword in research_keywords):
            return True
        
        # Check requirements
        requirements_text = ' '.join(requirements).lower()
        if any(keyword in requirements_text for keyword in research_keywords):
            return True
        
        # Check responsibilities
        responsibilities_text = ' '.join(responsibilities).lower()
        if any(keyword in responsibilities_text for keyword in research_keywords):
            return True
        
        return False
    
    def _has_phd_requirement(self, requirements: List[str]) -> bool:
        """Check if PhD is required"""
        requirements_text = ' '.join(requirements).lower()
        phd_keywords = ['phd', 'doctorate', 'doctoral', 'ph.d']
        return any(keyword in requirements_text for keyword in phd_keywords)
    
    def _has_publications(self, cv_data: Dict[str, Any]) -> bool:
        """Check if candidate has publications mentioned"""
        # This would need to be enhanced based on actual CV structure
        # For now, check if there are any research-related keywords in projects
        projects = cv_data.get('projects', [])
        for project in projects:
            description = project.get('description', '').lower()
            if any(keyword in description for keyword in ['publication', 'paper', 'journal', 'conference']):
                return True
        return False
    
    def _extract_domain_expertise(self, job_analysis: Dict[str, Any], cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract ALL relevant domains and keywords using API-powered analysis"""
        
        # Prepare data for API analysis
        job_text = self._prepare_job_text(job_analysis)
        cv_text = self._prepare_cv_text(cv_data)
        
        prompt = f"""
        Analyze this job description and CV to identify ALL relevant domains, keywords, and expertise areas.
        
        JOB DESCRIPTION:
        {job_text}
        
        CANDIDATE CV:
        {cv_text}
        
        Extract and categorize the following:
        
        1. TECHNICAL DOMAINS (e.g., Machine Learning, Data Science, Software Engineering, etc.)
        2. INDUSTRY DOMAINS (e.g., Biology, Finance, Healthcare, E-commerce, etc.)
        3. APPLICATION AREAS (e.g., Drug Discovery, Fraud Detection, Customer Analytics, etc.)
        4. METHODOLOGIES (e.g., Research, Development, Analysis, etc.)
        5. SPECIFIC TECHNOLOGIES/SKILLS mentioned in both job and CV
        
        For each domain/keyword, provide:
        - Relevance score (0-1) based on how important it is for the job
        - Whether it appears in both job and CV (matching)
        - Specific examples from the data
        
        Return as JSON:
        {{
            "job_domains": [{{"domain": "string", "relevance": float, "examples": ["string"]}}],
            "candidate_domains": [{{"domain": "string", "relevance": float, "examples": ["string"]}}],
            "matching_domains": [{{"domain": "string", "relevance": float, "job_examples": ["string"], "cv_examples": ["string"]}}],
            "relevant_projects": ["project_name"],
            "domain_skills": ["skill1", "skill2"]
        }}
        
        Focus on identifying ALL relevant areas, not just one domain. Be comprehensive.
        """
        
        try:
            response = self.client.completion(
                model=self.model,
                prompt=prompt,
                max_tokens_to_sample=1000
            )
            
            content = response.completion.strip()
            
            # Clean up the response
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Try to parse JSON with better error handling
            try:
                parsed_data = json.loads(content)
            except json.JSONDecodeError as json_error:
                print(f"❌ JSON parsing error: {json_error}")
                print(f"Raw content: {content[:200]}...")
                # Fallback to basic extraction
                return self._fallback_domain_extraction(job_analysis, cv_data)
            
            # Extract simplified lists for summary generation
            job_domains = [item.get('domain', '') for item in parsed_data.get('job_domains', [])]
            candidate_domains = [item.get('domain', '') for item in parsed_data.get('candidate_domains', [])]
            matching_domains = [item.get('domain', '') for item in parsed_data.get('matching_domains', [])]
            relevant_projects = parsed_data.get('relevant_projects', [])
            domain_skills = parsed_data.get('domain_skills', [])
            
            return {
                'job_domains': job_domains,
                'candidate_domains': candidate_domains,
                'matching_domains': matching_domains,
                'relevant_projects': relevant_projects,
                'domain_skills': domain_skills,
                'detailed_analysis': parsed_data
            }
            
        except Exception as e:
            print(f"❌ Error in domain extraction: {e}")
            # Fallback to basic extraction
            return self._fallback_domain_extraction(job_analysis, cv_data)
    
    def _prepare_job_text(self, job_analysis: Dict[str, Any]) -> str:
        """Prepare job analysis data as text for API processing"""
        role_info = job_analysis.get('role_analysis', {})
        keywords = job_analysis.get('keywords', {})
        
        job_text = f"""
        Role: {role_info.get('role_category', '')}
        Seniority: {role_info.get('seniority_level', '')}
        Industry: {role_info.get('industry_focus', '')}
        Experience: {role_info.get('experience_years', '')}
        
        Technical Skills: {keywords.get('technical_skills', [])}
        Tools & Technologies: {keywords.get('tools_technologies', [])}
        Soft Skills: {keywords.get('soft_skills', [])}
        Requirements: {keywords.get('requirements', [])}
        Responsibilities: {keywords.get('responsibilities', [])}
        """
        
        return job_text
    
    def _prepare_cv_text(self, cv_data: Dict[str, Any]) -> str:
        """Prepare CV data as text for API processing"""
        
        cv_text = f"""
        Education: {[edu.get('degree', '') for edu in cv_data.get('education', [])]}
        
        Work Experience:
        {[f"{exp.get('title', '')} at {exp.get('company', '')}: {exp.get('achievements', [])}" for exp in cv_data.get('work_experience', [])]}
        
        Projects:
        {[f"{proj.get('name', '')}: {proj.get('description', '')} - Technologies: {proj.get('technologies', [])}" for proj in cv_data.get('projects', [])]}
        
        Technical Skills: {cv_data.get('technical_skills', [])}
        Extracted Keywords: {cv_data.get('extracted_keywords', [])}
        """
        
        return cv_text
    
    def _fallback_domain_extraction(self, job_analysis: Dict[str, Any], cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback domain extraction if API fails"""
        
        # Basic keyword extraction
        job_keywords = job_analysis.get('keywords', {})
        job_requirements = job_keywords.get('requirements', [])
        job_responsibilities = job_keywords.get('responsibilities', [])
        
        # Extract from CV
        projects = cv_data.get('projects', [])
        work_experience = cv_data.get('work_experience', [])
        
        # Simple domain identification
        domains = set()
        for req in job_requirements + job_responsibilities:
            domains.update(req.lower().split())
        
        candidate_domains = set()
        for project in projects:
            candidate_domains.update(project.get('name', '').lower().split())
            candidate_domains.update(project.get('description', '').lower().split())
        
        return {
            'job_domains': list(domains)[:10],
            'candidate_domains': list(candidate_domains)[:10],
            'matching_domains': list(domains.intersection(candidate_domains))[:5],
            'relevant_projects': [proj.get('name', '') for proj in projects[:3]],
            'domain_skills': list(domains)[:5]
        }
    
    def generate_skills_section(self, module3_data: Dict[str, Any], job_analysis: Dict[str, Any]) -> ResumeSection:
        """Generate skills section with job-relevant skills including project technologies"""
        skills_data = module3_data.get('skills', [])
        projects_data = module3_data.get('projects', [])
        
        # Collect skills from both skills data and project technologies
        all_skills = {}
        
        # Add skills from skills data
        for skill in skills_data:
            category = skill.get('category', 'Other')
            skill_name = skill.get('name', '')
            if skill_name and category not in all_skills:
                all_skills[category] = []
            if skill_name and skill_name not in all_skills.get(category, []):
                all_skills[category].append(skill_name)
        
        # Add technologies from projects
        project_technologies = set()
        for project in projects_data:
            technologies = project.get('technologies', [])
            for tech in technologies:
                # Filter out non-skills
                if self._is_valid_skill(tech):
                    project_technologies.add(tech)
        
        # Categorize project technologies
        for tech in project_technologies:
            category = self._categorize_technology(tech)
            if category not in all_skills:
                all_skills[category] = []
            if tech not in all_skills[category]:
                all_skills[category].append(tech)
        
        # Remove duplicates across categories and clean up
        all_skills = self._deduplicate_and_clean_skills(all_skills)
        
        # Format skills content
        skills_content = []
        for category, skills in all_skills.items():
            if skills:
                category_title = category.replace('_', ' ').title()
                skills_content.append(f"{category_title}: {', '.join(skills)}")
        
        return ResumeSection(
            title="TECHNICAL SKILLS",
            content=skills_content,
            order=3
        )
    
    def _is_valid_skill(self, skill: str) -> bool:
        """Check if a skill is valid (not a dataset, generic term, etc.)"""
        skill_lower = skill.lower()
        
        # Filter out non-skills
        invalid_terms = [
            'datasets', 'dataset', 'data', 'genomics datasets', 'genomics dataset',
            'probability', 'statistics', 'mathematics', 'linear algebra', 'optimization',
            'machine learning', 'deep learning', 'artificial intelligence', 'ai', 'ml',
            'computational biology', 'bioinformatics', 'apache kafka', 'kubernetes', 'redis', 'elasticsearch'
        ]
        
        return not any(term in skill_lower for term in invalid_terms)
    
    def _deduplicate_and_clean_skills(self, all_skills: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Remove duplicates across categories and clean up skills"""
        # Track all skills to avoid duplicates
        seen_skills = set()
        cleaned_skills = {}
        
        # Priority order for categories (skills will be kept in the first category they appear)
        category_priority = [
            "Programming Languages",
            "Frameworks", 
            "AI/ML Technologies",
            "Cloud & Infrastructure",
            "Databases & Storage",
            "Tools",
            "Other Technologies"
        ]
        
        # Process skills in priority order
        for category in category_priority:
            if category in all_skills:
                cleaned_skills[category] = []
                for skill in all_skills[category]:
                    skill_lower = skill.lower()
                    if skill_lower not in seen_skills and self._is_valid_skill(skill):
                        cleaned_skills[category].append(skill)
                        seen_skills.add(skill_lower)
        
        # Add any remaining categories
        for category, skills in all_skills.items():
            if category not in cleaned_skills:
                cleaned_skills[category] = []
                for skill in skills:
                    skill_lower = skill.lower()
                    if skill_lower not in seen_skills and self._is_valid_skill(skill):
                        cleaned_skills[category].append(skill)
                        seen_skills.add(skill_lower)
        
        # Remove empty categories
        return {k: v for k, v in cleaned_skills.items() if v}
    
    def _categorize_technology(self, tech: str) -> str:
        """Categorize technology into appropriate skill category"""
        tech_lower = tech.lower().strip()
        
        # AI/ML Specific (check this first to avoid misclassification)
        if any(ai in tech_lower for ai in ['mistral', 'gpt', 'bert', 'roberta', 'llama', 'rag', 'fine-tuning', 'prompt engineering', 'lora', 'peft', 'ctransformers', 'transformers']):
            return "AI/ML Technologies"
        
        # Frameworks & Libraries
        frameworks = ['pytorch', 'tensorflow', 'scikit', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'keras', 'jax', 'langchain', 'streamlit', 'fastapi', 'django', 'flask', 'react', 'angular', 'vue']
        if any(framework == tech_lower for framework in frameworks):
            return "Frameworks"
        
        # Cloud & Infrastructure
        cloud_infra = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'gitlab', 'github']
        if any(cloud == tech_lower for cloud in cloud_infra):
            return "Cloud & Infrastructure"
        
        # Databases & Storage
        dbs = ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'snowflake', 'databricks', 'faiss', 'hadoop', 'spark']
        if any(db == tech_lower for db in dbs):
            return "Databases & Storage"
        
        # Tools & Platforms
        tools = ['git', 'jupyter', 'vscode', 'pycharm', 'tableau', 'powerbi', 'excel', 'word', 'powerpoint', 'ssrs']
        if any(tool == tech_lower for tool in tools):
            return "Tools"
        
        # Programming Languages (exact match only)
        languages = ['python', 'r', 'java', 'javascript', 'c++', 'c#', 'sql', 'scala', 'go', 'rust']
        if tech_lower in languages:
            return "Programming Languages"
        
        # Default category
        return "Other Technologies"
    
    def generate_experience_section(self, module3_data: Dict[str, Any], cv_data: Dict[str, Any]) -> ResumeSection:
        """Generate experience section with optimized bullets including project-based experience"""
        experience_data = module3_data.get('experience', [])
        projects_data = module3_data.get('projects', [])
        
        experience_content = []
        current_company = ""
        current_title = ""
        
        # Add traditional work experience
        for exp in experience_data:
            # Add company/title header if it changes
            if exp.get('company') and exp.get('company') != current_company:
                current_company = exp.get('company', '')
                current_title = exp.get('title', '')
                experience_content.append(f"\n{current_title} | {current_company}")
                experience_content.append("-" * (len(current_title) + len(current_company) + 3))
            
            # Add bullet point - combine bullet and result into single sentence
            bullet = exp.get('bullet', '')
            result = exp.get('result', '')
            if bullet:
                if result:
                    # Combine bullet and result into one sentence
                    combined_bullet = f"• {bullet} {result}"
                    experience_content.append(combined_bullet)
                else:
                    experience_content.append(f"• {bullet}")
        
        # Add project-based experience bullets
        if projects_data:
            experience_content.append(f"\nProject-Based Experience")
            experience_content.append("-" * 25)

            for project in projects_data[:5]:  # Limit to top 5 projects
                name = project.get('name', '')
                description = project.get('description', '')
                outcomes = project.get('outcomes', [])
                technologies = project.get('technologies', [])

                if name and description:
                    # Create project-based experience bullet
                    tech_list = ', '.join(technologies[:3])  # Limit to 3 technologies
                    outcome_text = ''
                    if outcomes:
                        outcome_text = f", resulting in {', '.join(outcomes).lower()}"  # Include all outcomes in lowercase

                    # Ensure proper sentence structure
                    project_bullet = f"• {description}{outcome_text}."
                    project_bullet = project_bullet.replace('using ', '').replace('using', '')  # Remove redundant 'using'
                    project_bullet = project_bullet.replace('.,', ',')  # Remove '.,' occurrence
                    project_bullet = project_bullet[0].upper() + project_bullet[1:]  # Capitalize first letter

                    experience_content.append(project_bullet)
        
        return ResumeSection(
            title="PROFESSIONAL EXPERIENCE",
            content=experience_content,
            order=4
        )
    
    def generate_education_section(self, cv_data: Dict[str, Any]) -> ResumeSection:
        """Generate education section"""
        education_data = cv_data.get('education', [])
        
        education_content = []
        for edu in education_data:
            degree = edu.get('degree', '')
            institution = edu.get('institution', '')
            year = edu.get('year', '')
            
            if degree and institution:
                education_content.append(f"{degree} | {institution} | {year}")
        
        if not education_content:
            education_content = ["Bachelor's Degree | University Name | 20XX"]
        
        return ResumeSection(
            title="EDUCATION",
            content=education_content,
            order=5
        )
    
    def generate_certifications_section(self, cv_data: Dict[str, Any], job_analysis: Dict[str, Any], gap_analysis: Dict[str, Any]) -> ResumeSection:
        """Generate certifications section with suggested certificates based on skill gaps"""
        certifications = cv_data.get('certifications', [])
        
        # Get missing skills from gap analysis
        missing_keywords = gap_analysis.get('missing_keywords', [])
        missing_skills = [item.get('keyword', '') for item in missing_keywords if item.get('keyword')]
        
        # Define certificate suggestions based on common missing skills
        certificate_suggestions = {
            'aws': ['AWS Certified Solutions Architect', 'AWS Certified Developer', 'AWS Certified Data Analytics'],
            'azure': ['Microsoft Azure Fundamentals', 'Azure Data Scientist Associate', 'Azure Developer Associate'],
            'gcp': ['Google Cloud Professional Data Engineer', 'Google Cloud Professional Cloud Architect'],
            'docker': ['Docker Certified Associate', 'Docker Certified Developer'],
            'kubernetes': ['Certified Kubernetes Administrator (CKA)', 'Certified Kubernetes Application Developer (CKAD)'],
            'python': ['Python Institute PCAP', 'Google IT Automation with Python'],
            'machine learning': ['Google TensorFlow Developer Certificate', 'IBM Machine Learning Professional Certificate'],
            'data science': ['IBM Data Science Professional Certificate', 'Google Data Analytics Professional Certificate'],
            'sql': ['Microsoft SQL Server Certification', 'Oracle Database SQL Certified Associate'],
            'tableau': ['Tableau Desktop Specialist', 'Tableau Desktop Certified Associate'],
            'power bi': ['Microsoft Power BI Data Analyst', 'Microsoft Power Platform Fundamentals'],
            'spark': ['Databricks Certified Associate Developer', 'Databricks Certified Data Engineer Associate'],
            'snowflake': ['Snowflake SnowPro Core Certification', 'Snowflake SnowPro Advanced Data Engineer'],
            'databricks': ['Databricks Certified Associate Developer', 'Databricks Certified Data Engineer Associate'],
            'terraform': ['HashiCorp Certified: Terraform Associate', 'HashiCorp Certified: Terraform Professional'],
            'jenkins': ['Jenkins Certified Engineer', 'DevOps Foundation'],
            'git': ['GitHub Certified Developer', 'GitLab Certified Associate'],
            'agile': ['Certified ScrumMaster (CSM)', 'Professional Scrum Master (PSM)', 'PMI Agile Certified Practitioner'],
            'project management': ['PMP (Project Management Professional)', 'PRINCE2 Foundation', 'PRINCE2 Practitioner']
        }
        
        cert_content = []
        
        # Add existing certifications
        if certifications:
            for cert in certifications:
                cert_content.append(f"• {cert}")
        
        # Add suggested certificates based on missing skills
        suggested_certs = set()
        for skill in missing_skills:
            skill_lower = skill.lower()
            for key, certs in certificate_suggestions.items():
                if key in skill_lower or skill_lower in key:
                    suggested_certs.update(certs[:2])  # Add up to 2 relevant certificates per skill
        
        if suggested_certs:
            cert_content.append("\nSuggested Certifications (based on skill gaps):")
            for cert in sorted(list(suggested_certs))[:5]:  # Limit to 5 suggestions
                cert_content.append(f"• {cert}")
        
        if not cert_content:
            cert_content = ["• Relevant certifications will be added here"]
        
        return ResumeSection(
            title="CERTIFICATIONS",
            content=cert_content,
            order=6
        )
    
    def generate_final_resume(self, job_name: str, output_dir: Path) -> FinalResume:
        """
        Generate final professional resume
        
        Args:
            job_name (str): Name of the job
            output_dir (Path): Output directory path
            
        Returns:
            FinalResume: Complete resume object
        """
        # Load data from all modules
        module_data = self.load_module_data(job_name, output_dir)
        
        if not module_data:
            raise ValueError(f"No module data found for job: {job_name}")
        
        # Extract data from modules
        job_analysis = module_data.get('module1', {})
        keyword_data = module_data.get('module2', {})
        sections_data = module_data.get('module3', {})
        cv_data = keyword_data.get('cv_data', {})
        gap_analysis = keyword_data.get('gap_analysis', {})
        
        # Generate all sections
        sections = []
        
        # Header
        sections.append(self.generate_header_section(job_analysis, cv_data))
        
        # Summary
        sections.append(self.generate_summary_section(job_analysis, gap_analysis, cv_data))
        
        # Skills
        if sections_data:
            sections.append(self.generate_skills_section(sections_data, job_analysis))
        
        # Experience
        if sections_data:
            sections.append(self.generate_experience_section(sections_data, cv_data))
        
        # Education
        sections.append(self.generate_education_section(cv_data))
        
        # Certifications
        sections.append(self.generate_certifications_section(cv_data, job_analysis, gap_analysis))
        
        # Sort sections by order
        sections.sort(key=lambda x: x.order)
        
        # Generate summary
        role_info = job_analysis.get('role_analysis', {})
        summary = f"Professional resume for {role_info.get('role_category', 'target role')} position with {len(sections)} sections"
        
        return FinalResume(
            job_name=job_name,
            timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            sections=sections,
            summary=summary,
            total_sections=len(sections)
        )
    
    def save_resume(self, resume: FinalResume, output_dir: Path) -> None:
        """
        Save resume in multiple formats
        
        Args:
            resume (FinalResume): Resume object to save
            output_dir (Path): Output directory path
        """
        job_dir = output_dir / "jobs" / resume.job_name
        module5_dir = job_dir / "module5"
        module5_dir.mkdir(exist_ok=True)
        
        # Save as text file
        txt_file = module5_dir / f"final_resume_{resume.timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("PROFESSIONAL RESUME\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated for: {resume.job_name}\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for section in resume.sections:
                f.write(f"{section.title}\n")
                f.write("-" * len(section.title) + "\n")
                for line in section.content:
                    f.write(f"{line}\n")
                f.write("\n")
        
        # Save as JSON
        json_file = module5_dir / f"final_resume_{resume.timestamp}.json"
        resume_dict = {
            "job_name": resume.job_name,
            "timestamp": resume.timestamp,
            "summary": resume.summary,
            "total_sections": resume.total_sections,
            "sections": [
                {
                    "title": section.title,
                    "content": section.content,
                    "order": section.order
                }
                for section in resume.sections
            ]
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(resume_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Final resume saved to:")
        print(f"   Text: {txt_file}")
        print(f"   JSON: {json_file}") 