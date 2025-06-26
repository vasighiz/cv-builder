# ATS Optimization Prompts

## ATS Compliance Checking

### System Prompt for ATS Checker
```
You are an expert ATS (Applicant Tracking System) compliance specialist.
Analyze resumes for formatting, structure, and keyword optimization to ensure they pass automated screening.
```

### ATS Compliance Analysis Prompt
```
Analyze this resume for ATS compliance and provide optimization recommendations:

RESUME TEXT:
{resume_text}

TARGET JOB KEYWORDS:
{job_keywords}

Check for:

1. FORMATTING COMPLIANCE:
   - Standard fonts (Arial, Times New Roman, Calibri)
   - Appropriate font size (11-12pt)
   - No tables, columns, or complex formatting
   - No headers/footers
   - No symbols or special characters
   - Consistent margins (0.5"-1")

2. STRUCTURE COMPLIANCE:
   - Standard section headings
   - Contact information properly formatted
   - Date formats (MM/YYYY or Month YYYY)
   - Bullet points using standard characters
   - No images or graphics

3. KEYWORD OPTIMIZATION:
   - Presence of required job keywords
   - Keyword placement in relevant sections
   - Natural keyword integration
   - No keyword stuffing

4. CONTENT QUALITY:
   - Quantifiable achievements
   - Action verbs
   - Industry-specific terminology
   - Clear, concise language

Provide:
- Overall ATS compliance score (0-100)
- Specific issues found
- Optimization recommendations
- Keyword gap analysis
- Formatting suggestions

Return as structured analysis with actionable improvements.
```

### ATS-Friendly Formatting Prompt
```
Convert this resume to ATS-friendly format:

ORIGINAL RESUME:
{original_resume}

Apply these ATS-friendly formatting rules:

1. FONT & TYPEFACE:
   - Use Arial, Times New Roman, or Calibri
   - Size 11-12pt for body text
   - 14-16pt for section headers
   - No decorative fonts

2. LAYOUT:
   - Single column layout
   - No tables or columns
   - No headers or footers
   - 0.5"-1" margins
   - Left alignment for all text

3. SECTION HEADERS:
   - Use standard headers: "Contact Information", "Professional Summary", "Work Experience", "Education", "Skills", "Projects"
   - Bold formatting only
   - No special characters

4. CONTACT INFORMATION:
   - Name (larger font, bold)
   - Email, phone, location on separate lines
   - LinkedIn/GitHub URLs as plain text

5. BULLET POINTS:
   - Use standard bullet points (•)
   - No special symbols
   - Consistent indentation

6. DATES:
   - Format: "Month YYYY - Month YYYY" or "MM/YYYY - MM/YYYY"
   - Consistent throughout

Return the reformatted resume with ATS-friendly formatting.
```

## Keyword Optimization

### Keyword Density Analysis Prompt
```
Analyze keyword density and placement in this resume:

RESUME TEXT:
{resume_text}

TARGET KEYWORDS:
{target_keywords}

Analyze:

1. KEYWORD PRESENCE:
   - Which keywords are present
   - Which keywords are missing
   - Keyword frequency in each section

2. KEYWORD PLACEMENT:
   - Strategic placement in summary
   - Integration in experience bullets
   - Presence in skills section
   - Natural language flow

3. KEYWORD VARIATIONS:
   - Synonyms and related terms
   - Industry-specific terminology
   - Abbreviations and acronyms

4. OPTIMIZATION OPPORTUNITIES:
   - Missing critical keywords
   - Underutilized keywords
   - Keyword stuffing issues
   - Natural integration suggestions

Provide:
- Keyword coverage percentage
- Missing critical keywords
- Placement recommendations
- Natural integration suggestions
- Overall keyword optimization score

Return as detailed analysis with specific recommendations.
```

### Keyword Integration Prompt
```
Integrate these keywords naturally into the resume sections:

RESUME SECTIONS:
{resume_sections}

KEYWORDS TO INTEGRATE:
{keywords_to_integrate}

TARGET JOB CONTEXT:
{job_context}

Integrate keywords by:

1. PROFESSIONAL SUMMARY:
   - Include 3-5 most important keywords
   - Use natural language flow
   - Connect to experience level

2. WORK EXPERIENCE:
   - Incorporate keywords into bullet points
   - Use action verbs with keywords
   - Show application of skills

3. SKILLS SECTION:
   - Group related keywords
   - Use industry-standard terminology
   - Include variations and synonyms

4. PROJECTS SECTION:
   - Highlight relevant technologies
   - Show practical application
   - Connect to job requirements

Guidelines:
- Use keywords naturally, not forced
- Maintain readability and flow
- Focus on relevance to job
- Avoid keyword stuffing
- Use industry-standard terms

Return optimized sections with integrated keywords.
```

