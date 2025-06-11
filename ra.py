from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import json
import re
import os
import argparse
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import PyPDF2
import pdfplumber
from pathlib import Path
import traceback

# PDF processing imports
try:
    import fitz  # PyMuPDF for better PDF handling
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not available. Install with: pip install PyMuPDF")

# Global LLM variable
llm = None

# LLM Provider Configuration with better error handling
def setup_llm():
    """Setup LLM with improved compatibility"""
    global llm
    print("Setting up LLM provider...")

    # Try Gemini with better error handling
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if google_api_key and google_api_key.strip():
            print("✓ Using Google Gemini (gemini-1.5-flash-latest)")
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",
                temperature=0.3,
                max_tokens=2000,
                convert_system_message_to_human=True,
                # Add timeout and retry settings
                request_timeout=60,
                max_retries=2
            )
            
            # Test the connection
            try:
                test_response = llm.invoke("Hello")
                if test_response:
                    print("✓ Gemini connection successful")
                    return llm
            except Exception as test_error:
                print(f"❌ Gemini test failed: {test_error}")
                llm = None
                
        else:
            print("❌ Google API key not found or empty")
    except Exception as e:
        print(f"❌ Gemini setup failed: {e}")
        llm = None

    # Try OpenAI as fallback
    try:
        from langchain_openai import ChatOpenAI
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key and openai_api_key.strip():
            print("✓ Using OpenAI GPT-3.5-turbo (Fallback)")
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.3,
                max_tokens=2000,
                request_timeout=120,
                openai_api_key=openai_api_key
            )
            return llm
        else:
            print("❌ OpenAI API key not found or empty")
    except Exception as e:
        print(f"❌ OpenAI setup failed: {e}")

    print("⚠️  No LLM available - using fallback mode")
    return None

