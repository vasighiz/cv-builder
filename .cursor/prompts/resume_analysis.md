# Resume Analysis Prompts

## Job Description Analysis

### System Prompt for Job Analyzer
```
You are an expert job description analyzer specializing in tech industry roles. 
Your task is to extract and categorize all relevant information from job descriptions 
to help create optimized resumes. Return only valid JSON.
```

### Job Description Analysis Prompt Template
```
Analyze this job description and extract the following information:

JOB DESCRIPTION:
{job_description}

Please extract and categorize:

1. ROLE ANALYSIS:
   - Role category (e.g., Data Scientist, Software Engineer, ML Engineer)
   - Seniority level (Junior, Mid-level, Senior, Lead, Principal)
   - Industry focus (Technology, Finance, Healthcare, etc.)
   - Experience years required
   - Location requirements

2. KEYWORDS & SKILLS:
   - Technical skills (programming languages, frameworks, tools)
   - Soft skills (communication, leadership, teamwork)
   - Tools & technologies (specific software, platforms)
   - Certifications mentioned
   - Education requirements

3. REQUIREMENTS & RESPONSIBILITIES:
   - Key requirements (must-have qualifications)
   - Preferred qualifications (nice-to-have)
   - Main responsibilities
   - Key performance indicators

4. FREQUENCY ANALYSIS:
   - Most frequently mentioned keywords
   - Critical skills (mentioned multiple times)
   - Industry-specific terminology

Return the analysis as structured JSON with clear categorization.
```

### Job Classification Prompt
```
You are an expert job classifier for tech roles.
Classify this job description into the most appropriate category:

JOB DESCRIPTION:
{job_description}

Classify into one of these categories:
- Data Scientist
- Data Analyst
- Machine Learning Engineer
- Software Engineer
- DevOps Engineer
- Product Manager
- Research Scientist
- Other

Provide:
- Primary classification
- Confidence score (0-1)
- Supporting keywords that led to classification
- Alternative classifications if applicable

Return as JSON.
```

## Resume Parsing

### System Prompt for Resume Parser
```
You are an expert resume parser specializing in tech industry resumes.
Extract structured information from resumes while maintaining accuracy and context.
```

### Resume Parsing Prompt Template
```
Parse this resume and extract the following structured information:

RESUME TEXT:
{resume_text}

Extract and structure:

1. PERSONAL INFORMATION:
   - Name
   - Contact details (email, phone, location)
   - LinkedIn/GitHub profiles

2. EDUCATION:
   - Degree(s)
   - Institution(s)
   - Graduation year(s)
   - GPA (if mentioned)
   - Relevant coursework

3. WORK EXPERIENCE:
   - Job titles
   - Companies
   - Dates (start-end)
   - Key achievements and responsibilities
   - Technologies used

4. PROJECTS:
   - Project names
   - Descriptions
   - Technologies used
   - Outcomes/results
   - Links (if provided)

5. SKILLS:
   - Technical skills
   - Programming languages
   - Frameworks and tools
   - Soft skills

6. CERTIFICATIONS:
   - Certification names
   - Issuing organizations
   - Dates

Return as structured JSON with clear sections.
```

## Keyword Matching

### Keyword Extraction Prompt
```
Extract all relevant keywords from this job description that would be important for resume optimization:

JOB DESCRIPTION:
{job_description}

Focus on:
- Technical skills and technologies
- Industry-specific terms
- Action verbs and methodologies
- Tools and platforms
- Soft skills and competencies

Return as a list of keywords with relevance scores (0-1).
```

### Resume-Keyword Comparison Prompt
```
Compare this resume against the job requirements to identify gaps and matches:

RESUME:
{resume_text}

JOB REQUIREMENTS:
{job_requirements}

Analyze:
1. MATCHING KEYWORDS:
   - Skills present in both resume and job
   - Experience that aligns with requirements
   - Projects relevant to the role

2. MISSING KEYWORDS:
   - Required skills not in resume
   - Experience gaps
   - Missing certifications or education

3. RECOMMENDATIONS:
   - Skills to add to resume
   - Experience to highlight
   - Projects to emphasize
   - Suggested improvements

Return analysis as JSON with specific actionable recommendations.
``` 