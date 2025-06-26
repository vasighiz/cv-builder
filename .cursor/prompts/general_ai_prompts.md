# General AI Prompts

## Code Review & Analysis

### System Prompt for Code Reviewer
```
You are an expert software engineer and code reviewer with extensive experience in multiple programming languages and best practices.
Provide thorough, constructive feedback that improves code quality, maintainability, and performance.
```

### Code Review Prompt Template
```
Review this code for quality, best practices, and potential improvements:

CODE:
```{language}
{code}
```

CONTEXT:
- Language: {language}
- Framework: {framework}
- Purpose: {purpose}
- Experience level: {experience_level}

Review for:

1. CODE QUALITY:
   - Readability and clarity
   - Naming conventions
   - Code organization
   - DRY principles
   - Single responsibility

2. BEST PRACTICES:
   - Language-specific conventions
   - Design patterns
   - Error handling
   - Performance considerations
   - Security concerns

3. MAINTAINABILITY:
   - Documentation
   - Comments
   - Modularity
   - Testability
   - Future extensibility

4. POTENTIAL ISSUES:
   - Bugs or edge cases
   - Performance bottlenecks
   - Security vulnerabilities
   - Scalability concerns
   - Compatibility issues

Provide:
- Overall assessment (1-10)
- Specific issues found
- Improvement suggestions
- Code examples for fixes
- Best practice recommendations

Return structured feedback with actionable improvements.
```

### Code Documentation Prompt
```
Generate comprehensive documentation for this code:

CODE:
```{language}
{code}
```

Generate:

1. FUNCTION/METHOD DOCUMENTATION:
   - Purpose and functionality
   - Parameters and return values
   - Usage examples
   - Edge cases and limitations

2. CLASS/MODULE DOCUMENTATION:
   - Overview and purpose
   - Dependencies
   - Usage patterns
   - Configuration options

3. API DOCUMENTATION (if applicable):
   - Endpoints and methods
   - Request/response formats
   - Authentication requirements
   - Error handling

4. README CONTENT:
   - Installation instructions
   - Usage examples
   - Configuration options
   - Troubleshooting guide

Use clear, concise language and include practical examples.
```

## Testing & Quality Assurance

### Test Case Generation Prompt
```
Generate comprehensive test cases for this code:

CODE:
```{language}
{code}
```

Generate test cases for:

1. UNIT TESTS:
   - Happy path scenarios
   - Edge cases
   - Error conditions
   - Boundary values
   - Invalid inputs

2. INTEGRATION TESTS:
   - Component interactions
   - Data flow
   - External dependencies
   - Error propagation

3. PERFORMANCE TESTS:
   - Load testing scenarios
   - Stress testing
   - Memory usage
   - Response times

4. SECURITY TESTS:
   - Input validation
   - Authentication
   - Authorization
   - Data protection

Include:
- Test descriptions
- Input data
- Expected outputs
- Test setup requirements
- Assertion criteria

Return structured test cases with clear instructions.
```

### Bug Analysis Prompt
```
Analyze this bug report and provide debugging guidance:

BUG REPORT:
{bug_report}

CODE CONTEXT:
{code_context}

Analyze:

1. BUG CLASSIFICATION:
   - Type of bug (logic, syntax, runtime, etc.)
   - Severity level
   - Impact assessment
   - Reproduction steps

2. ROOT CAUSE ANALYSIS:
   - Likely causes
   - Contributing factors
   - Code areas to investigate
   - Related components

3. DEBUGGING STRATEGY:
   - Investigation steps
   - Tools to use
   - Logging suggestions
   - Test scenarios

4. FIX RECOMMENDATIONS:
   - Potential solutions
   - Code changes needed
   - Testing requirements
   - Prevention measures

Provide:
- Detailed analysis
- Step-by-step debugging guide
- Code fix suggestions
- Prevention strategies
- Testing recommendations

Return comprehensive debugging guidance.
```

## Project Management