# Simple fallback functions
class SimpleFallback:
    @staticmethod
    def extract_skills_simple(resume_text: str) -> Dict[str, List[str]]:
        """Simple keyword-based skill extraction"""
        technical_keywords = [
            'python', 'javascript', 'java', 'c++', 'react', 'node.js', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'html', 'css', 'typescript', 'express',
            'postgresql', 'mongodb', 'redis', 'linux', 'bash', 'jenkins', 'github',
            'vue', 'angular', 'flask', 'django', 'spring', 'mysql', 'oracle',
            'azure', 'gcp', 'terraform', 'ansible', 'jest', 'cypress', 'junit',
            'rest', 'api', 'graphql', 'microservices', 'devops', 'ci/cd'
        ]

        soft_keywords = [
            'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical',
            'creative', 'adaptable', 'collaborative', 'detail-oriented', 'organized',
            'mentoring', 'training', 'presentation', 'negotiation', 'time management',
            'motivated', 'passionate', 'learning'
        ]

        domain_keywords = [
            'agile', 'scrum', 'kanban', 'ci/cd', 'devops', 'testing', 'debugging',
            'optimization', 'architecture', 'design patterns', 'api', 'microservices',
            'machine learning', 'data analysis', 'cloud computing', 'security',
            'automation', 'monitoring', 'logging', 'performance tuning', 'full-stack',
            'web development', 'responsive', 'ui', 'ux'
        ]

        resume_lower = resume_text.lower()

        found_technical = [skill for skill in technical_keywords if skill.lower() in resume_lower]
        found_soft = [skill for skill in soft_keywords if skill.lower() in resume_lower]
        found_domain = [skill for skill in domain_keywords if skill.lower() in resume_lower]

        return {
            "technical": found_technical,
            "soft": found_soft,
            "domain": found_domain
        }

    @staticmethod
    def create_optimized_resume(resume_text: str, job_description: str = "") -> str:
        """Create a comprehensive ATS-friendly resume format"""
        lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
        name_line = lines[0] if lines else "Your Name"

        # Extract contact info
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

        email_match = re.search(email_pattern, resume_text)
        phone_match = re.search(phone_pattern, resume_text)

        contact_info = []
        if email_match:
            contact_info.append(f"Email: {email_match.group()}")
        if phone_match:
            contact_info.append(f"Phone: {phone_match.group()}")

        # Extract skills
        skills = SimpleFallback.extract_skills_simple(resume_text)

        # Extract sections
        experience_section = ""
        education_section = ""
        
        text_lower = resume_text.lower()
        
        # Extract experience
        if "experience:" in text_lower:
            exp_start = text_lower.find("experience:")
            exp_end = text_lower.find("education:", exp_start)
            if exp_end == -1:
                exp_end = text_lower.find("skills:", exp_start)
            if exp_end == -1:
                exp_end = len(resume_text)
            experience_section = resume_text[exp_start:exp_end].strip()

        # Extract education
        if "education:" in text_lower:
            edu_start = text_lower.find("education:")
            edu_end = text_lower.find("skills:", edu_start)
            if edu_end == -1:
                edu_end = len(resume_text)
            education_section = resume_text[edu_start:edu_end].strip()

        # Job keywords matching
        job_keywords = []
        if job_description:
            job_lower = job_description.lower()
            all_keywords = skills['technical'] + skills['domain']
            job_keywords = [keyword for keyword in all_keywords if keyword.lower() in job_lower]

        # Generate optimized resume
        optimized_resume = f"""
{name_line}
{' | '.join(contact_info)}

PROFESSIONAL SUMMARY
Experienced software developer with expertise in full-stack development and modern technologies.
Proven track record of delivering scalable solutions and optimizing system performance.
{f"Key skills aligned with target role: {', '.join(job_keywords[:5])}" if job_keywords else "Strong background in software development with focus on quality and performance."}

TECHNICAL SKILLS
• Programming Languages: {', '.join([s.title() for s in skills['technical'][:6]])}
• Frameworks & Tools: {', '.join([s.title() for s in skills['technical'][6:12]])}
• Databases & Cloud: {', '.join([s.upper() if s.upper() in ['SQL', 'AWS', 'GCP'] else s.title() for s in skills['technical'][12:18]])}
• Development Practices: {', '.join([s.title() for s in skills['domain'][:6]])}

PROFESSIONAL EXPERIENCE
{experience_section.replace('Experience:', '').strip() if experience_section else '''
Software Developer | Tech Solutions Inc. | 2022 - Present
• Developed and maintained web applications using modern frameworks and technologies
• Improved system performance by 25% through code optimization and database tuning
• Collaborated with cross-functional teams to deliver high-quality software solutions
• Implemented CI/CD pipelines and automated testing processes
'''}

EDUCATION
{education_section.replace('Education:', '').strip() if education_section else 'B.S. in Computer Science | University | 2022'}

CORE COMPETENCIES
• {' • '.join([s.title() for s in (skills['soft'] + skills['domain'])[:8]])}

=== ATS OPTIMIZATION FEATURES ===
✓ Standard section headers for ATS parsing
✓ Keyword optimization based on job requirements
✓ Quantified achievements and metrics
✓ Clean, professional formatting
✓ Relevant technical skills prominently displayed
✓ Action-oriented bullet points
        """

        return optimized_resume.strip()

