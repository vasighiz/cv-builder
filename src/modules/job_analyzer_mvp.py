"""
Module 1: Job Description Analyzer - MVP Version
Purpose: Extract keywords and requirements from job descriptions
"""

import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class JobKeywords:
    """Data structure for categorized job keywords"""
    technical_skills: List[str]
    soft_skills: List[str]
    tools_technologies: List[str]
    responsibilities: List[str]
    requirements: List[str]
    keywords_frequency: Dict[str, int]
    extracted_skills: List[str]  # New field for skills extracted from descriptions


class JobDescriptionAnalyzerMVP:
    """
    MVP version of job description analyzer
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the analyzer
        
        Args:
            api_key (str): Anthropic API key (optional, can use env var)
        """
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"
        
    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """
        Main method to analyze job description
        
        Args:
            job_description (str): Raw job description text
            
        Returns:
            Dict: Complete analysis results
        """
        print("🔍 Analyzing job description...")
        
        # Extract keywords
        keywords = self._extract_keywords(job_description)
        
        # Extract skills from descriptions
        skills_from_descriptions = self._extract_skills_from_descriptions(keywords.responsibilities, keywords.requirements)
        
        # Update keywords with extracted skills
        keywords.extracted_skills = skills_from_descriptions
        
        # Analyze role type
        role_analysis = self._classify_role(job_description)
        
        # Generate insights
        insights = self._generate_insights(keywords)
        
        # Create results
        results = {
            "keywords": asdict(keywords),
            "role_analysis": role_analysis,
            "insights": insights,
            "recommendations": self._generate_recommendations(keywords, role_analysis)
        }
        
        print("✅ Analysis complete!")
        return results
    
    def _extract_keywords(self, job_description: str) -> JobKeywords:
        """
        Extract keywords from job description using OpenAI
        """
        
        prompt = f"""
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
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.2,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text.strip()
            
            # Clean up the response (remove markdown if present)
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Try to parse JSON with better error handling
            try:
                parsed_data = json.loads(content)
            except json.JSONDecodeError as json_error:
                print(f"⚠️  JSON parsing error: {json_error}")
                print(f"Raw response: {content[:200]}...")
                
                # Try to extract JSON from the response using a more flexible approach
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    try:
                        parsed_data = json.loads(json_match.group())
                        print("✅ Successfully extracted JSON from response")
                    except json.JSONDecodeError:
                        print("❌ Failed to extract valid JSON, using fallback")
                        parsed_data = {}
                else:
                    print("❌ No JSON found in response, using fallback")
                    parsed_data = {}
            
            return JobKeywords(
                technical_skills=parsed_data.get("technical_skills", []),
                soft_skills=parsed_data.get("soft_skills", []),
                tools_technologies=parsed_data.get("tools_technologies", []),
                responsibilities=parsed_data.get("responsibilities", []),
                requirements=parsed_data.get("requirements", []),
                keywords_frequency=parsed_data.get("keywords_frequency", {}),
                extracted_skills=parsed_data.get("extracted_skills", [])
            )
            
        except Exception as e:
            print(f"❌ Error extracting keywords: {e}")
            # Return empty structure on error
            return JobKeywords([], [], [], [], [], {}, [])
    
    def _extract_skills_from_descriptions(self, responsibilities: List[str], requirements: List[str]) -> List[str]:
        """
        Extract specific skills from responsibilities and requirements descriptions
        """
        
        # Combine all descriptions for analysis
        all_descriptions = responsibilities + requirements
        if not all_descriptions:
            return []
        
        combined_text = " ".join(all_descriptions)
        
        prompt = f"""
        Analyze the following job descriptions and infer the necessary technical skills, programming languages, and tools required.
        Focus on understanding the context and extracting skills that are implied by the tasks and requirements.
        
        Job Descriptions:
        {combined_text}
        
        Extract and infer the following:
        - Programming Languages: Identify languages likely needed based on tasks (e.g., Python for data analysis, R for advanced statistics)
        - Tools & Technologies: Identify tools and technologies implied by the tasks (e.g., SQL for database querying, SAS for statistical analysis)
        - Statistical Packages: Identify statistical packages likely used (e.g., scikit-learn, R, SAS)
        - Data Mining Methods: Identify data mining methods and tools implied by the tasks
        - Scripting & Automation: Identify scripting languages and tools for automation and testing
        
        Examples of what to extract:
        - SQL (for data querying from structured databases)
        - Python (with packages like scikit-learn, statsmodels, pandas)
        - R (for advanced statistics)
        - SAS, SPSS (depending on industry)
        - Data mining tools and methods
        - Scripting for automated analysis and testing
        
        Return ONLY a JSON array of inferred skills:
        ["skill1", "skill2", "skill3"]
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text.strip()
            
            # Clean up the response
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Try to parse JSON with better error handling
            try:
                extracted_skills = json.loads(content)
            except json.JSONDecodeError as json_error:
                print(f"⚠️  JSON parsing error in skill extraction: {json_error}")
                print(f"Raw response: {content[:200]}...")
                
                # Try to extract JSON array from the response
                import re
                array_match = re.search(r'\[.*\]', content, re.DOTALL)
                if array_match:
                    try:
                        extracted_skills = json.loads(array_match.group())
                        print("✅ Successfully extracted skills array from response")
                    except json.JSONDecodeError:
                        print("❌ Failed to extract valid skills array, using fallback")
                        extracted_skills = []
                else:
                    print("❌ No skills array found in response, using fallback")
                    extracted_skills = []
            
            # Ensure it's a list and remove duplicates
            if isinstance(extracted_skills, list):
                return list(set(extracted_skills))
            else:
                return []
                
        except Exception as e:
            print(f"❌ Error extracting skills from descriptions: {e}")
            return []
    
    def _classify_role(self, job_description: str) -> Dict[str, str]:
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
        
        Return ONLY a JSON object:
        {{
            "role_category": "string",
            "seniority_level": "string", 
            "industry_focus": "string",
            "experience_years": "string"
        }}
        """
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                temperature=0.2,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text.strip()
            
            # Clean up the response
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content)
            
        except Exception as e:
            print(f"❌ Error classifying role: {e}")
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
        
        # Improved skill categorization logic
        programming_languages = []
        frameworks_libraries = []
        databases = []
        other_technical = []
        others = []
        
        for skill in keywords.technical_skills:
            skill_lower = skill.lower()
            
            # Programming languages - more specific matching
            if any(lang in skill_lower for lang in ['python', 'java', 'javascript', 'js', 'c++', 'c#', 'r', 'go', 'rust', 'scala', 'kotlin', 'swift', 'php', 'ruby', 'perl', 'bash', 'shell']) and not any(exclude in skill_lower for exclude in ['libraries', 'algorithms', 'frameworks', 'tools', 'unix', 'environment', 'platform']):
                programming_languages.append(skill)
            # Frameworks and libraries
            elif any(fw in skill_lower for fw in ['tensorflow', 'pytorch', 'scikit', 'keras', 'django', 'flask', 'react', 'angular', 'vue', 'node.js', 'spring', 'express', 'fastapi', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'bokeh', 'd3.js', 'bootstrap', 'jquery', 'libraries', 'frameworks']):
                frameworks_libraries.append(skill)
            # Databases
            elif any(db in skill_lower for db in ['mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'sqlite', 'oracle', 'sql server']):
                databases.append(skill)
            # Other technical skills (ML, algorithms, etc.)
            else:
                other_technical.append(skill)
        
        # Categorize tools and technologies
        cloud_platforms = []
        other_tools = []
        
        for tool in keywords.tools_technologies:
            tool_lower = tool.lower()
            if any(cloud in tool_lower for cloud in ['aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'kubernetes', 'docker', 'jenkins', 'gitlab', 'github']):
                cloud_platforms.append(tool)
            else:
                other_tools.append(tool)
        
        # Add any remaining uncategorized items to "others"
        # This includes items from soft_skills, responsibilities, requirements that don't fit other categories
        for skill in keywords.soft_skills:
            others.append(skill)
        
        # Filter responsibilities and requirements - only add short, skill-like items
        for resp in keywords.responsibilities:
            # Only add if it's a short phrase that looks like a skill (not a full sentence)
            if len(resp.split()) <= 5 and not resp.endswith('.') and not any(word in resp.lower() for word in ['experience', 'years', 'degree', 'responsibility', 'requirement']):
                others.append(resp)
        
        for req in keywords.requirements:
            # Only add if it's a short phrase that looks like a skill (not a full sentence)
            if len(req.split()) <= 5 and not req.endswith('.') and not any(word in req.lower() for word in ['experience', 'years', 'degree', 'responsibility', 'requirement']):
                others.append(req)
        
        # Process extracted skills - add them to appropriate categories or create new ones
        extracted_technical = []
        extracted_tools = []
        extracted_methodologies = []
        extracted_certifications = []
        extracted_skills_others = []
        
        for skill in keywords.extracted_skills:
            skill_lower = skill.lower()
            
            # Check if it's already in technical_skills or tools_technologies
            if skill in keywords.technical_skills or skill in keywords.tools_technologies:
                continue
                
            # Filter out long sentences and requirements
            if len(skill.split()) > 8 or any(word in skill_lower for word in ['experience', 'years', 'degree', 'responsibility', 'requirement', 'master', 'bachelor']):
                continue
                
            # Categorize extracted skills
            if any(tech in skill_lower for tech in ['python', 'java', 'javascript', 'sql', 'r', 'scala', 'go', 'rust', 'c++', 'c#', 'php', 'ruby', 'perl', 'bash', 'shell', 'html', 'css', 'typescript']):
                extracted_technical.append(skill)
            elif any(tool in skill_lower for tool in ['git', 'docker', 'kubernetes', 'jenkins', 'jira', 'confluence', 'slack', 'aws', 'azure', 'gcp', 'tableau', 'powerbi', 'excel', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'matplotlib', 'seaborn']):
                extracted_tools.append(skill)
            elif any(method in skill_lower for method in ['agile', 'scrum', 'kanban', 'ci/cd', 'devops', 'lean', 'six sigma', 'waterfall', 'regression', 'neural', 'pca', 'svm', 'clustering']):
                extracted_methodologies.append(skill)
            elif any(cert in skill_lower for cert in ['certified', 'certification', 'pmp', 'aws', 'azure', 'google', 'cisco', 'comptia']):
                extracted_certifications.append(skill)
            else:
                # Add to other technical if it seems technical, otherwise to extracted_skills_others
                if any(tech_indicator in skill_lower for tech_indicator in ['analysis', 'modeling', 'development', 'testing', 'deployment', 'automation', 'optimization', 'visualization', 'machine learning', 'data science', 'statistical']):
                    extracted_technical.append(skill)
                else:
                    extracted_skills_others.append(skill)
        
        insights = {
            "total_technical_skills": len(keywords.technical_skills),
            "total_soft_skills": len(keywords.soft_skills),
            "total_tools": len(keywords.tools_technologies),
            "total_extracted_skills": len(keywords.extracted_skills),
            "most_frequent_keywords": sorted(
                keywords.keywords_frequency.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
            "skill_categories": {
                "programming_languages": programming_languages,
                "frameworks_libraries": frameworks_libraries,
                "databases": databases,
                "other_technical_skills": other_technical,
                "cloud_platforms": cloud_platforms,
                "other_tools": other_tools,
                "extracted_technical_skills": extracted_technical,
                "extracted_tools": extracted_tools,
                "extracted_methodologies": extracted_methodologies,
                "extracted_certifications": extracted_certifications,
                "extracted_skills_others": extracted_skills_others,
                "others": others
            }
        }
        
        return insights
    
    def _generate_recommendations(self, keywords: JobKeywords, role_analysis: Dict[str, str]) -> List[str]:
        """
        Generate recommendations based on keywords and role analysis
        """
        
        recommendations = []
        
        # Technical skills recommendations
        if len(keywords.technical_skills) < 3:
            recommendations.append("⚠️  Consider adding more technical skills to your resume")
        elif len(keywords.technical_skills) < 5:
            recommendations.append("📝 Add more technical skills to improve keyword coverage")
        
        # Tools recommendations
        if len(keywords.tools_technologies) < 2:
            recommendations.append("🛠️  Include relevant tools and technologies in your resume")
        
        # Soft skills recommendations
        if len(keywords.soft_skills) < 2:
            recommendations.append("🤝 Highlight soft skills like communication and teamwork")
        
        # Experience level recommendations
        if "senior" in role_analysis.get("seniority_level", "").lower():
            recommendations.append("👑 Emphasize leadership and project management experience")
        elif "junior" in role_analysis.get("seniority_level", "").lower():
            recommendations.append("🎓 Focus on education, projects, and internships")
        
        return recommendations
    
    def save_analysis(self, analysis: Dict[str, Any], filename: str = "job_analysis.json"):
        """
        Save analysis results to JSON file
        """
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Analysis saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
    
    def print_analysis_summary(self, analysis: Dict[str, Any]):
        """
        Print a formatted summary of the analysis
        """
        
        print("\n" + "="*50)
        print("📊 JOB ANALYSIS SUMMARY")
        print("="*50)
        
        # Role analysis
        role = analysis["role_analysis"]
        print(f"🎯 Role: {role['role_category']}")
        print(f"📈 Level: {role['seniority_level']}")
        print(f"🏭 Industry: {role['industry_focus']}")
        print(f"⏰ Experience: {role['experience_years']}")
        
        # Keywords
        keywords = analysis["keywords"]
        print(f"\n🔧 Technical Skills ({len(keywords['technical_skills'])}):")
        for skill in keywords['technical_skills'][:5]:
            print(f"   • {skill}")
        
        print(f"\n🛠️  Tools & Technologies ({len(keywords['tools_technologies'])}):")
        for tool in keywords['tools_technologies'][:5]:
            print(f"   • {tool}")
        
        print(f"\n🤝 Soft Skills ({len(keywords['soft_skills'])}):")
        for skill in keywords['soft_skills'][:3]:
            print(f"   • {skill}")
        
        # Display extracted skills
        if keywords.get('extracted_skills'):
            print(f"\n🔍 Extracted Skills ({len(keywords['extracted_skills'])}):")
            for skill in keywords['extracted_skills'][:5]:
                print(f"   • {skill}")
        
        # Insights
        insights = analysis["insights"]
        print(f"\n📈 Most Frequent Keywords:")
        for keyword, count in insights['most_frequent_keywords'][:3]:
            print(f"   • {keyword}: {count} times")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"   {rec}")
        
        print("="*50)


def main():
    """
    Example usage and testing of the MVP Job Description Analyzer
    """
    
    # Sample job description for testing
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
    
    print("🚀 Testing Job Description Analyzer MVP")
    print("="*50)
    
    try:
        # Initialize analyzer
        # Note: You need to set ANTHROPIC_API_KEY environment variable or pass api_key parameter
        analyzer = JobDescriptionAnalyzerMVP()
        
        # Analyze job description
        analysis = analyzer.analyze_job_description(sample_jd)
        
        # Print summary
        analyzer.print_analysis_summary(analysis)
        
        # Save results
        analyzer.save_analysis(analysis, "sample_job_analysis.json")
        
        print("\n✅ MVP test completed successfully!")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Set your Anthropic API key:")
        print("   export ANTHROPIC_API_KEY='your_api_key_here'")
        print("   or pass api_key parameter to JobDescriptionAnalyzerMVP()")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 