"""
Simple test script for Module 1 MVP
"""

import os
from dotenv import load_dotenv
from src.modules.job_analyzer_mvp import JobDescriptionAnalyzerMVP

# Load environment variables from .env file
load_dotenv()

def test_mvp():
    """Test the MVP with a simple job description"""
    
    print("🧪 Testing Module 1 MVP")
    print("="*40)
    
    # Check if API key is loaded
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file!")
        return
    
    print("✅ API key loaded successfully")
    
    # Sample job description
    job_description = """
    Senior Data Scientist - Machine Learning
    
    We are seeking a Senior Data Scientist to join our growing team. You will:
    
    - Develop and implement machine learning models using Python, scikit-learn, and TensorFlow
    - Analyze large datasets using SQL, Pandas, and NumPy
    - Build predictive models for customer segmentation and behavior analysis
    - Collaborate with cross-functional teams to deploy models into production
    - Communicate complex findings to non-technical stakeholders
    
    Requirements:
    - 5+ years experience in data science or machine learning
    - Strong programming skills in Python and SQL
    - Experience with statistical analysis and machine learning algorithms
    - Excellent communication and problem-solving skills
    - Master's degree in Computer Science, Statistics, or related field
    
    Preferred:
    - Experience with deep learning frameworks (TensorFlow, PyTorch)
    - Knowledge of cloud platforms (AWS, Azure)
    - Experience with data visualization tools (Tableau, Power BI)
    """
    
    try:
        print("🔍 Initializing analyzer...")
        analyzer = JobDescriptionAnalyzerMVP(api_key)
        
        print("🚀 Analyzing job description...")
        analysis = analyzer.analyze_job_description(job_description)
        
        print("\n📊 Analysis Results:")
        analyzer.print_analysis_summary(analysis)
        
        # Save results
        analyzer.save_analysis(analysis, "test_analysis.json")
        
        print("\n✅ Test completed successfully!")
        print("💾 Results saved to: test_analysis.json")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_mvp() 