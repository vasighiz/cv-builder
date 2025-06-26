# Resume Generation Prompts

## Professional Summary Generation

### System Prompt for Summary Writer
```
You are an expert resume writer specializing in creating compelling professional summaries 
that highlight ALL relevant domain expertise and skills that match the specific job requirements.
```

### Professional Summary Prompt Template
```
Create a compelling professional summary for a resume that matches this job description.

JOB INFORMATION:
- Role: {role_category}
- Seniority: {seniority_level}
- Industry: {industry_focus}
- Experience Required: {experience_years}

JOB REQUIREMENTS: {requirements}
JOB RESPONSIBILITIES: {responsibilities}

CANDIDATE INFORMATION:
- Experience Years: {experience_years} years
- Education: {education}
- Top Technical Skills: {technical_skills}
- Key Tools: {tools}
- Is Research Role: {is_research_role}
- PhD Required: {has_phd}
- Has Publications: {has_publications}

DOMAIN ANALYSIS:
- Job Domains: {job_domains}
- Candidate Domains: {candidate_domains}
- Matching Domains: {matching_domains}
- Key Projects: {relevant_projects}
- Domain-Specific Skills: {domain_skills}

Create a professional summary that:
1. Opens with role and experience level
2. HIGHLIGHTS ALL RELEVANT DOMAIN EXPERTISE that matches the job requirements
3. Mentions specific qualifications if required (PhD, research experience, publications)
4. Shows passion and interest in the specific domains/fields relevant to this job
5. Connects candidate's background to job requirements
6. Uses professional, confident tone
7. Is 3-4 sentences maximum

IMPORTANT: Focus on the domains and skills that are MOST RELEVANT to this specific job. 
Don't limit to just one domain - highlight ALL relevant expertise areas.

Return ONLY the summary text, no additional formatting.
```

## Skills Section Generation

### System Prompt for Skills Optimizer
```
You are an expert resume writer specializing in tech industry skills optimization.
Create comprehensive, well-categorized skills sections that pass ATS filters.
```

### Skills Section Prompt Template
```
Generate an optimized skills section for a resume targeting this job:

JOB REQUIREMENTS:
{job_requirements}

CANDIDATE SKILLS:
{candidate_skills}

PROJECT TECHNOLOGIES:
{project_technologies}

Create a skills section that:
1. Categorizes skills logically (Programming Languages, Frameworks, Tools, etc.)
2. Prioritizes skills most relevant to the job
3. Includes both technical and soft skills
4. Uses industry-standard terminology
5. Avoids generic terms that don't add value
6. Ensures ATS compatibility

Categories to use:
- Programming Languages
- Frameworks & Libraries
- AI/ML Technologies
- Cloud & Infrastructure
- Databases & Storage
- Tools & Platforms
- Soft Skills

Return formatted skills section with clear categories.
```

## Experience Section Generation

### System Prompt for Experience Writer
```
You are an expert resume writer creating impactful work experience bullet points.
Focus on quantifiable achievements and relevant keywords for ATS optimization.
```

### Experience Bullet Points Prompt Template
```
Generate optimized work experience bullet points for this role:

JOB TITLE: {job_title}
COMPANY: {company}
DATES: {dates}

ORIGINAL EXPERIENCE:
{original_experience}

JOB REQUIREMENTS:
{job_requirements}

KEYWORDS TO INCLUDE:
{target_keywords}

Create bullet points that:
1. Start with strong action verbs
2. Include quantifiable results (%, $, #, metrics)
3. Incorporate relevant job keywords naturally
4. Focus on achievements, not just responsibilities
5. Use industry-specific terminology
6. Keep each bullet to 1-2 lines maximum
7. Highlight transferable skills

Format: "• [Action verb] [what you did] [how you did it] [quantifiable result]"

Return 3-5 optimized bullet points.
```

## Project Section Generation

### System Prompt for Project Writer
```
You are an expert resume writer creating compelling project descriptions.
Highlight technical skills, methodologies, and quantifiable outcomes.
```

### Project Description Prompt Template
```
Rewrite this project description to be more compelling for the target job:

PROJECT NAME: {project_name}
ORIGINAL DESCRIPTION: {original_description}
TECHNOLOGIES USED: {technologies}

TARGET JOB REQUIREMENTS:
{job_requirements}

Create a project description that:
1. Opens with a compelling hook about the problem solved
2. Highlights relevant technical skills and methodologies
3. Includes quantifiable outcomes and metrics
4. Shows impact and business value
5. Uses industry-relevant terminology
6. Demonstrates problem-solving abilities
7. Connects to the target role's requirements

Structure:
- Problem/Challenge
- Technical approach
- Technologies used
- Results/Outcomes
- Impact/Value

Return a 2-3 sentence optimized project description.
```

## Domain Expertise Analysis

### Domain Analysis Prompt Template
```
Analyze this job description and CV to identify ALL relevant domains, keywords, and expertise areas.

JOB DESCRIPTION:
{job_text}

CANDIDATE CV:
{cv_text}

Extract and categorize the following:

1. TECHNICAL DOMAINS (e.g., Machine Learning, Data Science, Software Engineering, etc.)
2. INDUSTRY DOMAINS (e.g., Biology, Finance, Healthcare, E-commerce, etc.)
3. APPLICATION AREAS (e.g., Drug Discovery, Fraud Detection, Customer Analytics, etc.)
4. METHODOLOGIES (e.g., Research, Development, Analysis, etc.)
5. SPECIFIC TECHNOLOGIES/SKILLS mentioned in both job and CV

For each domain/keyword, provide:
- Relevance score (0-1) based on how important it is for the job
- Whether it appears in both job and CV (matching)
- Specific examples from the data

Return as JSON:
{
    "job_domains": [{"domain": "string", "relevance": float, "examples": ["string"]}],
    "candidate_domains": [{"domain": "string", "relevance": float, "examples": ["string"]}],
    "matching_domains": [{"domain": "string", "relevance": float, "job_examples": ["string"], "cv_examples": ["string"]}],
    "relevant_projects": ["project_name"],
    "domain_skills": ["skill1", "skill2"]
}

Focus on identifying ALL relevant areas, not just one domain. Be comprehensive.
```

## Education & Certifications

### Education Section Prompt
```
Generate an optimized education section for this candidate:

EDUCATION DATA:
{education_data}

TARGET JOB:
{job_requirements}

Create an education section that:
1. Highlights relevant degrees and coursework
2. Includes GPA if above 3.0
3. Mentions relevant academic projects
4. Shows progression and achievements
5. Connects education to job requirements

Format: "Degree | Institution | Year | GPA (if applicable)"
```

### Certification Recommendations Prompt
```
Based on the skill gaps identified, suggest relevant certifications:

MISSING SKILLS:
{missing_skills}

CANDIDATE BACKGROUND:
{candidate_background}

TARGET ROLE:
{target_role}

Suggest certifications that:
1. Address the most critical skill gaps
2. Are recognized in the industry
3. Provide practical value
4. Are achievable within reasonable time
5. Align with career goals

For each suggestion, include:
- Certification name
- Issuing organization
- Relevance to missing skills
- Estimated time to complete
- Cost (if known)

Return as structured recommendations.
``` 