### Project Planning Prompt
```
Help plan this software project:

PROJECT DESCRIPTION:
{project_description}

TECHNICAL REQUIREMENTS:
{technical_requirements}

TEAM COMPOSITION:
{team_composition}

Create a project plan including:

1. PROJECT STRUCTURE:
   - Architecture overview
   - Technology stack
   - Development environment
   - Deployment strategy

2. TIMELINE & MILESTONES:
   - Development phases
   - Key milestones
   - Dependencies
   - Risk factors

3. TASK BREAKDOWN:
   - Feature requirements
   - Technical tasks
   - Testing requirements
   - Documentation needs

4. RESOURCE ALLOCATION:
   - Team roles and responsibilities
   - Skill requirements
   - Training needs
   - External dependencies

5. RISK MANAGEMENT:
   - Technical risks
   - Timeline risks
   - Resource risks
   - Mitigation strategies

Provide:
- Detailed project plan
- Timeline estimates
- Resource requirements
- Risk assessment
- Success criteria

Return comprehensive project planning document.
```

### Requirements Analysis Prompt
```
Analyze and refine these project requirements:

RAW REQUIREMENTS:
{raw_requirements}

PROJECT CONTEXT:
{project_context}

Analyze for:

1. REQUIREMENT CLARITY:
   - Ambiguous statements
   - Missing details
   - Conflicting requirements
   - Unrealistic expectations

2. TECHNICAL FEASIBILITY:
   - Technology constraints
   - Resource limitations
   - Timeline considerations
   - Integration challenges

3. SCOPE DEFINITION:
   - Core features
   - Nice-to-have features
   - Out-of-scope items
   - Dependencies

4. ACCEPTANCE CRITERIA:
   - Measurable outcomes
   - Success metrics
   - Testing requirements
   - User acceptance criteria

5. IMPLEMENTATION STRATEGY:
   - Development approach
   - Architecture decisions
   - Technology choices
   - Integration points

Provide:
- Refined requirements
- Technical specifications
- Implementation approach
- Risk assessment
- Timeline estimates

Return structured requirements analysis.
```

## Documentation & Communication

### Technical Writing Prompt
```
Create technical documentation for this topic:

TOPIC:
{topic}

AUDIENCE:
{audience}

CONTEXT:
{context}

Create:

1. OVERVIEW DOCUMENTATION:
   - Executive summary
   - Key concepts
   - Business value
   - Technical overview

2. USER DOCUMENTATION:
   - Getting started guide
   - Step-by-step instructions
   - Troubleshooting guide
   - FAQ section

3. TECHNICAL DOCUMENTATION:
   - Architecture diagrams
   - API documentation
   - Configuration guide
   - Performance considerations

4. MAINTENANCE DOCUMENTATION:
   - Deployment procedures
   - Monitoring guidelines
   - Backup strategies
   - Update procedures

Use:
- Clear, concise language
- Visual aids where helpful
- Practical examples
- Consistent formatting
- Appropriate technical depth

Return comprehensive documentation package.
```

### Meeting Summary Prompt
```
Create a comprehensive summary of this meeting:

MEETING DETAILS:
- Date: {date}
- Participants: {participants}
- Duration: {duration}
- Topic: {topic}

MEETING NOTES:
{meeting_notes}

Create a summary including:

1. KEY DECISIONS:
   - Decisions made
   - Rationale
   - Impact assessment
   - Next steps

2. ACTION ITEMS:
   - Assigned tasks
   - Responsible parties
   - Deadlines
   - Dependencies

3. DISCUSSION POINTS:
   - Key topics covered
   - Different viewpoints
   - Concerns raised
   - Resolutions reached

4. FOLLOW-UP ITEMS:
   - Pending decisions
   - Required research
   - Stakeholder communications
   - Timeline updates

Format:
- Executive summary
- Detailed breakdown
- Action item tracker
- Next meeting agenda

Return structured meeting summary with clear action items.
```

## Problem Solving

