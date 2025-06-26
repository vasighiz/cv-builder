"""
Module 1: Job Description Analyzer - MVP Version
Purpose: Extract keywords and requirements from job descriptions
"""

import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from openai import OpenAI


@dataclass
class JobKeywords:
    """Data structure for categorized job keywords"""
    technical_skills: List[str]
    soft_skills: List[str]
    tools_technologies: List[str]
    responsibilities: List[str]
    requirements: List[str]
    keywords_frequency: Dict[str, int]


class JobDescriptionAnalyzerMVP:
    """
    MVP version of job description analyzer
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the analyzer
        
        Args:
            api_key (str): OpenAI API key (optional, can use env var)
        """
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"
        
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert job description analyzer. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up the response (remove markdown if present)
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
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
            print(f"❌ Error extracting keywords: {e}")
            # Return empty structure on error
            return JobKeywords([], [], [], [], [], {})
    
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert job classifier. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
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
        
        insights = {
            "total_technical_skills": len(keywords.technical_skills),
            "total_soft_skills": len(keywords.soft_skills),
            "total_tools": len(keywords.tools_technologies),
            "most_frequent_keywords": sorted(
                keywords.keywords_frequency.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
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
        # Note: You need to set OPENAI_API_KEY environment variable or pass api_key parameter
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
        print("💡 Set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your_api_key_here'")
        print("   or pass api_key parameter to JobDescriptionAnalyzerMVP()")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main() 