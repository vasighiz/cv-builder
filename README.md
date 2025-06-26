# Resume Builder with Local LLM Support

A comprehensive resume builder that can generate professional resumes using both local LLM models (Mistral 7B) and API-based models (OpenAI GPT-4). This project provides a modular architecture for easy switching between local and cloud-based LLM providers.

## 🚀 Features

### Core Resume Building
- **Job Analysis**: Analyze job descriptions to extract key requirements and keywords
- **Keyword Matching**: Match candidate skills with job requirements
- **Resume Section Generation**: Create professional resume sections
- **Final Resume Assembly**: Combine all sections into a complete resume
- **Enhanced Resume Generation**: Improve existing resumes using LLM

### LLM Integration
- **Local LLM Support**: Use Mistral 7B and other local models for testing
- **API LLM Support**: Use OpenAI GPT-4 for production
- **Easy Provider Switching**: Switch between local and API models seamlessly
- **Usage Statistics**: Track token usage and performance metrics
- **Reusable Components**: Modular design for use in other projects

### Prompt Management
- **Organized Prompts**: Categorized prompts for different use cases
- **Personal Prompt Library**: Save and reuse effective prompts
- **Quick Reference**: Easy access to commonly used prompts

## 📋 Requirements

### System Requirements
- Python 3.8+
- 8GB+ RAM (for local LLM models)
- 10GB+ free disk space (for model downloads)
- CUDA-compatible GPU (optional, for faster inference)

### Python Dependencies
```bash
pip install -r requirements.txt
```

Key dependencies include:
- `torch>=2.0.0` - PyTorch for local model inference
- `transformers>=4.30.0` - Hugging Face transformers
- `openai==1.3.0` - OpenAI API client
- `python-dotenv==1.1.0` - Environment variable management

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vasighiz/cv-builder.git
   cd cv-builder
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🎯 Quick Start

### Using Local LLM (Mistral 7B)

1. **Test local LLM setup**
   ```bash
   python test_local_llm.py
   ```

2. **Run resume generation with local model**
   ```python
   from src.modules.llm_interface import create_llm_interface
   
   # Create interface with local provider
   llm = create_llm_interface("local")
   
   # Generate content
   response = llm.generate_response("Write a professional summary for a data scientist.")
   print(response)
   ```

### Using API LLM (OpenAI)

1. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Switch to API provider**
   ```python
   llm = create_llm_interface("api")
   llm.set_provider("api")
   ```

### Complete Resume Generation

```python
from src.modules.enhanced_resume_generator import EnhancedResumeGenerator
from pathlib import Path

# Create generator with local LLM
generator = EnhancedResumeGenerator(llm_provider="local")

# Generate enhanced resume
output_dir = Path("output")
enhanced_resume = generator.generate_enhanced_resume(
    job_name="data_scientist_position",
    output_dir=output_dir,
    llm_provider="local"  # or "api"
)
```

## 📁 Project Structure

```
resume-builder/
├── src/
│   ├── modules/
│   │   ├── local_llm_manager.py      # Local LLM management
│   │   ├── llm_interface.py          # Unified LLM interface
│   │   ├── enhanced_resume_generator.py  # Enhanced resume generation
│   │   ├── job_analyzer.py           # Job description analysis
│   │   ├── keyword_matcher.py        # Keyword matching
│   │   ├── resume_sections_generator_mvp.py  # Section generation
│   │   └── final_resume_generator.py # Final resume assembly
│   ├── data/
│   │   ├── keywords/                 # Keyword databases
│   │   ├── samples/                  # Sample job descriptions
│   │   └── templates/                # Resume templates
│   └── utils/                        # Utility functions
├── .cursor/
│   ├── prompts/                      # Organized AI prompts
│   └── my_prompts/                   # Personal prompt library
├── tests/                            # Test files
├── output/                           # Generated resumes
└── requirements.txt                  # Python dependencies
```

## 🔧 Configuration

### LLM Configuration

The system supports multiple LLM configurations:

```python
from src.modules.local_llm_manager import LLMConfig, MISTRAL_7B_CONFIG

# Default Mistral 7B configuration
config = MISTRAL_7B_CONFIG

# Custom configuration
custom_config = LLMConfig(
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    model_type="local",
    max_length=2048,
    temperature=0.7,
    top_p=0.9,
    device="auto"  # auto, cpu, cuda, mps
)
```

### Environment Variables

Create a `.env` file with:

```env
# OpenAI API (for production)
OPENAI_API_KEY=your-openai-api-key

# Local model settings (optional)
LOCAL_MODEL_PATH=./models
DEVICE=cuda  # or cpu, mps
```

## 🧪 Testing

### Test Local LLM
```bash
python test_local_llm.py
```

### Test LLM Interface
```bash
python -m src.modules.llm_interface
```

### Test Enhanced Generator
```bash
python -m src.modules.enhanced_resume_generator
```

## 📊 Usage Statistics

The system tracks usage statistics for both local and API providers:

```python
llm = create_llm_interface("local")
stats = llm.get_usage_stats()

# Example output:
# {
#     "local": {"calls": 5, "tokens": 1250, "errors": 0},
#     "api": {"calls": 0, "tokens": 0, "errors": 0}
# }
```

## 🔄 Switching Between Providers

### During Runtime
```python
llm = create_llm_interface("local")

# Switch to API
llm.set_provider("api")

# Switch back to local
llm.set_provider("local")
```

### For Different Use Cases
```python
# Development/testing with local model
generator = EnhancedResumeGenerator(llm_provider="local")

# Production with API model
generator = EnhancedResumeGenerator(llm_provider="api")
```

## 🎨 Prompt Management

### Using Organized Prompts
```python
# Prompts are organized in .cursor/prompts/
# - resume_analysis.md
# - resume_generation.md
# - ats_optimization.md
# - general_ai_prompts.md
```

### Personal Prompt Library
```python
# Save effective prompts in .cursor/my_prompts/
# - module_creation/
# - code_generation/
# - project_setup/
# - debugging/
```

## 🚀 Performance Tips

### Local LLM Optimization
1. **Use GPU acceleration** when available
2. **Adjust model parameters** for speed vs quality trade-off
3. **Use smaller models** for faster inference
4. **Enable model caching** to avoid re-downloading

### API LLM Optimization
1. **Batch requests** when possible
2. **Use appropriate temperature** settings
3. **Monitor token usage** to control costs
4. **Implement retry logic** for failed requests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Local model not loading**
   - Check available disk space
   - Verify internet connection for model download
   - Ensure sufficient RAM/VRAM

2. **API provider not working**
   - Verify API key is set correctly
   - Check API quota and billing
   - Ensure network connectivity

3. **Performance issues**
   - Use smaller models for testing
   - Enable GPU acceleration
   - Adjust batch sizes

### Getting Help

- Check the test files for usage examples
- Review the prompt templates for guidance
- Open an issue for bugs or feature requests

## 🔮 Future Enhancements

- [ ] Support for more local models (Llama, GPT-J, etc.)
- [ ] Model fine-tuning capabilities
- [ ] Web interface for resume generation
- [ ] Integration with job boards
- [ ] Multi-language support
- [ ] Advanced ATS optimization 