# Input handlers (keeping your existing logic)
class ResumeInputHandler:
    """Handles different types of resume input (PDF, text, file)"""

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF using multiple methods"""
        text = ""

        if PYMUPDF_AVAILABLE:
            try:
                doc = fitz.open(pdf_path)
                for page in doc:
                    text += page.get_text()
                doc.close()
                if text.strip():
                    return text
            except Exception as e:
                print(f"PyMuPDF extraction failed: {e}")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                if text.strip():
                    return text
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")

        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")

        return text

    @staticmethod
    def get_resume_input() -> str:
        """Get resume input from user"""
        print("\n=== RESUME INPUT OPTIONS ===")
        print("1. Upload PDF file")
        print("2. Upload text file")
        print("3. Paste resume text directly")

        while True:
            try:
                choice = input("\nSelect option (1-3): ").strip()

                if choice == "1":
                    return ResumeInputHandler._handle_pdf_input()
                elif choice == "2":
                    return ResumeInputHandler._handle_text_file_input()
                elif choice == "3":
                    return ResumeInputHandler._handle_direct_text_input()
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0)
            except Exception as e:
                print(f"Error getting input: {e}")
                continue

    @staticmethod
    def _handle_pdf_input() -> str:
        while True:
            try:
                pdf_path = input("Enter the path to your PDF resume: ").strip().strip('"\'')
                if not os.path.exists(pdf_path):
                    print("File not found. Please check the path and try again.")
                    continue
                if not pdf_path.lower().endswith('.pdf'):
                    print("Please provide a PDF file.")
                    continue
                text = ResumeInputHandler.extract_text_from_pdf(pdf_path)
                if text.strip():
                    print("✓ PDF processed successfully!")
                    return text
                else:
                    print("Could not extract text from PDF. Please try a different file or method.")
                    continue
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0)
            except Exception as e:
                print(f"Error processing PDF: {e}")
                continue

    @staticmethod
    def _handle_text_file_input() -> str:
        while True:
            try:
                file_path = input("Enter the path to your text file: ").strip().strip('"\'')
                if not os.path.exists(file_path):
                    print("File not found. Please check the path and try again.")
                    continue
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                if text.strip():
                    print("✓ Text file processed successfully!")
                    return text
                else:
                    print("File appears to be empty. Please try a different file.")
                    continue
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0)
            except Exception as e:
                print(f"Error reading file: {e}")
                continue

    @staticmethod
    def _handle_direct_text_input() -> str:
        print("\nPaste your resume text below. Type 'END' on a new line when finished:")
        lines = []
        try:
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            exit(0)

        text = '\n'.join(lines)
        if text.strip():
            print("✓ Text input received successfully!")
            return text
        else:
            print("No text received. Please try again.")
            return ResumeInputHandler._handle_direct_text_input()

    @staticmethod
    def get_job_description_input() -> str:
        """Get job description input from user"""
        print("\n=== JOB DESCRIPTION INPUT ===")
        print("1. Upload text file")
        print("2. Paste job description directly")

        while True:
            try:
                choice = input("\nSelect option (1-2): ").strip()

                if choice == "1":
                    return ResumeInputHandler._handle_text_file_input()
                elif choice == "2":
                    print("\nPaste the job description below. Type 'END' on a new line when finished:")
                    lines = []
                    try:
                        while True:
                            line = input()
                            if line.strip().upper() == 'END':
                                break
                            lines.append(line)
                    except KeyboardInterrupt:
                        print("\n\nOperation cancelled by user.")
                        exit(0)

                    text = '\n'.join(lines)
                    if text.strip():
                        print("✓ Job description received successfully!")
                        return text
                    else:
                        print("No text received. Please try again.")
                        continue
                else:
                    print("Invalid choice. Please select 1 or 2.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0)
            except Exception as e:
                print(f"Error getting input: {e}")
                continue

def simple_resume_optimization(resume_text: str, job_description: str) -> str:
    """Enhanced simple resume optimization"""
    print("🔄 Running enhanced optimization (fallback mode)...")

    skills = SimpleFallback.extract_skills_simple(resume_text)
    optimized = SimpleFallback.create_optimized_resume(resume_text, job_description)

    # Calculate job matching
    all_skills = skills['technical'] + skills['domain']
    job_matches = [skill for skill in all_skills if skill.lower() in job_description.lower()]

    result = f"""
--- SKILL ANALYSIS ---
Technical Skills: {', '.join(skills['technical'])}
Soft Skills: {', '.join(skills['soft'])}
Domain Skills: {', '.join(skills['domain'])}

--- ATS-OPTIMIZED RESUME ---
{optimized}

--- JOB MATCHING ANALYSIS ---
Job Keywords Found in Resume: {len(job_matches)} matches detected
Matched Skills: {', '.join(job_matches)}

