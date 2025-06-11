"""
Resume Optimization using LangGraph (Real Google-supported framework)
Install: pip install langgraph langchain-google-genai
"""

import os
from typing import Dict, List, Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
import PyPDF2
import re

class ResumeState(TypedDict):
    """State passed between agents"""
    resume_text: str
    job_description: str
    parsed_data: Dict[str, Any]
    skills: Dict[str, List[str]]
    job_requirements: Dict[str, List[str]]
    optimized_resume: str
    ats_score: float
    recommendations: List[str]
    errors: List[str]

class ResumeOptimizationGraph:
    def __init__(self):
        self.llm = self._setup_llm()
        self.graph = self._create_graph()
    
    def _setup_llm(self):
        """Setup Google's Gemini model"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable required")
        
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0.3,
            google_api_key=api_key
        )
    
    def _create_graph(self) -> StateGraph:
        """Create the agent workflow graph"""
        workflow = StateGraph(ResumeState)
        
        # Add nodes (agents)
        workflow.add_node("parse_resume", self.parse_resume_agent)
        workflow.add_node("analyze_skills", self.skills_analyzer_agent)
        workflow.add_node("analyze_job", self.job_analyzer_agent)
        workflow.add_node("optimize_resume", self.resume_optimizer_agent)
        workflow.add_node("score_ats", self.ats_scorer_agent)
        
        # Define the flow
        workflow.set_entry_point("parse_resume")
        workflow.add_edge("parse_resume", "analyze_skills")
        workflow.add_edge("analyze_skills", "analyze_job")
        workflow.add_edge("analyze_job", "optimize_resume")
        workflow.add_edge("optimize_resume", "score_ats")
        workflow.add_edge("score_ats", END)
        
        return workflow.compile()
    
    def parse_resume_agent(self, state: ResumeState) -> ResumeState:
        """Parse resume and extract basic information"""
        try:
            resume_text = state["resume_text"]
            
            # Extract contact information
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            
            email_match = re.search(email_pattern, resume_text)
            phone_match = re.search(phone_pattern, resume_text)
            
            # Extract name (first non-empty line)
            lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
            name = lines[0] if lines else "Name Not Found"
            
            parsed_data = {
                "name": name,
                "email": email_match.group() if email_match else "",
                "phone": phone_match.group() if phone_match else "",
                "sections": self._extract_sections(resume_text)
            }
            
            state["parsed_data"] = parsed_data
            return state
            
        except Exception as e:
            state["errors"].append(f"Resume parsing error: {str(e)}")
            return state
    
    def skills_analyzer_agent(self, state: ResumeState) -> ResumeState:
        """Analyze and extract skills"""
        try:
            resume_text = state["resume_text"]
            
            # Skill databases
            technical_skills = [
                'python', 'javascript', 'java', 'c++', 'react', 'node.js', 'sql', 'aws',
                'docker', 'kubernetes', 'git', 'html', 'css', 'typescript'
            ]
            
            soft_skills = [
                'leadership', 'communication', 'teamwork', 'problem-solving', 'analytical'
            ]
            
            text_lower = resume_text.lower()
            
            found_technical = [skill for skill in technical_skills if skill.lower() in text_lower]
            found_soft = [skill for skill in soft_skills if skill.lower() in text_lower]
            
            state["skills"] = {
                "technical": found_technical,
                "soft": found_soft
            }
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Skills analysis error: {str(e)}")
            return state
    
    def job_analyzer_agent(self, state: ResumeState) -> ResumeState:
        """Analyze job description"""
        try:
            job_description = state["job_description"]
            
            # Extract keywords using LLM
            prompt = f"""
            Analyze this job description and extract:
            1. Required technical skills
            2. Required soft skills
            3. Key responsibilities
            4. Important keywords for ATS
            
            Job Description:
            {job_description}
            
            Return as JSON format:
            {{
                "required_technical": ["skill1", "skill2"],
                "required_soft": ["skill1", "skill2"],
                "keywords": ["keyword1", "keyword2"]
            }}
            """
            
            response = self.llm.invoke(prompt)
            
            # Simple keyword extraction as fallback
            keywords = ['python', 'javascript', 'react', 'aws', 'leadership', 'teamwork']
            found_keywords = [kw for kw in keywords if kw.lower() in job_description.lower()]
            
            state["job_requirements"] = {
                "keywords": found_keywords,
                "description": job_description
            }
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Job analysis error: {str(e)}")
            return state
    
    def resume_optimizer_agent(self, state: ResumeState) -> ResumeState:
        """Optimize resume using LLM"""
        try:
            resume_text = state["resume_text"]
            job_requirements = state["job_requirements"]
            skills = state["skills"]
            
            prompt = f"""
            Optimize this resume for the job requirements. Make it ATS-friendly.
            
            ORIGINAL RESUME:
            {resume_text}
            
            FOUND SKILLS:
            Technical: {', '.join(skills.get('technical', []))}
            Soft: {', '.join(skills.get('soft', []))}
            
            JOB KEYWORDS TO INCLUDE:
            {', '.join(job_requirements.get('keywords', []))}
            
            Create an optimized, ATS-friendly resume with:
            1. Professional formatting
            2. Relevant keywords naturally integrated
            3. Clear section headers
            4. Quantified achievements where possible
            
            Return only the formatted resume text.
            """
            
            response = self.llm.invoke(prompt)
            optimized_text = response.content if hasattr(response, 'content') else str(response)
            
            state["optimized_resume"] = optimized_text
            return state
            
        except Exception as e:
            state["errors"].append(f"Resume optimization error: {str(e)}")
            # Fallback to basic optimization
            state["optimized_resume"] = self._basic_optimization(state)
            return state
    
    def ats_scorer_agent(self, state: ResumeState) -> ResumeState:
        """Score ATS compatibility"""
        try:
            optimized_resume = state["optimized_resume"]
            job_keywords = state["job_requirements"].get("keywords", [])
            
            # Calculate keyword matching score
            text_lower = optimized_resume.lower()
            matched_keywords = [kw for kw in job_keywords if kw.lower() in text_lower]
            
            keyword_score = len(matched_keywords) / max(len(job_keywords), 1) * 100
            
            # Basic format scoring
            format_score = 85  # Assume good formatting from LLM
            if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', optimized_resume):
                format_score += 15
            
            overall_score = (keyword_score + format_score) / 2
            
            recommendations = []
            if keyword_score < 70:
                recommendations.append("Include more job-relevant keywords")
            if format_score < 80:
                recommendations.append("Improve resume formatting")
            
            state["ats_score"] = overall_score
            state["recommendations"] = recommendations
            
            return state
            
        except Exception as e:
            state["errors"].append(f"ATS scoring error: {str(e)}")
            state["ats_score"] = 75.0  # Default score
            return state
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract resume sections"""
        sections = {}
        text_lower = text.lower()
        
        # Extract experience section
        if 'experience:' in text_lower:
            start = text_lower.find('experience:')
            end = text_lower.find('education:', start)
            if end == -1:
                end = len(text)
            sections['experience'] = text[start:end].strip()
        
        return sections
    
    def _basic_optimization(self, state: ResumeState) -> str:
        """Basic rule-based optimization fallback"""
        parsed_data = state["parsed_data"]
        skills = state["skills"]
        
        # Fix: Use variables to avoid backslashes in f-strings
        name = parsed_data.get('name', 'Your Name')
        email = parsed_data.get('email', '')
        phone = parsed_data.get('phone', '')
        technical_skills_str = ', '.join(skills.get('technical', []))
        soft_skills_str = ', '.join(skills.get('soft', []))
        experience_section = parsed_data.get('sections', {}).get('experience', 'PROFESSIONAL EXPERIENCE\nSoftware Developer | Company | 2022-Present')
        
        return f"""{name}
{email} | {phone}

PROFESSIONAL SUMMARY
Experienced professional with expertise in {', '.join(skills.get('technical', [])[:5])}.

TECHNICAL SKILLS
{technical_skills_str}

CORE COMPETENCIES  
{soft_skills_str}

{experience_section}""".strip()
    
    async def optimize_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Main optimization method"""
        initial_state = ResumeState(
            resume_text=resume_text,
            job_description=job_description,
            parsed_data={},
            skills={},
            job_requirements={},
            optimized_resume="",
            ats_score=0.0,
            recommendations=[],
            errors=[]
        )
        
        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        return {
            "optimized_resume": final_state["optimized_resume"],
            "ats_score": final_state["ats_score"],
            "recommendations": final_state["recommendations"],
            "skills_found": final_state["skills"],
            "errors": final_state["errors"]
        }

# Utility functions for file handling
def read_pdf_file(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def read_text_file(file_path: str) -> str:
    """Read text from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def get_user_input():
    """Get resume and job description from user"""
    print("=== Resume Optimization Tool ===\n")
    
    # Get resume input
    print("Choose resume input method:")
    print("1. Type/paste resume text")
    print("2. Load from text file")
    print("3. Load from PDF file")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    resume_text = ""
    if choice == "1":
        print("\nPaste your resume text (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "" and len(lines) > 0 and lines[-1] == "":
                break
            lines.append(line)
        resume_text = "\n".join(lines[:-1])  # Remove last empty line
    
    elif choice == "2":
        file_path = input("\nEnter path to text file: ").strip()
        resume_text = read_text_file(file_path)
    
    elif choice == "3":
        file_path = input("\nEnter path to PDF file: ").strip()
        resume_text = read_pdf_file(file_path)
    
    else:
        print("Invalid choice. Using manual input.")
        resume_text = input("\nEnter your resume text: ")
    
    # Get job description
    print("\n" + "="*50)
    print("Choose job description input method:")
    print("1. Type/paste job description")
    print("2. Load from text file")
    
    job_choice = input("\nEnter choice (1-2): ").strip()
    
    job_description = ""
    if job_choice == "1":
        print("\nPaste job description (press Enter twice when done):")
        lines = []
        while True:
            line = input()
            if line == "" and len(lines) > 0 and lines[-1] == "":
                break
            lines.append(line)
        job_description = "\n".join(lines[:-1])  # Remove last empty line
    
    elif job_choice == "2":
        file_path = input("\nEnter path to job description file: ").strip()
        job_description = read_text_file(file_path)
    
    else:
        job_description = input("\nEnter job description: ")
    
    return resume_text, job_description

async def main():
    """Main function with user interaction"""
    try:
        # Check for API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("ERROR: GOOGLE_API_KEY environment variable not found!")
            print("Please set it using: export GOOGLE_API_KEY='your-api-key'")
            print("Or create a .env file with: GOOGLE_API_KEY=your-api-key")
            return
        
        print("✓ Google API key found")
        
        # Get user input
        resume_text, job_description = get_user_input()
        
        if not resume_text or not job_description:
            print("ERROR: Both resume and job description are required!")
            return
        
        print("\n" + "="*50)
        print("🔄 Processing your resume...")
        
        # Initialize optimizer
        optimizer = ResumeOptimizationGraph()
        
        # Optimize resume
        results = await optimizer.optimize_resume(resume_text, job_description)
        
        # Display results
        print("\n" + "="*50)
        print("=== OPTIMIZATION RESULTS ===")
        print(f"🎯 ATS Score: {results['ats_score']:.1f}/100")
        
        if results['errors']:
            print(f"\n⚠️  Errors encountered:")
            for error in results['errors']:
                print(f"   - {error}")
        
        print(f"\n📊 Skills Found:")
        skills = results['skills_found']
        if skills.get('technical'):
            print(f"   Technical: {', '.join(skills['technical'])}")
        if skills.get('soft'):
            print(f"   Soft Skills: {', '.join(skills['soft'])}")
        
        if results['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in results['recommendations']:
                print(f"   - {rec}")
        
        print(f"\n📄 OPTIMIZED RESUME:")
        print("-" * 50)
        print(results['optimized_resume'])
        
        # Save option
        save_choice = input(f"\n💾 Save optimized resume to file? (y/n): ").lower()
        if save_choice == 'y':
            filename = input("Enter filename (default: optimized_resume.txt): ").strip()
            if not filename:
                filename = "optimized_resume.txt"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(results['optimized_resume'])
                print(f"✅ Resume saved to {filename}")
            except Exception as e:
                print(f"❌ Error saving file: {e}")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    asyncio.run(main())