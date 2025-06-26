# Module 1 MVP: Job Description Analyzer

A simplified, working implementation of the Job Description Analyzer that extracts keywords and requirements from job descriptions using OpenAI's GPT models.

## 🚀 Quick Start

### 1. Setup
```bash
# Run the setup script
python setup_mvp.py
```

This will:
- Check Python version (3.8+ required)
- Install required dependencies
- Set up environment variables
- Create sample data
- Test the setup

### 2. Set OpenAI API Key
You need an OpenAI API key. You can:
- Add it to the `.env` file: `OPENAI_API_KEY=your_key_here`
- Set environment variable: `export OPENAI_API_KEY=your_key_here`
- Pass it directly to the analyzer

### 3. Test the MVP
```bash
# Test with sample job descriptions
python test_mvp.py

# Test with your own job description
python test_mvp.py custom
```

## 📁 Files Structure

```
src/modules/
├── job_analyzer_mvp.py    # Main MVP implementation
├── job_analyzer.py        # Full-featured version
├── keyword_matcher.py     # Module 2
└── section_generator.py   # Module 3

src/data/
├── samples/
│   └── sample_job_descriptions.json  # Sample job descriptions
└── keywords/
    └── master_keywords.json          # Master keyword lists

test_mvp.py               # Test script
setup_mvp.py              # Setup script
MVP_README.md             # This file
```

## 🔧 How It Works

### Core Features
1. **Keyword Extraction**: Uses GPT-3.5-turbo to extract:
   - Technical skills (Python, SQL, etc.)
   - Soft skills (Communication, Leadership, etc.)
   - Tools & Technologies (AWS, Docker, etc.)
   - Responsibilities and Requirements

2. **Role Classification**: Identifies:
   - Job category (Data Scientist, Software Engineer, etc.)
   - Seniority level (Junior, Senior, etc.)
   - Industry focus (AI/ML, Web Development, etc.)
   - Required experience level

3. **Insights Generation**: Provides:
   - Keyword frequency analysis
   - Skill categorization
   - Recommendations for resume optimization

### Example Output
```json
{
  "keywords": {
    "technical_skills": ["Python", "Machine Learning", "SQL", "TensorFlow"],
    "soft_skills": ["Communication", "Problem Solving", "Teamwork"],
    "tools_technologies": ["AWS", "Docker", "Git", "Jupyter"],
    "responsibilities": ["Model Development", "Data Processing"],
    "requirements": ["5+ years experience", "Master's degree"],
    "keywords_frequency": {"Python": 3, "Machine Learning": 2}
  },
  "role_analysis": {
    "role_category": "Data Scientist",
    "seniority_level": "Senior",
    "industry_focus": "AI/ML",
    "experience_years": "5+ years"
  },
  "insights": {
    "total_technical_skills": 4,
    "total_soft_skills": 3,
    "most_frequent_keywords": [["Python", 3], ["Machine Learning", 2]]
  },
  "recommendations": [
    "📝 Add more technical skills to improve keyword coverage",
    "🛠️  Include relevant tools and technologies in your resume",
    "👑 Emphasize leadership and project management experience"
  ]
}
```

## 🧪 Testing

### Sample Job Descriptions
The MVP includes sample job descriptions for:
- Data Scientist
- Software Engineer
- Machine Learning Engineer
- Data Analyst
- AI Engineer

### Custom Testing
You can test with your own job descriptions:
```bash
python test_mvp.py custom
```

## 💡 Usage Examples

### Basic Usage
```python
from src.modules.job_analyzer_mvp import JobDescriptionAnalyzerMVP

# Initialize analyzer
analyzer = JobDescriptionAnalyzerMVP(api_key="your_openai_api_key")

# Analyze job description
job_description = "Your job description here..."
analysis = analyzer.analyze_job_description(job_description)

# Print summary
analyzer.print_analysis_summary(analysis)

# Save results
analyzer.save_analysis(analysis, "my_analysis.json")
```

### Integration with Other Modules
The output from this MVP can be used as input for:
- **Module 2**: Resume Keyword Matcher (gap analysis)
- **Module 3**: Resume Sections Generator (content creation)

## 🔄 Next Steps

After testing this MVP:

1. **Test with real job descriptions** from your target companies
2. **Review the extracted keywords** for accuracy and completeness
3. **Move to Module 2** (Keyword Matcher) to compare against your resume
4. **Move to Module 3** (Section Generator) to create optimized content

## 🛠️ Technical Details

### Dependencies
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management

### Model Used
- **GPT-3.5-turbo**: Cost-effective model for MVP testing
- **Temperature**: 0.2-0.3 for consistent results
- **Max tokens**: 1000-1500 for comprehensive analysis

### Error Handling
- Graceful handling of API errors
- Fallback to empty structures on failure
- Clear error messages for debugging

## 📊 Performance

### Typical Response Time
- 2-5 seconds per job description
- Depends on job description length and API response time

### Cost Estimation
- ~$0.01-0.03 per job description analysis
- Uses GPT-3.5-turbo for cost efficiency

### Accuracy
- High accuracy for technical skills extraction
- Good role classification for common tech roles
- May need refinement for specialized roles

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ❌ OPENAI_API_KEY environment variable not set!
   ```
   **Solution**: Set your OpenAI API key in `.env` file or environment variable

2. **Import Error**
   ```
   ModuleNotFoundError: No module named 'openai'
   ```
   **Solution**: Run `pip install openai python-dotenv`

3. **JSON Parsing Error**
   ```
   json.decoder.JSONDecodeError
   ```
   **Solution**: Check if the job description is too long or contains special characters

### Debug Mode
Add debug prints to see API responses:
```python
# In job_analyzer_mvp.py, add print statements
print(f"API Response: {content}")
```

## 📈 Future Enhancements

### Planned Improvements
- Support for PDF/Word document input
- Enhanced role classification
- Keyword relevance scoring
- Industry-specific keyword databases
- Batch processing for multiple job descriptions

### Integration Features
- Web interface using Streamlit
- Database storage for analysis history
- Export to various formats (CSV, Excel)
- API endpoint for integration

---

**Ready to test?** Run `python setup_mvp.py` to get started! 