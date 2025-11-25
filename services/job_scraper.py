import pandas as pd
from typing import Dict, List, Any
from services.real_job_search import get_job_search

def search_jobs(parsed_resume: Dict, search_query: Dict, max_results: int = 20) -> List[Dict]:
    """
    Search for real jobs using multiple APIs with fallback to enhanced mock data
    
    Args:
        parsed_resume: Parsed resume data for matching
        search_query: Search parameters including keywords, location, etc.
        max_results: Maximum number of results to return
        
    Returns:
        List of job dictionaries with real data
    """
    try:
        job_search = get_job_search()
        jobs = job_search.search_jobs(parsed_resume, search_query, max_results)
        return jobs
    except Exception as e:
        print(f"Job search failed: {e}")
        # Return minimal fallback data
        return [{
            "title": "Software Engineer",
            "company": "Tech Company",
            "location": "Remote",
            "description": "Software engineering position",
            "url": "#",
            "match_score": 50,
            "salary": "Not specified",
            "remote": True,
            "hybrid": False,
            "days_ago": 1,
            "source": "Fallback"
        }]

def search_jobs_legacy(jd_text: str, max_results: int = 10) -> pd.DataFrame:
    """
    Legacy function for backward compatibility
    """
    try:
        # Create a basic search query from job description text
        search_query = {
            "keywords": jd_text[:100],  # Use first 100 chars as keywords
            "location": "",
            "experience_level": "Any"
        }
        
        # Create minimal parsed resume
        parsed_resume = {
            "skills": [],
            "experience": [],
            "location": ""
        }
        
        jobs = search_jobs(parsed_resume, search_query, max_results)
        return pd.DataFrame(jobs)
    except Exception as e:
        print(f"Legacy job search failed: {e}")
        return pd.DataFrame()
