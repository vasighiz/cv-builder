"""
Test script for Module 1 MVP: Job Description Analyzer
"""

import os
import sys
from src.modules.job_analyzer_mvp import JobDescriptionAnalyzerMVP
from dotenv import load_dotenv

load_dotenv()


def test_with_sample_job_descriptions():
    """
    Test the MVP with different sample job descriptions
    """
    
    # Sample job descriptions for testing
    sample_jobs = {
        "data_scientist": """
        Data Scientist - Machine Learning
        
        We are seeking a Data Scientist to join our growing team. You will:
        
        - Develop and implement machine learning models using Python, scikit-learn, and TensorFlow
        - Analyze large datasets using SQL, Pandas, and NumPy
        - Build predictive models for customer segmentation and behavior analysis
        - Collaborate with cross-functional teams to deploy models into production
        - Communicate complex findings to non-technical stakeholders
        
        Requirements:
        - 3+ years experience in data science or machine learning
        - Strong programming skills in Python and SQL
        - Experience with statistical analysis and machine learning algorithms
        - Excellent communication and problem-solving skills
        - Bachelor's degree in Computer Science, Statistics, or related field
        
        Preferred:
        - Experience with deep learning frameworks (TensorFlow, PyTorch)
        - Knowledge of cloud platforms (AWS, Azure)
        - Experience with data visualization tools (Tableau, Power BI)
        """,
        
        "software_engineer": """
        Senior Software Engineer - Full Stack
        
        We're looking for a Senior Software Engineer to build scalable web applications.
        
        Responsibilities:
        - Design and develop full-stack web applications using React, Node.js, and Python
        - Write clean, maintainable code and conduct code reviews
        - Optimize application performance and ensure scalability
        - Collaborate with product managers and designers
        - Mentor junior developers and contribute to technical decisions
        
        Requirements:
        - 5+ years experience in software development
        - Proficiency in JavaScript, Python, and SQL
        - Experience with modern web frameworks (React, Angular, Vue.js)
        - Knowledge of cloud platforms (AWS, GCP, Azure)
        - Strong problem-solving and communication skills
        
        Nice to have:
        - Experience with microservices architecture
        - Knowledge of DevOps practices and CI/CD pipelines
        - Experience with Docker and Kubernetes
        """,
        
        "ml_engineer": """
        Machine Learning Engineer
        
        Join our AI team to build and deploy machine learning models at scale.
        
        Key Responsibilities:
        - Design and implement machine learning pipelines using Python and TensorFlow
        - Develop and optimize ML models for production deployment
        - Build data processing pipelines using Apache Spark and Kafka
        - Implement MLOps practices for model monitoring and deployment
        - Work with data scientists to operationalize research models
        
        Required Skills:
        - 4+ years experience in machine learning or software engineering
        - Strong Python programming skills and experience with ML libraries
        - Experience with cloud platforms (AWS, GCP) and containerization (Docker)
        - Knowledge of distributed computing and big data technologies
        - Excellent problem-solving and collaboration skills
        
        Preferred:
        - Experience with Kubernetes and microservices architecture
        - Knowledge of real-time data processing and streaming
        - Experience with model serving platforms (TensorFlow Serving, MLflow)
        """
    }
    
    print("🧪 Testing Job Description Analyzer MVP")
    print("="*60)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("💡 Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize analyzer
        analyzer = JobDescriptionAnalyzerMVP(api_key)
        
        # Test each job description
        for job_type, job_description in sample_jobs.items():
            print(f"\n🔍 Testing {job_type.replace('_', ' ').title()} job description...")
            print("-" * 40)
            
            # Analyze the job description
            analysis = analyzer.analyze_job_description(job_description)
            
            # Print summary
            analyzer.print_analysis_summary(analysis)
            
            # Save individual results
            filename = f"analysis_{job_type}.json"
            analyzer.save_analysis(analysis, filename)
            
            print(f"💾 Results saved to {filename}")
            print("\n" + "="*60)
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")


def test_custom_job_description():
    """
    Test with a custom job description from user input
    """
    
    print("🎯 Custom Job Description Test")
    print("="*40)
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        return
    
    try:
        # Get custom job description
        print("📝 Enter your job description (press Enter twice to finish):")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        
        job_description = "\n".join(lines[:-1])  # Remove the last empty line
        
        if not job_description.strip():
            print("❌ No job description provided!")
            return
        
        # Initialize analyzer
        analyzer = JobDescriptionAnalyzerMVP(api_key)
        
        # Analyze the job description
        print("\n🔍 Analyzing your job description...")
        analysis = analyzer.analyze_job_description(job_description)
        
        # Print summary
        analyzer.print_analysis_summary(analysis)
        
        # Save results
        analyzer.save_analysis(analysis, "custom_job_analysis.json")
        
        print("✅ Custom analysis completed!")
        
    except KeyboardInterrupt:
        print("\n❌ Analysis cancelled by user")
    except Exception as e:
        print(f"❌ Error during custom analysis: {e}")


def main():
    """
    Main function to run tests
    """
    
    print("🚀 Job Description Analyzer MVP - Test Suite")
    print("="*50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "custom":
            test_custom_job_description()
        else:
            print("Usage: python test_mvp.py [custom]")
            print("  - No arguments: Run sample job tests")
            print("  - 'custom': Test with your own job description")
    else:
        test_with_sample_job_descriptions()


if __name__ == "__main__":
    main() 