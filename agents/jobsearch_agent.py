from services.job_scraper import search_jobs

def search_jobs_agent(jd_text):
    """
    Return jobs relevant to the JD
    """
    try:
        jobs_df = search_jobs(jd_text)
        return jobs_df
    except Exception as e:
        print(f"Job search agent failed: {e}")
        return None
