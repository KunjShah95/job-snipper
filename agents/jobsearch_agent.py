from services.job_scraper import search_jobs
from typing import Dict, List, Any

def search_jobs_agent(parsed_resume: Dict, search_query: Dict) -> List[Dict]:
    """
    Search for jobs using the real job search service
    
    Args:
        parsed_resume: Parsed resume data for matching
        search_query: Search parameters from UI
        
    Returns:
        List of job dictionaries
    """
    try:
        jobs = search_jobs(parsed_resume, search_query)
        return jobs
    except Exception as e:
        print(f"Job search agent failed: {e}")
        return []

def search_jobs_legacy(jd_text: str) -> List[Dict]:
    """
    Legacy function for backward compatibility
    """
    try:
        # Create basic search query from job description
        search_query = {
            "keywords": jd_text[:100],
            "location": "",
            "experience_level": "Any"
        }
        
        # Create minimal parsed resume
        parsed_resume = {
            "skills": [],
            "experience": [],
            "location": ""
        }
        
        return search_jobs(parsed_resume, search_query)
    except Exception as e:
        print(f"Legacy job search agent failed: {e}")
        return []
