# LangGraph Resume Optimization System 🚀

An advanced AI-powered resume optimization tool built with Google's **LangGraph** framework. This system uses a multi-agent workflow to analyze, optimize, and score resumes for ATS (Applicant Tracking System) compatibility.

## 🌟 Features

### Core Capabilities
- **Multi-Agent Workflow**: 5 specialized agents working in sequence
- **Google Gemini Integration**: Powered by Google's latest AI model
- **ATS Scoring**: Quantified compatibility assessment (0-100)
- **Smart Skill Extraction**: Automatic identification of technical and soft skills
- **Job Matching**: Tailored optimization based on job descriptions
- **Multiple Input Methods**: PDF, text files, or direct input
- **Error Resilience**: Fallback mechanisms for reliable operation

### Agent Workflow
1. **Resume Parser Agent** - Extracts contact info and sections
2. **Skills Analyzer Agent** - Identifies technical and soft skills
3. **Job Analyzer Agent** - Processes job requirements and keywords
4. **Resume Optimizer Agent** - AI-powered resume enhancement
5. **ATS Scorer Agent** - Calculates compatibility score and recommendations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Google API key for Gemini access

### Required Dependencies

```bash
# Core framework
pip install langgraph

# Google AI integration
pip install langchain-google-genai

# File processing
pip install PyPDF2

# Environment management (optional but recommended)
pip install python-dotenv
```

### Quick Installation

```bash
# Install all dependencies at once
pip install langgraph langchain-google-genai PyPDF2 python-dotenv
```

## ⚙️ Setup & Configuration

### 1. Get Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the generated key

### 2. Set Environment Variables

Choose one of these methods:

**Method 1: Environment Variable**
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

**Method 2: .env File (Recommended)**
```bash
# Create .env file in your project directory
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

**Method 3: System Environment (Windows)**
```cmd
set GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Verify Setup

```python
import os
print("API Key loaded:", bool(os.getenv('GOOGLE_API_KEY')))
```

## 🚀 Usage

### Basic Usage

```bash
python resume_optimizer.py
```

### Step-by-Step Workflow

1. **Start the Application**
   ```bash
   python resume_optimizer.py
   ```

2. **Choose Resume Input Method**
   ```
   === Resume Optimization Tool ===
   
   Choose resume input method:
   1. Type/paste resume text
   2. Load from text file
   3. Load from PDF file
   
   Enter choice (1-3): 
   ```

3. **Provide Job Description**
   ```
   Choose job description input method:
   1. Type/paste job description
   2. Load from text file
   
   Enter choice (1-2):
   ```

4. **View Results**
   - ATS compatibility score
   - Skills analysis
   - Optimization recommendations
   - Fully optimized resume

### Input Methods Explained

#### Resume Input Options
- **Option 1**: Direct text input (press Enter twice to finish)
- **Option 2**: Load from `.txt` file
- **Option 3**: Load from `.pdf` file (automatic text extraction)

#### Job Description Input
- **Option 1**: Direct text input (press Enter twice to finish)
- **Option 2**: Load from `.txt` file

## 📊 System Architecture

### Agent Flow Diagram
```
Resume Text → Parse Resume → Analyze Skills → Analyze Job
                                ↓
ATS Scorer ← Optimize Resume ← Job Requirements
```

### State Management
The system uses a shared state object (`ResumeState`) that passes information between agents:

```python
class ResumeState(TypedDict):
    resume_text: str           # Original resume
    job_description: str       # Target job description
    parsed_data: Dict          # Extracted contact info & sections
    skills: Dict               # Technical & soft skills
    job_requirements: Dict     # Job keywords & requirements
    optimized_resume: str      # Final optimized resume
    ats_score: float          # Compatibility score (0-100)
    recommendations: List     # Improvement suggestions
    errors: List              # Error tracking
```

## 📈 Output Analysis

### Sample Output Structure

```
=== OPTIMIZATION RESULTS ===
🎯 ATS Score: 87.5/100

📊 Skills Found:
   Technical: python, javascript, react, aws, docker
   Soft Skills: leadership, communication, teamwork

💡 Recommendations:
   - Include more job-relevant keywords
   - Quantify achievements with specific metrics

📄 OPTIMIZED RESUME:
--------------------------------------------------
[AI-optimized resume with ATS-friendly formatting]
```

### ATS Scoring Methodology

The system calculates scores based on:
- **Keyword Matching** (50%): Job requirements vs. resume content
- **Format Quality** (50%): Professional structure and contact info

**Score Ranges:**
- **90-100**: Excellent ATS compatibility
- **80-89**: Good compatibility, minor improvements needed
- **70-79**: Fair compatibility, several improvements recommended
- **Below 70**: Significant optimization required

## 🛠️ Advanced Configuration

### Customizing Skill Databases

Edit the skill lists in the `skills_analyzer_agent` method:

