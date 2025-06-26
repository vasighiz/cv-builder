"""
LLM Interface Module
Purpose: Unified interface for switching between local and API LLM models in resume builder modules
"""

import os
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from dotenv import load_dotenv

# Import our LLM manager
from .local_llm_manager import LLMManager, LLMConfig, MISTRAL_7B_GGUF_CONFIG, GPT4_CONFIG, create_llm_manager

# Load environment variables
load_dotenv()

class LLMInterface:
    """Unified interface for LLM operations in resume builder"""
    
    def __init__(self, default_provider: str = "local"):
        """
        Initialize LLM interface
        
        Args:
            default_provider (str): Default provider ('local' or 'api')
        """
        self.manager = create_llm_manager()
        self.default_provider = default_provider
        
        # Set default provider
        if default_provider in self.manager.providers:
            self.manager.set_provider(default_provider)
        else:
            available = list(self.manager.providers.keys())
            if available:
                self.manager.set_provider(available[0])
                print(f"⚠️  Provider '{default_provider}' not available, using '{available[0]}'")
            else:
                raise RuntimeError("No LLM providers available")
    
    def generate_text(self, prompt: str, provider: Optional[str] = None, **kwargs) -> str:
        """
        Generate text using LLM
        
        Args:
            prompt (str): Input prompt
            provider (str, optional): Provider to use ('local' or 'api')
            **kwargs: Additional generation parameters
            
        Returns:
            str: Generated text
        """
        return self.manager.generate(prompt, provider, **kwargs)
    
    def switch_provider(self, provider: str):
        """Switch to different provider"""
        self.manager.set_provider(provider)
        self.default_provider = provider
    
    def get_available_providers(self) -> Dict[str, bool]:
        """Get available providers and their status"""
        providers = {}
        for name, provider in self.manager.providers.items():
            providers[name] = provider.is_available()
        return providers
    
    def get_usage_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get usage statistics"""
        return self.manager.get_usage_stats()
    
    def test_connection(self, provider: Optional[str] = None) -> bool:
        """Test connection to provider"""
        try:
            provider_name = provider or self.default_provider
            test_response = self.manager.generate(
                "Hello, this is a test.", 
                provider=provider_name, 
                max_tokens=10
            )
            return "Error" not in test_response
        except Exception:
            return False

def create_llm_interface(provider: str = "local") -> LLMInterface:
    """
    Create LLM interface with specified provider
    
    Args:
        provider (str): Provider to use ('local' or 'api')
        
    Returns:
        LLMInterface: Configured LLM interface
    """
    return LLMInterface(provider)

# Convenience functions for resume builder modules
def generate_resume_summary(job_description: str, cv_data: Dict[str, Any], provider: str = "local") -> str:
    """
    Generate professional summary for resume
    
    Args:
        job_description (str): Job description text
        cv_data (Dict): CV data
        provider (str): LLM provider to use
        
    Returns:
        str: Generated professional summary
    """
    llm = create_llm_interface(provider)
    
    prompt = f"""
    Create a compelling professional summary for a resume based on this job description and CV data.
    
    JOB DESCRIPTION:
    {job_description}
    
    CV DATA:
    {cv_data}
    
    Generate a professional summary that:
    1. Highlights relevant skills and experience
    2. Matches the job requirements
    3. Is 2-3 sentences long
    4. Uses professional language
    """
    
    return llm.generate_text(prompt, max_tokens=150)

def generate_skills_section(job_requirements: List[str], candidate_skills: List[str], provider: str = "local") -> str:
    """
    Generate skills section for resume
    
    Args:
        job_requirements (List[str]): Job requirements
        candidate_skills (List[str]): Candidate skills
        provider (str): LLM provider to use
        
    Returns:
        str: Generated skills section
    """
    llm = create_llm_interface(provider)
    
    prompt = f"""
    Create a skills section for a resume based on job requirements and candidate skills.
    
    JOB REQUIREMENTS:
    {job_requirements}
    
    CANDIDATE SKILLS:
    {candidate_skills}
    
    Generate a skills section that:
    1. Prioritizes skills that match job requirements
    2. Groups skills by category (Technical, Soft Skills, Tools, etc.)
    3. Uses bullet points or comma-separated format
    4. Is concise and professional
    """
    
    return llm.generate_text(prompt, max_tokens=200)

def generate_experience_bullets(job_title: str, responsibilities: List[str], provider: str = "local") -> List[str]:
    """
    Generate experience bullet points for resume
    
    Args:
        job_title (str): Job title
        responsibilities (List[str]): Job responsibilities
        provider (str): LLM provider to use
        
    Returns:
        List[str]: Generated bullet points
    """
    llm = create_llm_interface(provider)
    
    prompt = f"""
    Create 3-4 professional bullet points for a resume based on this job information.
    
    JOB TITLE: {job_title}
    RESPONSIBILITIES: {responsibilities}
    
    Generate bullet points that:
    1. Start with action verbs
    2. Include quantifiable achievements when possible
    3. Are specific and relevant
    4. Follow the format: "• Action verb + what + result/impact"
    5. Are 1-2 lines each
    """
    
    response = llm.generate_text(prompt, max_tokens=300)
    
    # Parse bullet points from response
    bullets = []
    for line in response.split('\n'):
        line = line.strip()
        if line.startswith('•') or line.startswith('-'):
            bullets.append(line)
        elif line and not bullets:  # First non-empty line without bullet
            bullets.append(f"• {line}")
    
    return bullets[:4]  # Return max 4 bullets

def analyze_job_description(job_description: str, provider: str = "local") -> Dict[str, Any]:
    """
    Analyze job description to extract key information
    
    Args:
        job_description (str): Job description text
        provider (str): LLM provider to use
        
    Returns:
        Dict[str, Any]: Analysis results
    """
    llm = create_llm_interface(provider)
    
    prompt = f"""
    Analyze this job description and extract key information in JSON format.
    
    JOB DESCRIPTION:
    {job_description}
    
    Extract and return as JSON:
    {{
        "role_title": "string",
        "seniority_level": "string",
        "required_skills": ["skill1", "skill2"],
        "preferred_skills": ["skill1", "skill2"],
        "responsibilities": ["resp1", "resp2"],
        "requirements": ["req1", "req2"],
        "industry": "string",
        "experience_years": "string"
    }}
    """
    
    response = llm.generate_text(prompt, max_tokens=500)
    
    # Try to parse JSON from response
    try:
        import json
        # Find JSON in response
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = response[start:end]
            return json.loads(json_str)
        else:
            raise ValueError("No JSON found in response")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return {
            "role_title": "Unknown",
            "seniority_level": "Unknown",
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "requirements": [],
            "industry": "Unknown",
            "experience_years": "Unknown"
        }

# Example usage and testing
def test_llm_interface():
    """Test the LLM interface"""
    print("🚀 Testing LLM Interface")
    print("=" * 50)
    
    # Create interface
    llm = create_llm_interface("local")
    
    # Test providers
    results = llm.get_available_providers()
    
    # Test content generation
    test_prompt = """
    Create a professional summary for a data scientist resume with the following requirements:
    - 3-4 sentences maximum
    - Focus on machine learning and data analysis
    - Include Python and SQL skills
    - Professional tone
    """
    
    print("\n📝 Testing content generation...")
    response = llm.generate_text(test_prompt)
    
    if response:
        print("✅ Generated content:")
        print(response)
    else:
        print("❌ Failed to generate content")
    
    # Show usage stats
    print("\n📊 Usage Statistics:")
    stats = llm.get_usage_stats()
    for provider, data in stats.items():
        print(f"{provider.capitalize()}: {data['calls']} calls, {data['tokens']} tokens, {data['errors']} errors")

if __name__ == "__main__":
    test_llm_interface() 