### Technical Problem Analysis Prompt
```
Analyze this technical problem and provide solutions:

PROBLEM DESCRIPTION:
{problem_description}

CONTEXT:
{context}

SYMPTOMS:
{symptoms}

Analyze for:

1. PROBLEM CLASSIFICATION:
   - Type of issue
   - Severity level
   - Impact assessment
   - Urgency

2. ROOT CAUSE ANALYSIS:
   - Likely causes
   - Contributing factors
   - System interactions
   - Environmental factors

3. SOLUTION OPTIONS:
   - Immediate fixes
   - Long-term solutions
   - Workarounds
   - Prevention measures

4. IMPLEMENTATION STRATEGY:
   - Solution approach
   - Resource requirements
   - Timeline estimates
   - Risk assessment

5. VALIDATION PLAN:
   - Testing approach
   - Success criteria
   - Monitoring requirements
   - Rollback plan

Provide:
- Problem analysis
- Solution recommendations
- Implementation plan
- Risk assessment
- Success metrics

Return comprehensive problem-solving approach.
```

### Performance Optimization Prompt
```
Analyze and optimize performance for this system:

SYSTEM DESCRIPTION:
{system_description}

PERFORMANCE ISSUES:
{performance_issues}

CURRENT METRICS:
{current_metrics}

Analyze for:

1. PERFORMANCE BOTTLENECKS:
   - CPU usage patterns
   - Memory consumption
   - I/O operations
   - Network latency
   - Database queries

2. OPTIMIZATION OPPORTUNITIES:
   - Algorithm improvements
   - Caching strategies
   - Database optimization
   - Code efficiency
   - Resource utilization

3. SCALABILITY CONSIDERATIONS:
   - Horizontal scaling
   - Vertical scaling
   - Load balancing
   - Database sharding
   - Microservices architecture

4. MONITORING & PROFILING:
   - Performance metrics
   - Profiling tools
   - Alerting thresholds
   - Baseline measurements

Provide:
- Performance analysis
- Optimization recommendations
- Implementation plan
- Expected improvements
- Monitoring strategy

Return comprehensive performance optimization plan.
```

## Learning & Development

### Code Learning Prompt
```
Help me understand this code and learn best practices:

CODE:
```{language}
{code}
```

MY BACKGROUND:
{background}

EXPERIENCE LEVEL:
{experience_level}

Explain:

1. CODE STRUCTURE:
   - Overall architecture
   - Design patterns used
   - Component relationships
   - Data flow

2. KEY CONCEPTS:
   - Important principles
   - Language features
   - Framework concepts
   - Best practices

3. LEARNING OPPORTUNITIES:
   - Areas for improvement
   - Alternative approaches
   - Modern practices
   - Industry standards

4. PRACTICAL APPLICATIONS:
   - Real-world examples
   - Use cases
   - Similar patterns
   - Related technologies

5. NEXT STEPS:
   - Learning resources
   - Practice exercises
   - Related topics
   - Skill development

Use:
- Clear explanations
- Practical examples
- Visual aids
- Progressive complexity
- Real-world context

Return comprehensive learning guide.
```

### Skill Assessment Prompt
```
Assess my technical skills and provide development recommendations:

SKILLS SELF-ASSESSMENT:
{skills_assessment}

CAREER GOALS:
{career_goals}

CURRENT ROLE:
{current_role}

Assess:

1. SKILL GAPS:
   - Missing competencies
   - Industry requirements
   - Role expectations
   - Career progression needs

2. STRENGTHS:
   - Core competencies
   - Unique skills
   - Experience areas
   - Competitive advantages

3. DEVELOPMENT PLAN:
   - Priority skills
   - Learning resources
   - Timeline
   - Milestones

4. PRACTICAL STEPS:
   - Immediate actions
   - Project suggestions
   - Practice exercises
   - Mentorship opportunities

5. CAREER ALIGNMENT:
   - Role fit assessment
   - Industry trends
   - Salary expectations
   - Growth opportunities

Provide:
- Skills assessment
- Development roadmap
- Resource recommendations
- Timeline estimates
- Success metrics

Return comprehensive skills development plan.
``` 