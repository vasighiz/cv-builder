"""
Personal RAG Enhancer Module
Purpose: Enhance resume generation using personal knowledge base and similar job examples
"""

import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

@dataclass
class PersonalData:
    """Personal data structure"""
    name: str
    email: str
    phone: str
    location: str
    linkedin: str
    experience_years: int
    education: List[Dict[str, Any]]
    work_experience: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    skills: Dict[str, List[str]]
    achievements: List[str]
    publications: List[str]
    certifications: List[str]

@dataclass
class SimilarJob:
    """Similar job structure"""
    job_title: str
    company: str
    description: str
    requirements: List[str]
    skills: List[str]
    similarity_score: float

@dataclass
class SuccessfulResume:
    """Successful resume example structure"""
    job_title: str
    company: str
    resume_sections: Dict[str, Any]
    success_factors: List[str]
    relevance_score: float

class PersonalRAGEnhancer:
    """
    Enhanced RAG system for personalized resume generation
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the RAG enhancer
        
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
        
        # Load knowledge bases
        self.similar_jobs_db = self._load_similar_jobs_database()
        self.successful_resumes_db = self._load_successful_resumes_database()
        
        # Initialize vectorizer for similarity search
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Vectorize knowledge bases
        self._vectorize_knowledge_bases()
    
    def _load_personal_data(self) -> PersonalData:
        """
        Load your personal data from CV and other sources
        """
        # This would be loaded from your actual CV data
        # For now, using the data from your manual resume
        return PersonalData(
            name="Your Name",
            email="your.email@example.com",
            phone="+1 (555) 123-4567",
            location="City, State",
            linkedin="linkedin.com/in/yourprofile",
            experience_years=6,
            education=[
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
            work_experience=[
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
                },
                {
                    "company": "University of Windsor",
                    "title": "Research Assistant",
                    "location": "ON, Canada",
                    "dates": "01/2020-04/2024",
                    "achievements": [
                        "Developed and deployed ML models for NGS (scRNA seq) data using PyTorch resulting in 15% improvement in link prediction accuracy",
                        "Delivered presentations and workshops on ML, Data Analysis, Generative AI, and LLMs to 100+ Master students",
                        "Provided mentorship on advanced AI research topics"
                    ]
                }
            ],
            projects=[
                {
                    "name": "Scientific Knowledge Chatbot",
                    "description": "Fine-tuned GPT-2 transformers using LoRA and PEFT for genomics datasets",
                    "technologies": ["GPT-2", "LoRA", "PEFT", "NGS", "Fine-tuning"],
                    "outcomes": ["Specialized conversational assistant", "Automated NGS data analysis", "Natural language querying"]
                },
                {
                    "name": "LLM-Based Question Answering System (RAG-Powered)",
                    "description": "Developed RAG pipeline using Python",
                    "technologies": ["LangChain", "Hugging Face", "FAISS", "Mistral 7B", "Streamlit"],
                    "outcomes": ["Document processing", "Semantic search", "Local LLM inference"]
                },
                {
                    "name": "Machine Learning Model Deployment Pipeline",
                    "description": "Built end-to-end ML pipeline using TensorFlow and AWS",
                    "technologies": ["TensorFlow", "AWS", "CI/CD", "Automated testing"],
                    "outcomes": ["Automated model training", "Validation", "Deployment"]
                },
                {
                    "name": "Identification of SARS-CoV-2 Cell Types on Single-Cell RNA-Seq Data",
                    "description": "Applied advanced unsupervised learning methods for COVID-19 research",
                    "technologies": ["Unsupervised Learning", "MLLE", "ICA", "Clustering", "scRNA-seq"],
                    "outcomes": ["Identified lung cell clusters", "Validated immune-related targets", "Research publication"]
                },
                {
                    "name": "Subgraph Embedding of Gene Expression Matrix for Cell-Cell Communication Prediction",
                    "description": "Developed SEGCECO, a novel attributed graph convolutional neural network method",
                    "technologies": ["Graph Neural Networks", "GCN", "Link Prediction", "scRNA-seq"],
                    "outcomes": ["0.99 ROC", "99% accuracy", "Superior performance over state-of-the-art"]
                }
            ],
            skills={
                "frameworks": ["PyTorch", "TensorFlow", "MLOps", "RAG", "Fine-tuning LLMs", "Model Optimization", "Prompt engineering"],
                "tools": ["Hugging Face Transformers", "LangChain", "Streamlit", "FastAPI", "AWS", "Git", "Docker", "HPC/GPU Clusters", "Linux", "Shell Scripting"],
                "programming": ["Python", "R"],
                "other": ["Communication", "Problem-solving", "JAX"]
            },
            achievements=[
                "Ph.D. in Computer Science with 96/100 GPA",
                "Published research on SARS-CoV-2 and SCLC",
                "Delivered workshops to 100+ Master students",
                "Developed systems with 99% accuracy",
                "Achieved 80% improvement in processing time"
            ],
            publications=[
                "SARS-CoV-2 Cell Types Identification Research",
                "SEGCECO: Subgraph Embedding for Cell-Cell Communication",
                "SCLC Therapeutic Targets Research"
            ],
            certifications=[]
        )
    
    def _load_similar_jobs_database(self) -> List[Dict[str, Any]]:
        """
        Load database of similar job descriptions
        """
        # This would be loaded from a real database
        # For now, creating sample similar jobs based on your field
        return [
            {
                "job_title": "Machine Learning Scientist",
                "company": "Deep Genomics",
                "description": "Develop and implement advanced machine learning models for drug discovery and computational biology",
                "requirements": ["PhD in ML/CS", "Experience in bioinformatics", "PyTorch/TensorFlow", "Research experience"],
                "skills": ["machine learning", "computational biology", "bioinformatics", "PyTorch", "TensorFlow", "research"]
            },
            {
                "job_title": "Senior ML Engineer",
                "company": "Rocket",
                "description": "Build and deploy machine learning models for data analysis and insights",
                "requirements": ["5+ years ML experience", "Python", "AWS", "Model deployment", "Team leadership"],
                "skills": ["machine learning", "Python", "AWS", "model deployment", "leadership", "data analysis"]
            },
            {
                "job_title": "Research Scientist - AI/ML",
                "company": "Elham Dolatabadi",
                "description": "Conduct research in machine learning and artificial intelligence applications",
                "requirements": ["PhD in relevant field", "Publication record", "Research experience", "ML frameworks"],
                "skills": ["research", "machine learning", "publications", "PyTorch", "TensorFlow", "academic"]
            }
        ]
    
    def _load_successful_resumes_database(self) -> List[Dict[str, Any]]:
        """
        Load database of successful resume examples
        """
        # This would be loaded from real successful resumes
        # For now, creating sample successful resume patterns
        return [
            {
                "job_title": "Machine Learning Scientist",
                "company": "Biotech Company",
                "resume_sections": {
                    "summary": "Results-driven ML scientist with PhD and 6+ years experience in bioinformatics and NGS data analysis",
                    "skills": "Frameworks: PyTorch, TensorFlow, MLOps | Tools: AWS, Docker, HPC | Programming: Python, R",
                    "experience": [
                        "Developed multi-agent architectures for NGS data analysis resulting in 80% improvement",
                        "Launched RAG-based system with 15% improvement in processing time"
                    ]
                },
                "success_factors": ["Specific metrics", "Domain expertise", "Technical depth", "Research background"]
            },
            {
                "job_title": "Senior ML Engineer",
                "company": "Tech Company",
                "resume_sections": {
                    "summary": "Experienced ML engineer with expertise in scalable systems and team leadership",
                    "skills": "ML Frameworks: PyTorch, TensorFlow | Cloud: AWS, GCP | Tools: Docker, Kubernetes",
                    "experience": [
                        "Led team of 5 engineers to deploy ML pipeline serving 1M+ users",
                        "Optimized model performance achieving 40% improvement in accuracy"
                    ]
                },
                "success_factors": ["Leadership", "Scale", "Technical achievements", "Business impact"]
            }
        ]
    
    def _vectorize_knowledge_bases(self):
        """
        Vectorize knowledge bases for similarity search
        """
        # Vectorize similar jobs
        job_texts = [job["description"] + " " + " ".join(job["skills"]) for job in self.similar_jobs_db]
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
        
        # Vectorize successful resumes
        resume_texts = []
        for resume in self.successful_resumes_db:
            text = resume["job_title"] + " " + resume["company"]
            for section in resume["resume_sections"].values():
                if isinstance(section, list):
                    text += " " + " ".join(section)
                else:
                    text += " " + str(section)
            resume_texts.append(text)
        
        self.resume_vectors = self.vectorizer.transform(resume_texts)
    
    def find_similar_jobs(self, job_description: str, top_k: int = 3) -> List[SimilarJob]:
        """
        Find similar jobs based on job description
        
        Args:
            job_description (str): Target job description
            top_k (int): Number of similar jobs to return
            
        Returns:
            List[SimilarJob]: Similar jobs with similarity scores
        """
        # Vectorize the target job description
        target_vector = self.vectorizer.transform([job_description])
        
        # Calculate similarities
        similarities = cosine_similarity(target_vector, self.job_vectors).flatten()
        
        # Get top-k similar jobs
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        similar_jobs = []
        for idx in top_indices:
            job = self.similar_jobs_db[idx]
            similar_jobs.append(SimilarJob(
                job_title=job["job_title"],
                company=job["company"],
                description=job["description"],
                requirements=job["requirements"],
                skills=job["skills"],
                similarity_score=float(similarities[idx])
            ))
        
        return similar_jobs
    
    def find_successful_resumes(self, similar_jobs: List[SimilarJob], top_k: int = 2) -> List[SuccessfulResume]:
        """
        Find successful resume examples based on similar jobs
        
        Args:
            similar_jobs (List[SimilarJob]): Similar jobs found
            top_k (int): Number of successful resumes to return
            
        Returns:
            List[SuccessfulResume]: Successful resume examples
        """
        # Create query from similar jobs
        query_text = " ".join([job.job_title + " " + " ".join(job.skills) for job in similar_jobs])
        query_vector = self.vectorizer.transform([query_text])
        
        # Calculate similarities with successful resumes
        similarities = cosine_similarity(query_vector, self.resume_vectors).flatten()
        
        # Get top-k successful resumes
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        successful_resumes = []
        for idx in top_indices:
            resume = self.successful_resumes_db[idx]
            successful_resumes.append(SuccessfulResume(
                job_title=resume["job_title"],
                company=resume["company"],
                resume_sections=resume["resume_sections"],
                success_factors=resume["success_factors"],
                relevance_score=float(similarities[idx])
            ))
        
        return successful_resumes
    
    def create_enhanced_prompt(self, job_description: str, section_type: str) -> str:
        """
        Create enhanced prompt using RAG and personal data
        
        Args:
            job_description (str): Target job description
            section_type (str): Type of section to generate (summary, skills, experience, projects)
            
        Returns:
            str: Enhanced prompt
        """
        # Find similar jobs and successful resumes
        similar_jobs = self.find_similar_jobs(job_description)
        successful_resumes = self.find_successful_resumes(similar_jobs)
        
        # Create personal context
        personal_context = self._create_personal_context()
        
        # Create examples context
        examples_context = self._create_examples_context(successful_resumes, section_type)
        
        # Create enhanced prompt based on section type
        if section_type == "summary":
            return self._create_summary_prompt(job_description, personal_context, examples_context, similar_jobs)
        elif section_type == "skills":
            return self._create_skills_prompt(job_description, personal_context, examples_context)
        elif section_type == "experience":
            return self._create_experience_prompt(job_description, personal_context, examples_context)
        elif section_type == "projects":
            return self._create_projects_prompt(job_description, personal_context, examples_context)
        else:
            return self._create_generic_prompt(job_description, personal_context, examples_context)
    
    def _create_personal_context(self) -> str:
        """
        Create personal context string
        """
        context = f"""
        CANDIDATE PERSONAL INFORMATION:
        - Name: {self.personal_data.name}
        - Experience: {self.personal_data.experience_years} years
        - Education: {[edu['degree'] for edu in self.personal_data.education]}
        - Current Role: {self.personal_data.work_experience[0]['title']} at {self.personal_data.work_experience[0]['company']}
        
        KEY SKILLS:
        - Frameworks: {', '.join(self.personal_data.skills['frameworks'])}
        - Tools: {', '.join(self.personal_data.skills['tools'])}
        - Programming: {', '.join(self.personal_data.skills['programming'])}
        
        TOP ACHIEVEMENTS:
        {chr(10).join([f"• {achievement}" for achievement in self.personal_data.achievements[:5]])}
        
        RESEARCH BACKGROUND:
        - Publications: {len(self.personal_data.publications)} research papers
        - PhD in Computer Science with 96/100 GPA
        - Specialization: NGS data analysis, bioinformatics, machine learning
        """
        return context
    
    def _create_examples_context(self, successful_resumes: List[SuccessfulResume], section_type: str) -> str:
        """
        Create examples context from successful resumes
        """
        if not successful_resumes:
            return ""
        
        examples = []
        for resume in successful_resumes:
            if section_type in resume.resume_sections:
                section_content = resume.resume_sections[section_type]
                if isinstance(section_content, list):
                    section_text = "\n".join([f"• {item}" for item in section_content])
                else:
                    section_text = section_content
                
                examples.append(f"""
                SUCCESSFUL EXAMPLE ({resume.job_title} at {resume.company}):
                {section_text}
                
                Success Factors: {', '.join(resume.success_factors)}
                """)
        
        return "\n".join(examples)
    
    def _create_summary_prompt(self, job_description: str, personal_context: str, examples_context: str, similar_jobs: List[SimilarJob]) -> str:
        """
        Create enhanced summary prompt
        """
        similar_jobs_context = "\n".join([
            f"• {job.job_title} at {job.company}: {job.description}"
            for job in similar_jobs
        ])
        
        return f"""
        Create a compelling professional summary for a resume that matches this job description.
        
        JOB DESCRIPTION:
        {job_description}
        
        SIMILAR SUCCESSFUL JOBS:
        {similar_jobs_context}
        
        {personal_context}
        
        SUCCESSFUL SUMMARY EXAMPLES:
        {examples_context}
        
        INSTRUCTIONS:
        1. Use your specific experience years ({self.personal_data.experience_years} years)
        2. Highlight your PhD and research background
        3. Emphasize your expertise in NGS data analysis and bioinformatics
        4. Mention your specific achievements (publications, workshops, high accuracy results)
        5. Show passion for the specific domain
        6. Use active, results-driven language
        7. Keep it to 3-4 sentences maximum
        8. Make it specific to this job, not generic
        
        Return ONLY the summary text, no additional formatting.
        """
    
    def _create_skills_prompt(self, job_description: str, personal_context: str, examples_context: str) -> str:
        """
        Create enhanced skills prompt
        """
        return f"""
        Generate an optimized skills section for a resume based on job requirements.
        
        JOB DESCRIPTION:
        {job_description}
        
        {personal_context}
        
        SUCCESSFUL SKILLS EXAMPLES:
        {examples_context}
        
        INSTRUCTIONS:
        1. Use your actual skills from the personal context
        2. Organize into clear categories (Frameworks, Tools, Programming Languages, Other Skills)
        3. Prioritize skills that match the job requirements
        4. Include specific tools and technologies you've used
        5. Format for ATS compatibility
        6. Limit to 15-20 most relevant skills
        
        Return as JSON:
        {{
            "skills": [
                {{
                    "skill": "string",
                    "category": "string",
                    "relevance_score": float (0.0-1.0),
                    "proficiency_level": "string"
                }}
            ]
        }}
        """
    
    def _create_experience_prompt(self, job_description: str, personal_context: str, examples_context: str) -> str:
        """
        Create enhanced experience prompt
        """
        experience_context = "\n".join([
            f"• {exp['title']} at {exp['company']} ({exp['dates']}): {', '.join(exp['achievements'][:2])}"
            for exp in self.personal_data.work_experience
        ])
        
        return f"""
        Generate optimized work experience bullet points based on job requirements.
        
        JOB DESCRIPTION:
        {job_description}
        
        {personal_context}
        
        YOUR EXPERIENCE:
        {experience_context}
        
        SUCCESSFUL EXPERIENCE EXAMPLES:
        {examples_context}
        
        INSTRUCTIONS:
        1. Use your actual work experience and achievements
        2. Quantify results with specific metrics
        3. Use strong action verbs
        4. Highlight relevant technical skills and tools
        5. Show progression and leadership
        6. Make each bullet point specific and impactful
        7. Focus on achievements that match the job requirements
        
        Return as JSON:
        {{
            "experience_bullets": [
                {{
                    "company": "string",
                    "title": "string",
                    "bullet": "string",
                    "keywords_used": ["string"],
                    "impact": "string"
                }}
            ]
        }}
        """
    
    def _create_projects_prompt(self, job_description: str, personal_context: str, examples_context: str) -> str:
        """
        Create enhanced projects prompt
        """
        projects_context = "\n".join([
            f"• {proj['name']}: {proj['description']} | Technologies: {', '.join(proj['technologies'])} | Outcomes: {', '.join(proj['outcomes'])}"
            for proj in self.personal_data.projects
        ])
        
        return f"""
        Generate optimized project descriptions based on job requirements.
        
        JOB DESCRIPTION:
        {job_description}
        
        {personal_context}
        
        YOUR PROJECTS:
        {projects_context}
        
        SUCCESSFUL PROJECT EXAMPLES:
        {examples_context}
        
        INSTRUCTIONS:
        1. Use your actual projects from the personal context
        2. Highlight research projects and publications
        3. Emphasize technical depth and methodologies
        4. Show quantifiable results and impact
        5. Connect projects to job requirements
        6. Include specific technologies and tools used
        7. Focus on domain-relevant projects (NGS, bioinformatics, ML)
        
        Return as JSON:
        {{
            "projects": [
                {{
                    "name": "string",
                    "description": "string",
                    "technologies": ["string"],
                    "outcomes": ["string"],
                    "relevance_explanation": "string"
                }}
            ]
        }}
        """
    
    def _create_generic_prompt(self, job_description: str, personal_context: str, examples_context: str) -> str:
        """
        Create generic enhanced prompt
        """
        return f"""
        Generate content for a resume based on job requirements.
        
        JOB DESCRIPTION:
        {job_description}
        
        {personal_context}
        
        SUCCESSFUL EXAMPLES:
        {examples_context}
        
        INSTRUCTIONS:
        1. Use your personal information and experience
        2. Match the job requirements and company culture
        3. Follow the successful examples' patterns
        4. Be specific and quantifiable
        5. Use professional, confident tone
        
        Return the generated content in appropriate format.
        """
    
    def enhance_module_prompt(self, original_prompt: str, job_description: str, section_type: str) -> str:
        """
        Enhance an existing module prompt with RAG and personal context
        
        Args:
            original_prompt (str): Original prompt from existing module
            job_description (str): Job description
            section_type (str): Type of section being generated
            
        Returns:
            str: Enhanced prompt
        """
        # Get RAG context
        similar_jobs = self.find_similar_jobs(job_description)
        successful_resumes = self.find_successful_resumes(similar_jobs)
        
        # Create enhanced context
        personal_context = self._create_personal_context()
        examples_context = self._create_examples_context(successful_resumes, section_type)
        
        # Enhance the original prompt
        enhanced_prompt = f"""
        {original_prompt}
        
        ENHANCED CONTEXT:
        
        PERSONAL BACKGROUND:
        {personal_context}
        
        SIMILAR SUCCESSFUL JOBS:
        {chr(10).join([f"• {job.job_title} at {job.company}: {job.description}" for job in similar_jobs])}
        
        SUCCESSFUL EXAMPLES:
        {examples_context}
        
        ADDITIONAL INSTRUCTIONS:
        - Use the personal background information provided
        - Follow patterns from successful examples
        - Make content specific to this job and your background
        - Ensure all information is accurate and verifiable
        """
        
        return enhanced_prompt
