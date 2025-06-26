"""
Example: Using Local LLM for Resume Generation
Purpose: Demonstrate how to use the local LLM manager for resume building
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from modules.llm_interface import create_llm_interface
from modules.enhanced_resume_generator import EnhancedResumeGenerator

def example_basic_llm_usage():
    """Example of basic LLM usage"""
    print("🎯 Example: Basic LLM Usage")
    print("=" * 50)
    
    # Create LLM interface with local provider
    llm = create_llm_interface("local")
    
    # Test prompt
    prompt = "Write a professional summary for a data scientist with 3 years of experience."
    
    print(f"Prompt: {prompt}")
    print("Generating response with local LLM...")
    
    response = llm.generate_response(prompt)
    
    if response:
        print(f"✅ Response: {response}")
    else:
        print("❌ No response generated")
    
    # Show usage stats
    stats = llm.get_usage_stats()
    print(f"\n📊 Usage Stats: {stats}")

def example_provider_switching():
    """Example of switching between providers"""
    print("\n🔄 Example: Provider Switching")
    print("=" * 50)
    
    # Start with local provider
    llm = create_llm_interface("local")
    
    # Generate with local
    print("Generating with local LLM...")
    local_response = llm.generate_response("List 3 key skills for a machine learning engineer.")
    print(f"Local response: {local_response[:100]}...")
    
    # Switch to API (if available)
    print("\nSwitching to API provider...")
    if llm.set_provider("api"):
        api_response = llm.generate_response("List 3 key skills for a machine learning engineer.")
        print(f"API response: {api_response[:100]}...")
    else:
        print("API provider not available")
    
    # Switch back to local
    print("\nSwitching back to local provider...")
    llm.set_provider("local")
    
    # Show final stats
    stats = llm.get_usage_stats()
    print(f"\n📊 Final Usage Stats: {stats}")

def example_resume_enhancement():
    """Example of resume enhancement using local LLM"""
    print("\n📝 Example: Resume Enhancement")
    print("=" * 50)
    
    # Create enhanced resume generator with local LLM
    generator = EnhancedResumeGenerator(llm_provider="local")
    
    # Example original content
    original_summary = "Data scientist with Python experience."
    job_requirements = ["machine learning", "data analysis", "python", "sql"]
    candidate_skills = ["python", "pandas", "numpy", "machine learning"]
    
    print("Original summary:", original_summary)
    print("Job requirements:", job_requirements)
    print("Candidate skills:", candidate_skills)
    
    # Enhance the summary
    print("\nEnhancing summary with local LLM...")
    enhanced_section = generator.enhance_professional_summary(
        original_summary, job_requirements, candidate_skills
    )
    
    print(f"Enhanced summary: {enhanced_section.content[0]}")
    print(f"Improvements: {enhanced_section.improvements}")
    
    # Show usage stats
    stats = generator.get_usage_stats()
    print(f"\n📊 Usage Stats: {stats}")

def example_work_experience_enhancement():
    """Example of work experience enhancement"""
    print("\n💼 Example: Work Experience Enhancement")
    print("=" * 50)
    
    generator = EnhancedResumeGenerator(llm_provider="local")
    
    # Example work experience bullets
    original_bullets = [
        "Used Python for data analysis",
        "Worked with machine learning models",
        "Created reports for stakeholders"
    ]
    
    job_keywords = ["python", "machine learning", "data analysis", "automation"]
    
    print("Original bullets:")
    for i, bullet in enumerate(original_bullets, 1):
        print(f"{i}. {bullet}")
    
    print(f"\nJob keywords: {job_keywords}")
    
    # Enhance work experience
    print("\nEnhancing work experience with local LLM...")
    enhanced_section = generator.enhance_work_experience(original_bullets, job_keywords)
    
    print("\nEnhanced bullets:")
    for i, bullet in enumerate(enhanced_section.content, 1):
        print(f"{i}. {bullet}")
    
    print(f"\nImprovements: {enhanced_section.improvements}")

def example_skills_enhancement():
    """Example of skills section enhancement"""
    print("\n🛠️ Example: Skills Enhancement")
    print("=" * 50)
    
    generator = EnhancedResumeGenerator(llm_provider="local")
    
    # Example skills
    original_skills = ["python", "pandas", "numpy", "machine learning", "sql"]
    job_requirements = ["python", "machine learning", "data analysis", "sql", "aws"]
    
    print("Original skills:", original_skills)
    print("Job requirements:", job_requirements)
    
    # Enhance skills
    print("\nEnhancing skills with local LLM...")
    enhanced_section = generator.enhance_skills_section(original_skills, job_requirements)
    
    print(f"Enhanced skills: {enhanced_section.content}")
    print(f"Improvements: {enhanced_section.improvements}")

def main():
    """Run all examples"""
    print("🚀 Local LLM Resume Builder Examples")
    print("=" * 60)
    
    try:
        # Test basic functionality
        example_basic_llm_usage()
        
        # Test provider switching
        example_provider_switching()
        
        # Test resume enhancement
        example_resume_enhancement()
        
        # Test work experience enhancement
        example_work_experience_enhancement()
        
        # Test skills enhancement
        example_skills_enhancement()
        
        print("\n🎉 All examples completed successfully!")
        print("\n💡 Tips:")
        print("- Use 'local' provider for testing and development")
        print("- Use 'api' provider for production and high-quality results")
        print("- Monitor usage stats to track performance")
        print("- Adjust model parameters for speed vs quality trade-offs")
        
    except Exception as e:
        print(f"\n💥 Example failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 