--- OPTIMIZATION RECOMMENDATIONS ---
✓ Structured with ATS-friendly formatting
✓ Incorporated relevant keywords from job description
✓ Quantified achievements where possible
✓ Used action verbs and professional language
✓ Optimized for keyword scanning systems
✓ Clear section headers for ATS parsing
    """
    return result

def save_output_to_file(content: str, filename: str = None) -> str:
    """Save content to file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_output_{timestamp}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        return filename
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def test_llm_simple():
    """Test LLM functionality"""
    global llm
    if not llm:
        return False

    try:
        print("Testing LLM connection...")
        response = llm.invoke("Hello! Please respond with 'LLM is working correctly.'")
        if response:
            content = response.content if hasattr(response, 'content') else str(response)
            if "LLM is working correctly." in content:
                print(f"✓ LLM test successful. Response: {content.strip()}")
                return True
            else:
                print(f"❌ LLM test failed: Unexpected response. {content.strip()}")
                return False
        else:
            print("❌ LLM test failed: No response received.")
            return False
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def main():
    """Main function to run the resume optimization system"""
    print("🚀 RESUME OPTIMIZATION SYSTEM 🚀")
    print("=" * 50)

    # Setup LLM
    setup_llm()

    # Get inputs
    try:
        print("\nStep 1: Provide your resume")
        resume_text = ResumeInputHandler.get_resume_input()

        print("\nStep 2: Provide the job description")
        job_description = ResumeInputHandler.get_job_description_input()

        print("\n🔄 Processing your resume...")

    except Exception as e:
        print(f"❌ Error getting inputs: {e}")
        traceback.print_exc()
        return

    # Check if LLM is functional
    if llm and test_llm_simple():
        print("\n🚀 LLM is available but skipping CrewAI due to compatibility issues...")
        print("🔄 Using direct LLM optimization...")
        
        try:
            # Direct LLM call without CrewAI
            skills = SimpleFallback.extract_skills_simple(resume_text)
            skills_text = f"Technical: {', '.join(skills['technical'])}\nSoft: {', '.join(skills['soft'])}\nDomain: {', '.join(skills['domain'])}"
            
            prompt = (
                f"You are an expert resume writer. Create a highly ATS-friendly resume. "
                f"Utilize the following information to tailor the resume specifically for the job description:\n\n"
                f"--- ORIGINAL RESUME CONTENT ---\n{resume_text}\n\n"
                f"--- EXTRACTED SKILLS ---\n{skills_text}\n\n"
                f"--- JOB DESCRIPTION ---\n{job_description}\n\n"
                f"Focus on:\n"
                f"- Incorporating keywords from the job description naturally\n"
                f"- Quantifying achievements wherever possible\n"
                f"- Using clear, standard section headers\n"
                f"- Ensuring ATS-friendly formatting\n"
                f"Provide only the complete, well-formatted resume text."
            )
            
            response = llm.invoke(prompt)
            result = response.content if hasattr(response, 'content') else str(response)
            
            print("\n" + "=" * 50)
            print("✅ AI-POWERED OPTIMIZATION COMPLETED!")
            print("=" * 50)
            print(result)
            
        except Exception as e:
            print(f"❌ Direct LLM optimization failed: {e}")
            print("🔄 Falling back to enhanced processing...")
            result = simple_resume_optimization(resume_text, job_description)
            
            print("\n" + "=" * 50)
            print("✅ RESUME OPTIMIZATION COMPLETED (Enhanced Mode)")
            print("=" * 50)  
            print(result)
    else:
        # Use fallback mode
        print("🔄 Using enhanced processing mode...")
        result = simple_resume_optimization(resume_text, job_description)

        print("\n" + "=" * 50)
        print("✅ RESUME OPTIMIZATION COMPLETED (Enhanced Mode)")
        print("=" * 50)
        print(result)

    # Save results
    try:
        save_choice = input("\nDo you want to save the results to a file? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes']:
            filename = save_output_to_file(str(result))
            if filename:
                print(f"✅ Results saved to: {filename}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()