```python
def skills_analyzer_agent(self, state: ResumeState) -> ResumeState:
    technical_skills = [
        'python', 'javascript', 'java', 'c++', 'react', 'node.js',
        # Add your industry-specific skills here
        'tensorflow', 'pytorch', 'scikit-learn'  # For ML roles
    ]
    
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem-solving',
        # Add relevant soft skills
        'mentoring', 'cross-functional collaboration'
    ]
```

### Modifying LLM Parameters

Adjust the Gemini model settings:

```python
def _setup_llm(self):
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0.3,  # Lower = more consistent, Higher = more creative
        google_api_key=api_key,
        max_tokens=4000,  # Increase for longer resumes
        top_p=0.8        # Nucleus sampling parameter
    )
```

### Custom Optimization Prompts

Modify the optimization logic in `resume_optimizer_agent`:

```python
prompt = f"""
Optimize this resume for a {job_role} position.

REQUIREMENTS:
- Use industry-specific terminology
- Include quantified achievements
- Ensure ATS-friendly formatting
- Maximum 2 pages length

ORIGINAL RESUME:
{resume_text}

TARGET KEYWORDS:
{job_keywords}
"""
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. API Key Not Found
```
ERROR: GOOGLE_API_KEY environment variable not found!
```
**Solution:**
- Verify your API key is set correctly
- Check for typos in the environment variable name
- Restart your terminal/IDE after setting the variable

#### 2. PDF Reading Errors
```
Error reading PDF: [specific error]
```
**Solutions:**
- Ensure PDF contains selectable text (not scanned images)
- Try converting PDF to text file first
- Use a different PDF processing tool if needed

#### 3. LLM Connection Issues
```
Error in resume optimization: [connection error]
```
**Solutions:**
- Check internet connection
- Verify API key has sufficient quota
- Wait a moment and retry (rate limiting)

#### 4. Empty Results
```
Optimized resume is empty
```
**Solutions:**
- Check if resume text was properly extracted
- Ensure job description is not empty
- Review error messages in the output

### Performance Tips

1. **File Size**: Keep PDF files under 10MB for best performance
2. **Text Quality**: Use PDFs with selectable text, not scanned images
3. **Internet**: Ensure stable connection for AI processing
4. **API Limits**: Be aware of Google's API rate limits

## 🧪 Testing & Development

### Running Tests

```python
# Test PDF extraction
from resume_optimizer import read_pdf_file
text = read_pdf_file("sample_resume.pdf")
print(f"Extracted {len(text)} characters")

# Test async functionality
import asyncio
from resume_optimizer import ResumeOptimizationGraph

async def test_optimization():
    optimizer = ResumeOptimizationGraph()
    results = await optimizer.optimize_resume(
        "Sample resume text...", 
        "Sample job description..."
    )
    print(f"ATS Score: {results['ats_score']}")

asyncio.run(test_optimization())
```

### Development Setup

1. Clone/download the script
2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies
4. Set up environment variables
5. Run tests

## 📋 Dependencies Reference

| Package | Purpose | Version |
|---------|---------|---------|
| `langgraph` | Multi-agent workflow framework | Latest |
| `langchain-google-genai` | Google Gemini AI integration | Latest |
| `PyPDF2` | PDF text extraction | Latest |
| `python-dotenv` | Environment variable management | Latest |

## 🤝 Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 conventions
2. **Error Handling**: Always include try-catch blocks
3. **Documentation**: Update docstrings for new methods
4. **Testing**: Test with various resume formats
5. **Backwards Compatibility**: Maintain existing API

### Adding New Agents

To add a new agent to the workflow:

1. **Define Agent Method**:
   ```python
   def new_agent(self, state: ResumeState) -> ResumeState:
       try:
           # Agent logic here
           return state
       except Exception as e:
           state["errors"].append(f"New agent error: {str(e)}")
           return state
   ```

2. **Update Graph**:
   ```python
   workflow.add_node("new_agent", self.new_agent)
   workflow.add_edge("previous_agent", "new_agent")
   ```

3. **Update State** (if needed):
   ```python
   class ResumeState(TypedDict):
       # existing fields...
       new_field: Any  # Add new state fields
   ```

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🆘 Support

### Getting Help

1. **Check Troubleshooting**: Review the troubleshooting section above
2. **Verify Setup**: Ensure API keys and dependencies are correctly configured
3. **Test with Samples**: Try with known-good resume and job description files
4. **Check Logs**: Review error messages for specific guidance

### Common Questions

**Q: Can I use other LLM providers?**  
A: Yes, but you'll need to modify the `_setup_llm()` method to use different providers like OpenAI or Anthropic.

**Q: How accurate is the ATS scoring?**  
A: The scoring provides a good baseline but should be supplemented with manual review and real ATS testing.

**Q: Can I process multiple resumes at once?**  
A: The current version processes one resume at a time. Batch processing can be added as an enhancement.

**Q: What file formats are supported?**  
A: Currently supports PDF and TXT files, plus direct text input.

---

**Built with ❤️ using Google's LangGraph framework**

*Empowering job seekers with AI-driven resume optimization*
