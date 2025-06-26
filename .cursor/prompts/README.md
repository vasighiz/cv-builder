# Cursor Prompts Collection

A comprehensive collection of effective AI prompts organized for reuse across projects. This directory contains carefully crafted prompts for various development tasks, from resume building to general software development.

## 📁 Directory Structure

```
.cursor/prompts/
├── README.md                    # This file - overview and usage guide
├── resume_analysis.md           # Job description analysis and resume parsing
├── resume_generation.md         # Resume section generation and optimization
├── ats_optimization.md          # ATS compliance and formatting
└── general_ai_prompts.md        # General development and project management
```

## 🎯 Prompt Categories

### 1. Resume Analysis (`resume_analysis.md`)
Specialized prompts for analyzing job descriptions and parsing resumes:
- **Job Description Analysis**: Extract keywords, requirements, and role information
- **Resume Parsing**: Convert unstructured resume text to structured data
- **Keyword Matching**: Compare resume content against job requirements
- **Job Classification**: Categorize roles and determine seniority levels

### 2. Resume Generation (`resume_generation.md`)
Prompts for creating compelling resume content:
- **Professional Summary**: Generate targeted summaries highlighting relevant expertise
- **Skills Section**: Optimize skills presentation for ATS and human readers
- **Experience Bullets**: Create impactful, quantifiable achievement statements
- **Project Descriptions**: Rewrite projects to showcase relevant skills
- **Domain Analysis**: Extract and highlight relevant domain expertise

### 3. ATS Optimization (`ats_optimization.md`)
Prompts for ensuring resumes pass automated screening:
- **ATS Compliance**: Check formatting and structure compliance
- **Keyword Optimization**: Analyze and improve keyword density and placement
- **Structure Optimization**: Optimize section order and content prioritization
- **Quality Assurance**: Comprehensive review and final polish

### 4. General AI Prompts (`general_ai_prompts.md`)
Reusable prompts for general development tasks:
- **Code Review**: Comprehensive code analysis and improvement suggestions
- **Testing**: Test case generation and bug analysis
- **Project Management**: Planning, requirements analysis, and documentation
- **Problem Solving**: Technical problem analysis and performance optimization
- **Learning**: Code explanation and skill assessment

## 🚀 How to Use These Prompts

### Basic Usage
1. **Copy the prompt template** from the relevant file
2. **Replace placeholder variables** with your specific content
3. **Customize the prompt** for your specific use case
4. **Use with your preferred AI model** (GPT-4, Claude, etc.)

### Example Usage

```python
# Example: Using a resume analysis prompt
from .cursor.prompts.resume_analysis import job_analysis_prompt

job_description = "Senior Data Scientist position..."
formatted_prompt = job_analysis_prompt.format(
    job_description=job_description
)

# Send to AI model
response = ai_model.generate(formatted_prompt)
```

### Template Variables
Most prompts use template variables in `{curly_braces}`. Common variables include:
- `{job_description}` - The job posting text
- `{resume_text}` - The candidate's resume content
- `{code}` - Code to be analyzed or documented
- `{language}` - Programming language context
- `{requirements}` - Job requirements or project requirements

## 📝 Prompt Design Principles

### 1. Specificity
- Clear, detailed instructions
- Specific output formats
- Contextual information provided

### 2. Structure
- Consistent formatting
- Logical organization
- Easy to scan and modify

### 3. Reusability
- Template-based design
- Modular components
- Cross-project applicability

### 4. Effectiveness
- Proven results from resume builder project
- Industry best practices
- ATS optimization focus

## 🔧 Customizing Prompts

### Adding New Prompts
1. **Choose the appropriate file** based on category
2. **Follow the existing format** and structure
3. **Include template variables** for flexibility
4. **Add clear descriptions** and usage examples
5. **Test the prompt** with real data

### Modifying Existing Prompts
1. **Maintain the core structure** for consistency
2. **Update template variables** as needed
3. **Add context-specific instructions**
4. **Test modifications** thoroughly

### Best Practices
- **Keep prompts focused** on specific tasks
- **Use clear, professional language**
- **Include examples** where helpful
- **Maintain consistent formatting**
- **Document any special requirements**

## 📊 Prompt Effectiveness Tracking

### Metrics to Monitor
- **Response quality** - How well the AI follows instructions
- **Consistency** - Similar inputs produce similar outputs
- **Completeness** - All required information is included
- **Accuracy** - Output matches expected format and content

### Improvement Process
1. **Test prompts** with various inputs
2. **Collect feedback** on output quality
3. **Iterate and refine** based on results
4. **Document successful patterns**
5. **Share improvements** with team

## 🛠️ Integration with Projects

### Resume Builder Integration
These prompts are specifically designed for the resume builder project:
- **Module 1**: Use job analysis prompts
- **Module 2**: Use keyword matching prompts
- **Module 3**: Use section generation prompts
- **Module 5**: Use ATS optimization prompts

### Other Project Integration
- **Code Review**: Use general AI prompts for code analysis
- **Documentation**: Use technical writing prompts
- **Testing**: Use test generation prompts
- **Project Planning**: Use project management prompts

## 📚 Learning Resources

### Understanding Prompt Engineering
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Microsoft Prompt Engineering Best Practices](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering)

### Resume Writing Resources
- [ATS Optimization Guide](https://www.indeed.com/career-advice/resumes-cover-letters/ats-resume)
- [Resume Writing Best Practices](https://www.linkedin.com/advice/0/how-do-you-write-effective-resume-bullet-points)
- [Technical Resume Examples](https://github.com/resume/resume.github.com)

## 🤝 Contributing

### Adding New Prompts
1. **Identify a gap** in the current collection
2. **Create a new prompt** following the established format
3. **Test thoroughly** with real use cases
4. **Document usage** and examples
5. **Submit for review**

### Improving Existing Prompts
1. **Identify areas for improvement**
2. **Propose specific changes**
3. **Test modifications**
4. **Update documentation**
5. **Share results**

### Feedback and Suggestions
- **Report issues** with specific prompts
- **Suggest improvements** based on usage
- **Share successful modifications**
- **Contribute new categories** of prompts

## 📄 License and Usage

These prompts are designed for internal use and project development. Feel free to:
- **Use in your projects**
- **Modify for specific needs**
- **Share with team members**
- **Contribute improvements**

## 🔄 Version History

### v1.0.0 (Current)
- Initial prompt collection
- Resume builder specific prompts
- General development prompts
- ATS optimization focus
- Comprehensive documentation

### Future Enhancements
- **More specialized prompts** for different industries
- **Multi-language support** for international projects
- **Integration examples** for popular frameworks
- **Automated prompt testing** and validation
- **Community prompt sharing** platform

---

**Note**: These prompts are living documents. Update them based on your experience and the evolving needs of your projects. Regular review and refinement will ensure they remain effective and relevant. 