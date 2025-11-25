from dotenv import load_dotenv
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_utils import generate_text

load_dotenv()


class LLMWrapper:
    """Thin wrapper that exposes .call(prompt) to match previous usage with multi-model support."""

    def __init__(self, temperature: float = 0.3, max_tokens: int = 2048):
        self.temperature = temperature
        self.max_tokens = max_tokens

    def call(self, prompt: str, preferred_provider: str = None) -> str:
        """
        Generate text using multi-model LLM with automatic fallback
        
        Args:
            prompt: The prompt to send to the LLM
            preferred_provider: Preferred provider (groq, gemini, openai, anthropic)
        
        Returns:
            Generated text response
        """
        try:
            return generate_text(
                prompt, 
                temperature=self.temperature, 
                max_tokens=self.max_tokens,
                preferred_provider=preferred_provider
            )
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")


# Create default wrapper instance
llm = LLMWrapper()


def generate_cover_letter(resume_json, jd_text, tone="formal"):
    """
    Generate a tailored cover letter with improved prompts and validation
    """
    try:
        # Extract key information from resume
        name = resume_json.get("name", "Candidate")
        email = resume_json.get("email", "")
        phone = resume_json.get("phone", "")
        location = resume_json.get("location", "")
        skills = resume_json.get("skills", [])
        experience = resume_json.get("experience", [])
        
        # Get the best available resume text
        rewritten_resume = resume_json.get("rewritten_text", resume_json.get("raw_text", ""))
        
        if not rewritten_resume or len(rewritten_resume.strip()) < 50:
            return "Error: Insufficient resume content to generate cover letter. Please ensure your resume has been properly parsed."
        
        # Create enhanced prompt
        prompt = f"""
        You are a professional career coach writing a {tone} cover letter. 
        
        JOB DESCRIPTION:
        {jd_text}
        
        CANDIDATE INFORMATION:
        Name: {name}
        Email: {email}
        Phone: {phone}
        Location: {location}
        Key Skills: {', '.join(skills[:10]) if skills else 'Not specified'}
        Experience: {', '.join(experience[:5]) if experience else 'Not specified'}
        
        RESUME CONTENT:
        {rewritten_resume}
        
        INSTRUCTIONS:
        1. Write a professional, {tone} cover letter that:
           - Addresses the hiring manager directly
           - Highlights relevant skills and experience from the resume
           - Shows enthusiasm for the specific role and company
           - Includes specific examples of achievements
           - Demonstrates knowledge of the role requirements
           - Ends with a strong call to action
        
        2. Format the letter properly with:
           - Professional greeting
           - 3-4 well-structured paragraphs
           - Professional closing
           - Include candidate contact information
        
        3. Make it personalized and specific to this job, not generic.
        
        4. Keep it concise but impactful (300-500 words).
        
        Generate the complete cover letter now:
        """
        
        cover_letter = llm.call(prompt)
        
        # Validate the response
        if not cover_letter or len(cover_letter.strip()) < 100:
            return "Error: Cover letter generation failed. Please try again or check your API configuration."
        
        # Basic quality checks
        if "Dear" not in cover_letter and "To Whom It May Concern" not in cover_letter:
            cover_letter = f"Dear Hiring Manager,\n\n{cover_letter}"
        
        if not cover_letter.strip().endswith(("Sincerely", "Best regards", "Thank you")):
            cover_letter += "\n\nSincerely,\n" + (name if name else "Candidate")
        
        return cover_letter.strip()
        
    except Exception as e:
        print(f"Cover letter generation failed: {e}")
        return f"Error generating cover letter: {str(e)}. Please check your API configuration and try again."
