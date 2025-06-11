ra.py-crew-Ai+gemini(main),others if gemini doesnt work
rlg.py-langraph framework
# Resume Optimization System 🚀

An intelligent resume optimization tool that analyzes your resume, extracts skills, and creates ATS-friendly versions tailored to specific job descriptions. The system uses AI-powered analysis with fallback modes to ensure reliable performance.

## Features ✨

- **Multiple Input Methods**: Support for PDF files, text files, and direct text input
- **AI-Powered Optimization**: Uses Google Gemini or OpenAI GPT for intelligent resume enhancement
- **ATS-Friendly Formatting**: Creates resumes optimized for Applicant Tracking Systems
- **Skill Extraction**: Automatically identifies technical, soft, and domain skills
- **Job Matching**: Analyzes how well your resume matches job requirements
- **Fallback Mode**: Enhanced processing when AI services are unavailable
- **Export Options**: Save optimized resumes to text files

## Installation 📦

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Required Dependencies

```bash
pip install crewai
pip install langchain-google-genai
pip install langchain-openai
pip install PyPDF2
pip install pdfplumber
pip install pydantic
```

### Optional Dependencies (Recommended)

```bash
pip install PyMuPDF  # For better PDF text extraction
```

### Quick Install

```bash
# Clone or download the script
# Install all dependencies at once
pip install crewai langchain-google-genai langchain-openai PyPDF2 pdfplumber pydantic PyMuPDF
```

## Configuration ⚙️

### API Keys Setup

The system supports two AI providers. Set up at least one:

#### Google Gemini (Recommended)
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

#### OpenAI (Fallback)
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

### Getting API Keys

**Google Gemini:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set the environment variable

**OpenAI:**
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Set the environment variable

## Usage 🖥️

### Basic Usage

```bash
python resume_optimizer.py
```

### Step-by-Step Process

1. **Run the Script**
   ```bash
   python resume_optimizer.py
   ```

2. **Provide Your Resume**
   - Option 1: Upload PDF file
   - Option 2: Upload text file
   - Option 3: Paste resume text directly

3. **Provide Job Description**
   - Option 1: Upload text file
   - Option 2: Paste job description directly

4. **Get Results**
   - View optimized resume in terminal
   - Option to save results to file

### Example Workflow

```
🚀 RESUME OPTIMIZATION SYSTEM 🚀
==================================================

Setting up LLM provider...
✓ Using Google Gemini (gemini-1.5-flash-latest)
✓ Gemini connection successful

Step 1: Provide your resume

=== RESUME INPUT OPTIONS ===
1. Upload PDF file
2. Upload text file
3. Paste resume text directly

Select option (1-3): 1
Enter the path to your PDF resume: /path/to/resume.pdf
✓ PDF processed successfully!

Step 2: Provide the job description

=== JOB DESCRIPTION INPUT ===
1. Upload text file
2. Paste job description directly

Select option (1-2): 2
[Paste job description and type 'END']
```

## System Architecture 🏗️

### AI Processing Modes

1. **AI-Powered Mode** (Primary)
   - Uses Google Gemini or OpenAI GPT
   - Advanced natural language processing
   - Intelligent keyword optimization

2. **Enhanced Fallback Mode** (Secondary)
   - Keyword-based skill extraction
   - Template-based optimization
   - ATS-friendly formatting

### Supported File Formats

- **PDF Files**: Uses multiple extraction methods (PyMuPDF, pdfplumber, PyPDF2)
- **Text Files**: UTF-8 encoded plain text
- **Direct Input**: Copy-paste functionality

## Output Features 📊

### Generated Content

- **Professional Summary**: Tailored to job requirements
- **Technical Skills**: Categorized and prioritized
- **ATS Optimization**: Keyword-rich formatting
- **Job Matching Analysis**: Quantified compatibility score
- **Recommendations**: Specific improvement suggestions

### Sample Output Structure

```
[Candidate Name]
[Contact Information]

PROFESSIONAL SUMMARY
[AI-generated summary with job-specific keywords]

TECHNICAL SKILLS
• Programming Languages: [Relevant languages]
• Frameworks & Tools: [Matching technologies]
• Databases & Cloud: [Platform expertise]

PROFESSIONAL EXPERIENCE
[Optimized work history with quantified achievements]

EDUCATION
[Educational background]

CORE COMPETENCIES
[Soft skills and domain expertise]

=== ATS OPTIMIZATION FEATURES ===
✓ Standard section headers for ATS parsing
✓ Keyword optimization based on job requirements
✓ Quantified achievements and metrics
```

## Troubleshooting 🔧

### Common Issues

**1. PDF Text Extraction Fails**
```
Solution: Install PyMuPDF for better PDF handling
pip install PyMuPDF
```

**2. API Key Errors**
```
Error: Google API key not found
Solution: Set environment variable
export GOOGLE_API_KEY="your_key_here"
```

**3. LLM Connection Issues**
```
Solution: System automatically falls back to enhanced mode
Fallback provides reliable keyword-based optimization
```

### Performance Tips

- Use PDF files with selectable text (not scanned images)
- Ensure API keys are properly set in environment variables
- For large resumes, allow extra processing time

## Advanced Configuration 🔧

### Customizing Skill Keywords

Edit the keyword lists in the `SimpleFallback` class:

```python
technical_keywords = [
    'python', 'javascript', 'java', 'c++', 'react', 'node.js',
    # Add your industry-specific keywords here
]

soft_keywords = [
    'leadership', 'communication', 'teamwork', 'problem-solving',
    # Add relevant soft skills
]
```

### Modifying Output Format

Customize the resume template in the `create_optimized_resume` method:

```python
optimized_resume = f"""
{name_line}
{' | '.join(contact_info)}

# Modify sections as needed
PROFESSIONAL SUMMARY
[Your custom summary format]
"""
```

## Dependencies 📋

| Package | Version | Purpose |
|---------|---------|----------|
| crewai | Latest | AI agent framework |
| langchain-google-genai | Latest | Google Gemini integration |
| langchain-openai | Latest | OpenAI GPT integration |
| PyPDF2 | Latest | PDF text extraction |
| pdfplumber | Latest | Enhanced PDF processing |
| PyMuPDF | Latest | Advanced PDF handling |
| pydantic | Latest | Data validation |

## Contributing 🤝

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install dependencies
4. Make your changes
5. Test thoroughly
6. Submit pull request

### Testing

```bash
# Test with sample resume and job description
python resume_optimizer.py

# Test PDF extraction
python -c "from resume_optimizer import ResumeInputHandler; print(ResumeInputHandler.extract_text_from_pdf('test.pdf'))"
```

## License 📄

This project is open source. Feel free to modify and distribute according to your needs.

## Support 💬

For issues and questions:
1. Check the troubleshooting section
2. Verify API key configuration
3. Test with sample files
4. Review error messages for specific guidance

## Changelog 📝

### Latest Version
- ✅ Multi-provider LLM support (Gemini + OpenAI)
- ✅ Enhanced PDF processing with multiple extraction methods
- ✅ Robust fallback system for reliable operation
- ✅ ATS-optimized output formatting
- ✅ Comprehensive skill extraction and matching
- ✅ Interactive input handling with error recovery

---
