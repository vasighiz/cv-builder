# AI-Powered Resume Builder

An automated resume builder using LLMs and AI-based strategies that takes a job description and generates optimized "Skills", "Work Experiences", and "Projects" sections for a gold-standard, ATS-compliant resume.

## 🎯 Project Overview

This system extracts key skills and requirements from job descriptions and generates FAANG-level resume sections that pass ATS filters, following industry best practices from "The Ultimate Resume Handbook (2024)".

**Target Roles**: Tech industry (AI, Data Scientist, Data Analyst, Machine Learning Engineer, ML Scientist, etc.)

## 🏗️ Project Architecture

### Core Modules

#### Module 1: Job Description Analyzer
**Purpose**: Extract keywords and requirements from job descriptions
- **Tech Stack**: Python, OpenAI API, LangChain, Pandas, JSON
- **Features**: 
  - Job description input (plain text)
  - LLM-powered keyword extraction (tech skills, soft skills, responsibilities)
  - Keyword frequency analysis
  - JSON output of categorized keywords

#### Module 2: Resume Keyword Matcher
**Purpose**: Compare user's resume against extracted keywords
- **Tech Stack**: Python, OpenAI API, Resume Parser libraries, Pandas
- **Features**:
  - Resume parsing and keyword extraction
  - Keyword coverage analysis
  - Missing keywords identification
  - Recommendations for additions

#### Module 3: Resume Sections Generator
**Purpose**: Auto-generate Skills, Experience, and Projects sections
- **Tech Stack**: Python, OpenAI API, LangChain, Template engines
- **Features**:
  - Skills section with relevance ranking
  - Work experience bullet points with action verbs and quantified results
  - Project descriptions with job-relevant language
  - ATS-optimized formatting

#### Module 4: Education & Extras Builder
**Purpose**: Recommend Education, Certifications, Languages
- **Tech Stack**: Python, OpenAI API, Database (SQLite/PostgreSQL)
- **Features**:
  - Course/certification suggestions for missing skills
  - Education section formatting
  - Optional sections recommendations

#### Module 5: Formatting & ATS Checker
**Purpose**: Ensure ATS compliance
- **Tech Stack**: Python, Regular expressions, Document processing libraries
- **Features**:
  - ATS-friendly formatting validation
  - Compliance scoring
  - Formatting suggestions
  - Font, margin, and structure checks

#### Module 6: Final Resume Assembler
**Purpose**: Combine components into final document
- **Tech Stack**: Python, python-docx, ReportLab, Streamlit/React
- **Features**:
  - Document generation (.docx/.pdf)
  - User editing interface
  - ATS summary report export

### Frontend & Backend
- **Frontend**: Streamlit (MVP) / React (enhanced)
- **Backend**: FastAPI (enhanced)
- **Database**: SQLite (MVP) / PostgreSQL (enhanced)
- **Storage**: Local files (MVP) / Cloud storage (enhanced)

## 🚀 MVP Features (Phase 1)

### Priority 1: Core Functionality
1. **Job Description Analyzer** - Basic keyword extraction
2. **Resume Sections Generator** - Skills and Experience generation
3. **Basic ATS Checker** - Format validation
4. **Simple Document Export** - .docx generation

### Priority 2: Enhanced Features
1. **Resume Keyword Matcher** - Gap analysis
2. **Education & Extras Builder** - Certification suggestions
3. **Advanced ATS Checker** - Compliance scoring

### Priority 3: Advanced Features
1. **Final Resume Assembler** - Complete document generation
2. **User Interface** - Streamlit web app
3. **Project Management** - Multiple resume versions

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume-builder
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
resume-builder/
├── src/
│   ├── modules/
│   │   ├── job_analyzer.py      # Module 1: Job Description Analyzer
│   │   ├── keyword_matcher.py   # Module 2: Resume Keyword Matcher
│   │   ├── section_generator.py # Module 3: Resume Sections Generator
│   │   ├── education_builder.py # Module 4: Education & Extras Builder
│   │   ├── ats_checker.py       # Module 5: Formatting & ATS Checker
│   │   └── resume_assembler.py  # Module 6: Final Resume Assembler
│   ├── utils/
│   │   ├── llm_client.py        # OpenAI API wrapper
│   │   ├── document_parser.py   # Resume parsing utilities
│   │   └── formatter.py         # Document formatting utilities
│   ├── data/
│   │   ├── keywords/            # Master keyword lists
│   │   ├── templates/           # Resume templates
│   │   └── samples/             # Sample job descriptions
│   └── ui/
│       └── streamlit_app.py     # Streamlit web interface
├── tests/
├── docs/
├── requirements.txt
├── main.py
└── README.md
```

## 🧪 Testing Strategy

### Unit Tests
- Individual module functionality
- LLM response parsing
- Document formatting validation

### Integration Tests
- End-to-end resume generation
- ATS compliance validation
- Document export functionality

### Sample Data
- Multiple job descriptions in `data/samples/`
- Resume templates in `data/templates/`
- Keyword lists in `data/keywords/`

## 🔄 Development Phases

### Phase 1: MVP (Weeks 1-2)
- Basic job description analysis
- Simple resume section generation
- Document export functionality

### Phase 2: Enhancement (Weeks 3-4)
- Keyword matching and gap analysis
- Advanced ATS compliance checking
- User interface development

### Phase 3: Advanced Features (Weeks 5-6)
- Complete resume assembly
- Multiple format support
- Performance optimization

## 📊 Success Metrics

- **ATS Compliance**: 95%+ pass rate on major ATS systems
- **Keyword Coverage**: 90%+ relevant keyword inclusion
- **User Satisfaction**: Resume quality improvement feedback
- **Processing Time**: <30 seconds for complete resume generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions, please open an issue in the repository. 