# [Prompt Name]

## Purpose
Brief description of what this prompt does and what problem it solves.

## When to Use
- Specific scenarios where this prompt is effective
- Input requirements and format
- Expected output format
- Any prerequisites or context needed

## Original Context
- When/why this prompt was created
- What specific problem it solved
- How it was used in the original scenario
- Any constraints or limitations

## Prompt Template
```python
# System prompt (if applicable)
system_prompt = """
[System prompt content]
"""

# Main prompt template
prompt = """
[Your prompt content here with {template_variables}]
"""
```

## Usage Example
```python
# How to use the prompt
formatted_prompt = prompt.format(
    variable1="value1",
    variable2="value2",
    # Add all required variables
)

# If using with system prompt
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": formatted_prompt}
]
```

## Results
- What kind of output it produces
- Quality assessment (1-10)
- Completeness of results
- Any modifications or post-processing needed

## Notes
- Tips for customization
- Potential improvements
- Related prompts or alternatives
- Any gotchas or limitations

## Tags
- Category: [module_creation/code_generation/etc.]
- Difficulty: [easy/medium/hard]
- Time saved: [estimated time saved]
- Reusability: [high/medium/low]

---
**Created**: [Date]
**Last Updated**: [Date]
**Success Rate**: [estimated success rate] 