# Quick Reference Guide

## 🚀 Most Used Prompts

### Resume Analysis
```markdown
**Job Description Analysis**
System: "You are an expert job description analyzer specializing in tech industry roles. Return only valid JSON."

Prompt: "Analyze this job description and extract: role category, seniority level, technical skills, soft skills, requirements, responsibilities. Return as structured JSON."

**Resume Parsing**
System: "You are an expert resume parser specializing in tech industry resumes."

Prompt: "Parse this resume and extract: personal info, education, work experience, projects, skills, certifications. Return as structured JSON."
```

### Resume Generation
```markdown
**Professional Summary**
System: "You are an expert resume writer specializing in creating compelling professional summaries that highlight ALL relevant domain expertise."

Prompt: "Create a 3-4 sentence professional summary for {role} position. Include: experience level, key skills, domain expertise, and value proposition. Focus on {job_requirements}."

**Skills Section**
System: "You are an expert resume writer specializing in tech industry skills optimization."

Prompt: "Generate ATS-friendly skills section for {job_title}. Categorize: Programming Languages, Frameworks, Tools, Soft Skills. Prioritize skills relevant to {job_requirements}."

**Experience Bullets**
System: "You are an expert resume writer creating impactful work experience bullet points."

Prompt: "Create 3-5 bullet points for {job_title} at {company}. Include: action verbs, quantifiable results, relevant keywords from {job_requirements}. Format: '• [Action] [what] [how] [result]'"
```

### ATS Optimization
```markdown
**ATS Compliance Check**
System: "You are an expert ATS compliance specialist."

Prompt: "Check this resume for ATS compliance: standard fonts, no tables/columns, proper headers, keyword optimization, quantifiable achievements. Provide score (0-100) and specific improvements."

**Keyword Integration**
System: "You are an expert ATS optimization specialist."

Prompt: "Integrate these keywords naturally into resume sections: {keywords}. Focus on: summary (3-5 keywords), experience bullets, skills section. Avoid keyword stuffing."
```

### Code Review
```markdown
**Code Review**
System: "You are an expert software engineer and code reviewer."

Prompt: "Review this {language} code for: code quality, best practices, maintainability, potential issues. Provide: assessment (1-10), specific issues, improvement suggestions, code examples."

**Documentation**
System: "You are an expert technical writer."

Prompt: "Generate documentation for this {language} code: function purpose, parameters, return values, usage examples, edge cases."
```

## 📋 Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{job_description}` | Full job posting text | "Senior Data Scientist position..." |
| `{resume_text}` | Candidate's resume content | "John Doe\nSoftware Engineer..." |
| `{job_requirements}` | Key job requirements | "Python, ML, AWS, 5+ years" |
| `{role}` | Job title/role | "Data Scientist" |
| `{job_title}` | Specific job title | "Senior ML Engineer" |
| `{company}` | Company name | "Google" |
| `{code}` | Code to analyze | "def process_data():" |
| `{language}` | Programming language | "Python" |
| `{framework}` | Framework/technology | "React" |

## ⚡ Quick Start Examples

### 1. Analyze Job Description
```python
prompt = """
You are an expert job description analyzer specializing in tech industry roles. Return only valid JSON.

Analyze this job description and extract the following information:

JOB DESCRIPTION:
{job_description}

Please extract and categorize:
1. ROLE ANALYSIS: role category, seniority level, industry focus, experience years
2. KEYWORDS & SKILLS: technical skills, soft skills, tools & technologies
3. REQUIREMENTS & RESPONSIBILITIES: key requirements, main responsibilities
4. FREQUENCY ANALYSIS: most mentioned keywords, critical skills

Return the analysis as structured JSON with clear categorization.
"""

# Usage
formatted_prompt = prompt.format(job_description="Senior Data Scientist...")
```

### 2. Generate Professional Summary
```python
prompt = """
You are an expert resume writer specializing in creating compelling professional summaries.

Create a compelling professional summary for a resume that matches this job description.

JOB INFORMATION:
- Role: {role}
- Seniority: {seniority}
- Experience Required: {experience_years}

JOB REQUIREMENTS: {requirements}

Create a professional summary that:
1. Opens with role and experience level
2. Highlights relevant domain expertise
3. Shows passion and interest in relevant domains
4. Connects background to job requirements
5. Uses professional, confident tone
6. Is 3-4 sentences maximum

Return ONLY the summary text, no additional formatting.
"""

# Usage
formatted_prompt = prompt.format(
    role="Data Scientist",
    seniority="Senior",
    experience_years="5+ years",
    requirements="Python, ML, AWS, SQL"
)
```

### 3. ATS Compliance Check
```python
prompt = """
You are an expert ATS compliance specialist.

Analyze this resume for ATS compliance and provide optimization recommendations:

RESUME TEXT:
{resume_text}

TARGET JOB KEYWORDS:
{job_keywords}

Check for:
1. FORMATTING COMPLIANCE: standard fonts, no tables/columns, proper headers
2. KEYWORD OPTIMIZATION: presence of required keywords, natural integration
3. CONTENT QUALITY: quantifiable achievements, action verbs, industry terminology

Provide:
- Overall ATS compliance score (0-100)
- Specific issues found
- Optimization recommendations
- Keyword gap analysis

Return as structured analysis with actionable improvements.
"""

# Usage
formatted_prompt = prompt.format(
    resume_text="John Doe\nSoftware Engineer...",
    job_keywords="Python, React, AWS, SQL"
)
```

## 🎯 Best Practices

### 1. System Prompts
- **Be specific** about the AI's role and expertise
- **Set clear expectations** for output format
- **Include constraints** (e.g., "Return only valid JSON")

### 2. User Prompts
- **Provide context** and background information
- **Use structured format** with clear sections
- **Include examples** where helpful
- **Specify output requirements** clearly

### 3. Template Variables
- **Use descriptive names** for variables
- **Provide examples** in documentation
- **Validate inputs** before formatting
- **Handle missing values** gracefully

### 4. Testing Prompts
- **Test with various inputs** to ensure robustness
- **Validate output format** and quality
- **Iterate based on results**
- **Document successful patterns**

## 🔧 Customization Tips

### Adding Context
```python
# Add more context for better results
prompt = prompt.format(
    job_description=job_description,
    industry="Technology",  # Additional context
    company_size="Large",   # Additional context
    location="Remote"       # Additional context
)
```

### Adjusting Output Format
```python
# Modify output requirements
prompt = prompt.replace(
    "Return as structured JSON",
    "Return as structured JSON with relevance scores (0-1)"
)
```

### Combining Prompts
```python
# Combine multiple prompts for complex tasks
analysis_prompt = job_analysis_prompt.format(job_description=jd)
summary_prompt = summary_prompt.format(
    analysis_result=analysis_prompt,
    candidate_info=candidate_info
)
```

## 📊 Effectiveness Metrics

### Quality Indicators
- **Completeness**: All required information included
- **Accuracy**: Output matches expected format
- **Relevance**: Content aligns with job requirements
- **Readability**: Clear, professional language

### Optimization Targets
- **ATS Score**: 85+ for automated screening
- **Keyword Coverage**: 90%+ of required keywords
- **Response Time**: <30 seconds for generation
- **Consistency**: Similar inputs produce similar outputs

---

**Pro Tip**: Start with these quick reference prompts and gradually customize them for your specific needs. The more you use them, the better you'll understand how to optimize them for your use cases. 