## Resume Structure Optimization

### Section Order Optimization Prompt
```
Optimize the section order for ATS and human readers:

CURRENT SECTIONS:
{current_sections}

TARGET JOB:
{target_job}

CANDIDATE PROFILE:
{candidate_profile}

Optimize section order based on:

1. ATS PRIORITY:
   - Contact Information (always first)
   - Professional Summary (high impact)
   - Work Experience (most important)
   - Skills (keyword-rich)
   - Education
   - Projects/Certifications

2. CANDIDATE STRENGTHS:
   - Lead with strongest qualifications
   - Highlight relevant experience
   - Show progression and growth
   - Address job requirements early

3. INDUSTRY STANDARDS:
   - Follow industry conventions
   - Consider role seniority
   - Adapt to job requirements
   - Include relevant sections

4. READER ENGAGEMENT:
   - Hook with strong summary
   - Show value proposition
   - Demonstrate fit early
   - End with supporting details

Provide:
- Recommended section order
- Rationale for each placement
- Content suggestions for each section
- ATS optimization notes

Return optimized structure with explanations.
```

### Content Prioritization Prompt
```
Prioritize content within each section for maximum impact:

RESUME CONTENT:
{resume_content}

TARGET JOB REQUIREMENTS:
{job_requirements}

Prioritize content by:

1. RELEVANCE TO JOB:
   - Most relevant experience first
   - Aligned skills prominently placed
   - Matching projects highlighted
   - Required qualifications emphasized

2. IMPACT AND ACHIEVEMENTS:
   - Quantifiable results first
   - High-impact projects prioritized
   - Leadership experience highlighted
   - Innovation and problem-solving shown

3. RECENCY AND PROGRESSION:
   - Recent experience first
   - Career progression shown
   - Growth and development demonstrated
   - Current skills emphasized

4. ATS OPTIMIZATION:
   - Keywords in first bullet points
   - Important terms in section headers
   - Relevant experience prominently placed
   - Required skills easily scannable

Guidelines:
- Lead with strongest qualifications
- Show progression and growth
- Highlight transferable skills
- Demonstrate fit for role
- Maintain logical flow

Return prioritized content with rationale for each decision.
```

## Quality Assurance

### Resume Quality Check Prompt
```
Perform a comprehensive quality check on this resume:

RESUME TEXT:
{resume_text}

TARGET JOB:
{target_job}

Check for:

1. CONTENT QUALITY:
   - Grammar and spelling
   - Professional tone
   - Clarity and conciseness
   - Consistency in formatting
   - Logical flow and structure

2. IMPACT AND ACHIEVEMENTS:
   - Quantifiable results
   - Strong action verbs
   - Specific accomplishments
   - Business impact shown
   - Problem-solving demonstrated

3. RELEVANCE AND FIT:
   - Alignment with job requirements
   - Appropriate experience level
   - Relevant skills highlighted
   - Industry knowledge shown
   - Cultural fit indicators

4. TECHNICAL ACCURACY:
   - Correct technology names
   - Accurate job titles
   - Proper company names
   - Valid dates and durations
   - Consistent terminology

5. COMPLETENESS:
   - All required sections present
   - Contact information complete
   - Experience gaps explained
   - Education details included
   - Relevant certifications listed

Provide:
- Overall quality score (0-100)
- Specific issues found
- Improvement recommendations
- Content suggestions
- Final polish recommendations

Return comprehensive quality analysis with actionable feedback.
```

### Final Review Prompt
```
Perform final review before submission:

RESUME:
{resume}

TARGET JOB:
{target_job}

Final checklist:

1. TECHNICAL COMPLIANCE:
   - ATS-friendly formatting
   - Keyword optimization
   - Proper file format
   - Correct file naming

2. CONTENT EXCELLENCE:
   - Professional summary compelling
   - Experience bullets impactful
   - Skills relevant and comprehensive
   - Projects showcase abilities
   - Education properly presented

3. JOB ALIGNMENT:
   - Requirements addressed
   - Skills match job needs
   - Experience relevant
   - Culture fit indicators
   - Growth potential shown

4. READABILITY:
   - Clear and concise
   - Professional tone
   - Logical structure
   - Easy to scan
   - Engaging content

5. COMPLETENESS:
   - All sections included
   - Contact information complete
   - No missing details
   - Consistent formatting
   - Professional appearance

Provide:
- Final approval or issues
- Last-minute improvements
- Submission readiness score
- Confidence level
- Any final recommendations

Return final review with go/no-go decision.
``` 