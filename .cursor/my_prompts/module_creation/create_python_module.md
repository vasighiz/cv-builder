# Create Python Module Structure

## Purpose
Generate a complete Python module structure with proper imports, class definitions, error handling, and documentation. This prompt is particularly effective for creating well-structured, production-ready Python modules.

## When to Use
- Creating new Python modules or packages
- Setting up module structure with proper organization
- Generating boilerplate code with best practices
- Creating modules that need to integrate with existing systems
- When you need consistent code structure across modules

## Original Context
Created during the resume builder project when we needed to generate multiple modules with consistent structure. This prompt was used to create the job analyzer, keyword matcher, and section generator modules. It proved effective for maintaining consistency and including all necessary components.

## Prompt Template
```python
# System prompt
system_prompt = """
You are an expert Python developer specializing in creating well-structured, production-ready modules.
Follow Python best practices, include proper error handling, comprehensive documentation, and maintainable code structure.
"""

# Main prompt template
prompt = """
Create a complete Python module for: {module_name}

MODULE PURPOSE:
{module_purpose}

REQUIRED FUNCTIONALITY:
{required_functionality}

INTEGRATION REQUIREMENTS:
{integration_requirements}

TECHNICAL REQUIREMENTS:
- Language: Python {python_version}
- Dependencies: {dependencies}
- Output format: {output_format}
- Error handling: {error_handling_requirements}

CREATE THE FOLLOWING:
1. Complete module file with proper imports
2. Main class with comprehensive methods
3. Error handling and validation
4. Comprehensive docstrings and comments
5. Type hints where appropriate
6. Example usage in docstring
7. Configuration handling if needed

STRUCTURE REQUIREMENTS:
- Follow PEP 8 style guidelines
- Include proper exception handling
- Add logging for debugging
- Include input validation
- Provide clear error messages
- Use dataclasses or Pydantic models if appropriate

Return the complete, runnable Python code with all necessary components.
"""
```

## Usage Example
```python
# Example usage for creating a job analyzer module
formatted_prompt = prompt.format(
    module_name="JobAnalyzer",
    module_purpose="Analyze job descriptions to extract keywords, requirements, and role information",
    required_functionality="""
    - Parse job description text
    - Extract technical skills and requirements
    - Identify role category and seniority
    - Generate structured analysis output
    """,
    integration_requirements="Integrate with OpenAI API for text analysis",
    python_version="3.8+",
    dependencies="openai, json, typing, dataclasses",
    output_format="JSON with structured analysis data",
    error_handling_requirements="Handle API errors, invalid input, and parsing failures"
)
```

## Results
- Produces complete, runnable Python modules
- Includes proper error handling and validation
- Follows Python best practices and PEP 8
- Contains comprehensive documentation
- Ready for immediate integration
- Quality assessment: 9/10

## Notes
- Works best when you provide detailed requirements
- Can be customized for different module types
- Add specific validation rules based on your needs
- Consider adding unit tests after generation
- Modify logging levels based on deployment environment

## Tags
- Category: module_creation
- Difficulty: medium
- Time saved: 30-45 minutes per module
- Reusability: high

---
**Created**: 2024-06-26
**Last Updated**: 2024-06-26
**Success Rate**: 95% 