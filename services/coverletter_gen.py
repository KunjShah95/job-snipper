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
    Generate a tailored cover letter
    """
    try:
        rewritten_resume = resume_json.get(
            "rewritten_text", resume_json.get("raw_text", "")
        )
        prompt = f"""
        Generate a {tone} cover letter for the following job description:

        Job Description:
        {jd_text}

        Candidate Resume:
        {rewritten_resume}
        """
        cover_letter = llm.call(prompt)
        return cover_letter
    except Exception as e:
        print(f"Cover letter generation failed: {e}")
        return ""
