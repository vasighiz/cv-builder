"""
Setup script for Module 1 MVP: Job Description Analyzer
"""

import os
import sys
import subprocess
import json


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'openai',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    return missing_packages


def install_dependencies(packages):
    """Install missing packages"""
    if not packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(packages)}")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install'
        ] + packages)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment():
    """Set up environment variables"""
    print("\n🔧 Setting up environment...")
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    # Create .env file
    print("📝 Creating .env file...")
    
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if api_key:
        with open(env_file, 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("✅ .env file created with API key")
        return True
    else:
        print("⚠️  No API key provided. You'll need to set OPENAI_API_KEY environment variable manually.")
        print("   You can create a .env file later or set the environment variable.")
        return False


def test_setup():
    """Test the setup by running a simple analysis"""
    print("\n🧪 Testing setup...")
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("💡 Please set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your_api_key_here'")
        print("   or add it to your .env file")
        return False
    
    try:
        # Import and test the analyzer
        from src.modules.job_analyzer_mvp import JobDescriptionAnalyzerMVP
        
        # Simple test job description
        test_jd = """
        Data Scientist
        
        We are looking for a Data Scientist to:
        - Analyze data using Python and SQL
        - Build machine learning models
        - Communicate findings to stakeholders
        
        Requirements:
        - Python programming skills
        - SQL experience
        - Communication skills
        """
        
        analyzer = JobDescriptionAnalyzerMVP(api_key)
        analysis = analyzer.analyze_job_description(test_jd)
        
        print("✅ Setup test successful!")
        print(f"   Extracted {len(analysis['keywords']['technical_skills'])} technical skills")
        print(f"   Role identified: {analysis['role_analysis']['role_category']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False


def create_sample_data():
    """Create sample data files"""
    print("\n📁 Creating sample data...")
    
    # Create data directories if they don't exist
    os.makedirs("src/data/samples", exist_ok=True)
    os.makedirs("src/data/keywords", exist_ok=True)
    os.makedirs("src/data/templates", exist_ok=True)
    
    # Create sample keywords file
    sample_keywords = {
        "programming_languages": [
            "Python", "JavaScript", "Java", "C++", "C#", "R", "SQL", "Go", "Rust", "TypeScript"
        ],
        "frameworks": [
            "TensorFlow", "PyTorch", "scikit-learn", "React", "Angular", "Vue.js", 
            "Django", "Flask", "Node.js", "Spring Boot"
        ],
        "tools": [
            "Git", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Jenkins", 
            "Jira", "Tableau", "Power BI"
        ],
        "soft_skills": [
            "Communication", "Leadership", "Problem Solving", "Teamwork", 
            "Time Management", "Adaptability", "Creativity", "Critical Thinking"
        ]
    }
    
    with open("src/data/keywords/master_keywords.json", "w") as f:
        json.dump(sample_keywords, f, indent=2)
    
    print("✅ Sample data created")


def main():
    """Main setup function"""
    print("🚀 Setting up Job Description Analyzer MVP")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    missing_packages = check_dependencies()
    
    # Install missing dependencies
    if missing_packages:
        if not install_dependencies(missing_packages):
            return
    
    # Set up environment
    setup_environment()
    
    # Create sample data
    create_sample_data()
    
    # Test setup
    if test_setup():
        print("\n🎉 Setup completed successfully!")
        print("\n📖 Next steps:")
        print("   1. Run: python test_mvp.py")
        print("   2. Run: python test_mvp.py custom")
        print("   3. Check the generated JSON files for analysis results")
        print("\n💡 Tips:")
        print("   - Make sure your OpenAI API key is set")
        print("   - The MVP uses GPT-3.5-turbo for cost efficiency")
        print("   - Results are saved as JSON files for further processing")
    else:
        print("\n❌ Setup incomplete. Please check the errors above.")


if __name__ == "__main__":
    main() 