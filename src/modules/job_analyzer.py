"""
Module 1: Job Description Analyzer
Purpose: Extract keywords and requirements from job descriptions
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import openai
from openai import OpenAI
import pandas as pd


@dataclass
class JobKeywords:
    """Data structure for categorized job keywords"""
    technical_skills: List[str]
    soft_skills: List[str]
    tools_technologies: List[str]
    responsibilities: List[str]
    requirements: List[str]
    keywords_frequency: Dict[str, int]


class JobDescriptionAnalyzer:
    """
    Analyzes job descriptions to extract relevant keywords and requirements
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the analyzer with OpenAI API key
        
        Args:
            api_key (str): OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
        
    def extract_keywords(self, job_description: str) -> JobKeywords:
        """
        Extract keywords from job description using OpenAI
        
        Args:
            job_description (str): Raw job description text
            
        Returns:
            JobKeywords: Categorized keywords and requirements
        """
        
        prompt = f"""
        Analyze the following job description and extract relevant keywords and requirements.
        Focus on tech industry roles (AI, Data Science, ML, Software Engineering, etc.).
        
        Job Description:
        {job_description}
        
        Please extract and categorize the following:
        
        1. Technical Skills (programming languages, frameworks, libraries, etc.)
        2. Soft Skills (communication, leadership, problem-solving, etc.)
        3. Tools & Technologies (specific tools, platforms, software, etc.)
        4. Key Responsibilities (main duties and tasks)
        5. Requirements (qualifications, experience, education, etc.)
        
        Also count the frequency of important keywords mentioned.
        
        Return the results in JSON format with the following structure:
        {{
            "technical_skills": ["skill1", "skill2", ...],
            "soft_skills": ["skill1", "skill2", ...],
            "tools_technologies": ["tool1", "tool2", ...],
            "responsibilities": ["responsibility1", "responsibility2", ...],
            "requirements": ["requirement1", "requirement2", ...],
            "keywords_frequency": {{"keyword1": count1, "keyword2": count2, ...}}
        }}
        
        Focus on extracting specific, actionable keywords that would be relevant for resume optimization.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert job description analyzer specializing in tech industry roles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            parsed_data = json.loads(content)
            
            return JobKeywords(
                technical_skills=parsed_data.get("technical_skills", []),
                soft_skills=parsed_data.get("soft_skills", []),
                tools_technologies=parsed_data.get("tools_technologies", []),
                responsibilities=parsed_data.get("responsibilities", []),
                requirements=parsed_data.get("requirements", []),
                keywords_frequency=parsed_data.get("keywords_frequency", {})
            )
            
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return JobKeywords([], [], [], [], [], {})
    
    def analyze_job_role(self, job_description: str) -> Dict[str, Any]:
        """
        Comprehensive job analysis including role classification
        
        Args:
            job_description (str): Raw job description text
            
        Returns:
            Dict: Complete analysis including role type and recommendations
        """
        
        # Extract keywords
        keywords = self.extract_keywords(job_description)
        
        # Analyze role type
        role_analysis = self._classify_role(job_description)
        
        # Get keyword insights
        insights = self._generate_insights(keywords)
        
        return {
            "keywords": keywords,
            "role_analysis": role_analysis,
            "insights": insights,
            "recommendations": self._generate_recommendations(keywords, role_analysis)
        }
    
    def _classify_role(self, job_description: str) -> Dict[str, Any]:
        """
        Classify the job role type and seniority level
        """
        
        prompt = f"""
        Analyze this job description and classify the role:
        
        {job_description}
        
        Determine:
        1. Primary role category (Data Scientist, ML Engineer, Software Engineer, etc.)
        2. Seniority level (Junior, Mid-level, Senior, Lead, etc.)
        3. Industry focus (AI/ML, Web Development, Data Analytics, etc.)
        4. Required experience level (years)
        
        Return as JSON:
        {{
            "role_category": "string",
            "seniority_level": "string", 
            "industry_focus": "string",
            "experience_years": "string"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert job classifier for tech roles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            print(f"Error classifying role: {e}")
            return {
                "role_category": "Unknown",
                "seniority_level": "Unknown",
                "industry_focus": "Unknown", 
                "experience_years": "Unknown"
            }
    
    def _generate_insights(self, keywords: JobKeywords) -> Dict[str, Any]:
        """
        Generate insights from extracted keywords
        """
        
        insights = {
            "total_technical_skills": len(keywords.technical_skills),
            "total_soft_skills": len(keywords.soft_skills),
            "total_tools": len(keywords.tools_technologies),
            "most_frequent_keywords": sorted(
                keywords.keywords_frequency.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10],
            "skill_categories": {
                "programming_languages": [skill for skill in keywords.technical_skills 
                                        if any(lang in skill.lower() for lang in 
                                              ['python', 'java', 'javascript', 'c++', 'c#', 'r', 'sql', 'go', 'rust'])],
                "frameworks": [skill for skill in keywords.technical_skills 
                             if any(fw in skill.lower() for fw in 
                                   ['tensorflow', 'pytorch', 'scikit', 'django', 'flask', 'react', 'angular', 'vue'])],
                "databases": [skill for skill in keywords.tools_technologies 
                            if any(db in skill.lower() for db in 
                                  ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sql', 'nosql'])]
            }
        }
        
        return insights
    
    def _generate_recommendations(self, keywords: JobKeywords, role_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on keywords and role analysis
        """
        
        recommendations = []
        
        # Technical skills recommendations
        if len(keywords.technical_skills) < 5:
            recommendations.append("Consider adding more technical skills to your resume")
        
        # Tools recommendations
        if len(keywords.tools_technologies) < 3:
            recommendations.append("Include relevant tools and technologies in your resume")
        
        # Soft skills recommendations
        if len(keywords.soft_skills) < 3:
            recommendations.append("Highlight soft skills like communication and teamwork")
        
        # Experience level recommendations
        if "senior" in role_analysis.get("seniority_level", "").lower():
            recommendations.append("Emphasize leadership and project management experience")
        
        return recommendations
    
    def save_analysis(self, analysis: Dict[str, Any], filename: str = "job_analysis.json"):
        """
        Save analysis results to JSON file
        
        Args:
            analysis (Dict): Analysis results
            filename (str): Output filename
        """
        
        # Convert dataclass to dict for JSON serialization
        analysis_copy = analysis.copy()
        analysis_copy["keywords"] = {
            "technical_skills": analysis["keywords"].technical_skills,
            "soft_skills": analysis["keywords"].soft_skills,
            "tools_technologies": analysis["keywords"].tools_technologies,
            "responsibilities": analysis["keywords"].responsibilities,
            "requirements": analysis["keywords"].requirements,
            "keywords_frequency": analysis["keywords"].keywords_frequency
        }
        
        with open(filename, 'w') as f:
            json.dump(analysis_copy, f, indent=2)
        
        print(f"Analysis saved to {filename}")


def main():
    """
    Example usage of the JobDescriptionAnalyzer
    """
    
    # Example job description
    sample_jd = """
    Senior Data Scientist
    
    We are looking for a Senior Data Scientist to join our AI team. You will be responsible for:
    
    - Developing machine learning models using Python, TensorFlow, and PyTorch
    - Analyzing large datasets using SQL, Pandas, and NumPy
    - Building predictive models for customer behavior analysis
    - Collaborating with engineering teams to deploy models
    - Communicating findings to stakeholders
    
    Requirements:
    - 5+ years experience in data science or machine learning
    - Strong programming skills in Python and SQL
    - Experience with deep learning frameworks
    - Excellent communication and problem-solving skills
    - Master's degree in Computer Science, Statistics, or related field
    
    Preferred:
    - Experience with cloud platforms (AWS, GCP)
    - Knowledge of MLOps and model deployment
    - Experience with A/B testing and experimentation
    """
    
    # Initialize analyzer (you'll need to set your API key)
    api_key = "your_openai_api_key_here"  # Replace with actual API key
    analyzer = JobDescriptionAnalyzer(api_key)
    
    # Analyze job description
    analysis = analyzer.analyze_job_role(sample_jd)
    
    # Print results
    print("=== Job Analysis Results ===")
    print(f"Role: {analysis['role_analysis']['role_category']}")
    print(f"Level: {analysis['role_analysis']['seniority_level']}")
    print(f"Industry: {analysis['role_analysis']['industry_focus']}")
    
    print("\n=== Technical Skills ===")
    for skill in analysis['keywords'].technical_skills:
        print(f"- {skill}")
    
    print("\n=== Tools & Technologies ===")
    for tool in analysis['keywords'].tools_technologies:
        print(f"- {tool}")
    
    print("\n=== Recommendations ===")
    for rec in analysis['recommendations']:
        print(f"- {rec}")
    
    # Save analysis
    analyzer.save_analysis(analysis)


if __name__ == "__main__":
    main() 