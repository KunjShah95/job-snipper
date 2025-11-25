"""
Real Job Search Service
Integrates with multiple job search APIs to provide real-world job data
"""

import os
import requests
import time
import json
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class RealJobSearch:
    """
    Multi-source job search service with caching and fallback mechanisms
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 3600  # 1 hour cache
        self.rate_limits = {
            'adzuna': {'calls': 0, 'reset_time': time.time() + 3600},
            'rapidapi': {'calls': 0, 'reset_time': time.time() + 3600}
        }
        
        # API configurations
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY')
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
        # Check which APIs are available
        self.has_adzuna = bool(self.adzuna_app_id and self.adzuna_app_key)
        self.has_rapidapi = bool(self.rapidapi_key)
        
        if not self.has_adzuna and not self.has_rapidapi:
            print("Warning: No job search API keys configured. Using fallback data.")
    
    def search_jobs(
        self, 
        parsed_resume: Dict, 
        search_query: Dict,
        max_results: int = 20
    ) -> List[Dict]:
        """
        Search for jobs using available APIs with fallback to mock data
        
        Args:
            parsed_resume: Parsed resume data
            search_query: Search parameters from UI
            max_results: Maximum number of results to return
            
        Returns:
            List of job dictionaries
        """
        # Create cache key
        cache_key = f"{hash(str(search_query))}_{max_results}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        jobs = []
        
        # Try Adzuna API first (best quality data)
        if self.has_adzuna and len(jobs) < max_results:
            try:
                adzuna_jobs = self._search_adzuna(search_query, max_results - len(jobs))
                jobs.extend(adzuna_jobs)
            except Exception as e:
                print(f"Adzuna API error: {e}")
        
        # Try RapidAPI JSearch as backup
        if self.has_rapidapi and len(jobs) < max_results:
            try:
                rapidapi_jobs = self._search_rapidapi(search_query, max_results - len(jobs))
                jobs.extend(rapidapi_jobs)
            except Exception as e:
                print(f"RapidAPI error: {e}")
        
        # If no APIs available or insufficient results, use enhanced mock data
        if not jobs:
            jobs = self._generate_enhanced_mock_jobs(search_query, max_results, parsed_resume)
        
        # Calculate match scores based on resume
        jobs = self._calculate_match_scores(jobs, parsed_resume)
        
        # Cache results
        self.cache[cache_key] = (jobs, time.time())
        
        return jobs[:max_results]
    
    def _search_adzuna(self, search_query: Dict, max_results: int) -> List[Dict]:
        """Search jobs using Adzuna API"""
        if not self.has_adzuna:
            return []
        
        # Check rate limits
        if self._is_rate_limited('adzuna'):
            return []
        
        base_url = "https://api.adzuna.com/v1/api/jobs"
        params = {
            'app_id': self.adzuna_app_id,
            'app_key': self.adzuna_app_key,
            'results_per_page': min(max_results, 50),
            'what': search_query.get('keywords', ''),
            'where': search_query.get('location', ''),
            'content-type': 'application/json'
        }
        
        # Add filters
        if search_query.get('experience_level'):
            params['category'] = self._map_experience_to_adzuna(search_query['experience_level'])
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self.rate_limits['adzuna']['calls'] += 1
            
            jobs = []
            for job in data.get('results', []):
                jobs.append({
                    'title': job.get('title', ''),
                    'company': job.get('company', {}).get('display_name', ''),
                    'location': job.get('location', {}).get('display_name', ''),
                    'description': job.get('description', ''),
                    'url': job.get('redirect_url', ''),
                    'salary': self._format_salary(job.get('salary_min'), job.get('salary_max')),
                    'remote': 'remote' in job.get('description', '').lower(),
                    'hybrid': 'hybrid' in job.get('description', '').lower(),
                    'days_ago': self._calculate_days_ago(job.get('created')),
                    'source': 'Adzuna'
                })
            
            return jobs
            
        except Exception as e:
            print(f"Adzuna API request failed: {e}")
            return []
    
    def _search_rapidapi(self, search_query: Dict, max_results: int) -> List[Dict]:
        """Search jobs using RapidAPI JSearch"""
        if not self.has_rapidapi:
            return []
        
        # Check rate limits
        if self._is_rate_limited('rapidapi'):
            return []
        
        url = "https://jsearch.p.rapidapi.com/search"
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        params = {
            'query': search_query.get('keywords', ''),
            'page': '1',
            'num_pages': '1',
            'date_posted': 'all',
            'remote_jobs_only': 'false'
        }
        
        if search_query.get('location'):
            params['location'] = search_query['location']
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self.rate_limits['rapidapi']['calls'] += 1
            
            jobs = []
            for job in data.get('data', []):
                jobs.append({
                    'title': job.get('job_title', ''),
                    'company': job.get('employer_name', ''),
                    'location': job.get('job_location', ''),
                    'description': job.get('job_description', ''),
                    'url': job.get('job_apply_link', ''),
                    'salary': self._format_salary(job.get('job_salary_min'), job.get('job_salary_max')),
                    'remote': job.get('job_is_remote', False),
                    'hybrid': 'hybrid' in job.get('job_description', '').lower(),
                    'days_ago': self._calculate_days_ago(job.get('job_posted_at_datetime_utc')),
                    'source': 'JSearch'
                })
            
            return jobs
            
        except Exception as e:
            print(f"RapidAPI request failed: {e}")
            return []
    
    def _generate_enhanced_mock_jobs(self, search_query: Dict, max_results: int, parsed_resume: Dict) -> List[Dict]:
        """Generate enhanced mock jobs based on search criteria and resume"""
        keywords = search_query.get('keywords', '').lower()
        location = search_query.get('location', '').lower()
        
        # Base job templates
        job_templates = [
            {
                'title': f"Senior {keywords.title() if keywords else 'Software Engineer'}",
                'company': 'TechCorp Inc.',
                'location': location.title() if location else 'San Francisco, CA',
                'description': f"Join our team as a Senior {keywords.title() if keywords else 'Software Engineer'}. We're looking for passionate developers to build innovative solutions.",
                'salary': '$120,000 - $150,000',
                'remote': True,
                'hybrid': False
            },
            {
                'title': f"{keywords.title() if keywords else 'Software Engineer'} - Remote",
                'company': 'StartupXYZ',
                'location': 'Remote',
                'description': f"Fully remote position for a {keywords.title() if keywords else 'Software Engineer'}. Work with cutting-edge technologies.",
                'salary': '$90,000 - $130,000',
                'remote': True,
                'hybrid': False
            },
            {
                'title': f"Lead {keywords.title() if keywords else 'Developer'}",
                'company': 'Enterprise Solutions',
                'location': location.title() if location else 'New York, NY',
                'description': f"Lead a team of {keywords.title() if keywords else 'developers'} in building scalable applications.",
                'salary': '$140,000 - $180,000',
                'remote': False,
                'hybrid': True
            }
        ]
        
        # Generate variations
        jobs = []
        for i in range(max_results):
            template = job_templates[i % len(job_templates)]
            job = template.copy()
            job.update({
                'title': f"{job['title']} {i+1}" if i > 2 else job['title'],
                'company': f"{job['company']} {i+1}" if i > 2 else job['company'],
                'url': f"https://example.com/job/{i+1}",
                'days_ago': i % 7,
                'source': 'Mock Data'
            })
            jobs.append(job)
        
        return jobs
    
    def _calculate_match_scores(self, jobs: List[Dict], parsed_resume: Dict) -> List[Dict]:
        """Calculate match scores based on resume skills and experience"""
        resume_skills = [skill.lower() for skill in parsed_resume.get('skills', [])]
        resume_experience = parsed_resume.get('experience', [])
        
        for job in jobs:
            score = 0
            
            # Skills matching (40% of score)
            job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
            matched_skills = [skill for skill in resume_skills if skill in job_text]
            if resume_skills:
                skill_score = (len(matched_skills) / len(resume_skills)) * 40
                score += min(skill_score, 40)
            
            # Experience matching (30% of score)
            if any(exp in job_text for exp in ['senior', 'lead', 'principal']):
                if any(exp in ' '.join(resume_experience).lower() for exp in ['senior', 'lead', 'principal']):
                    score += 30
            else:
                score += 20  # Entry/mid level match
            
            # Location matching (20% of score)
            if job.get('remote', False):
                score += 20
            elif parsed_resume.get('location', '').lower() in job.get('location', '').lower():
                score += 20
            
            # Company size/type matching (10% of score)
            if any(keyword in job.get('company', '').lower() for keyword in ['startup', 'tech', 'software']):
                score += 10
            
            job['match_score'] = min(int(score), 100)
            job['matched_skills'] = matched_skills[:5]  # Top 5 matched skills
        
        return jobs
    
    def _is_rate_limited(self, api: str) -> bool:
        """Check if API is rate limited"""
        if api not in self.rate_limits:
            return False
        
        current_time = time.time()
        rate_info = self.rate_limits[api]
        
        # Reset counter if reset time has passed
        if current_time > rate_info['reset_time']:
            rate_info['calls'] = 0
            rate_info['reset_time'] = current_time + 3600
        
        # Check limits (conservative limits)
        if api == 'adzuna':
            return rate_info['calls'] >= 100  # 100 calls per hour
        elif api == 'rapidapi':
            return rate_info['calls'] >= 50   # 50 calls per hour
        
        return False
    
    def _map_experience_to_adzuna(self, experience_level: str) -> str:
        """Map experience level to Adzuna category"""
        mapping = {
            'Entry Level': 'entry-level',
            'Mid Level': 'mid-level', 
            'Senior Level': 'senior-level',
            'Executive': 'executive'
        }
        return mapping.get(experience_level, '')
    
    def _format_salary(self, min_sal: Optional[int], max_sal: Optional[int]) -> str:
        """Format salary range"""
        if not min_sal and not max_sal:
            return "Not specified"
        
        if min_sal and max_sal:
            return f"${min_sal:,} - ${max_sal:,}"
        elif min_sal:
            return f"${min_sal:,}+"
        else:
            return f"Up to ${max_sal:,}"
    
    def _calculate_days_ago(self, date_str: Optional[str]) -> int:
        """Calculate days since job was posted"""
        if not date_str:
            return 0
        
        try:
            # Handle different date formats
            if 'T' in date_str:
                job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                job_date = datetime.strptime(date_str, '%Y-%m-%d')
            
            return (datetime.now() - job_date).days
        except:
            return 0


# Global instance
_job_search_instance = None

def get_job_search() -> RealJobSearch:
    """Get or create the global job search instance"""
    global _job_search_instance
    if _job_search_instance is None:
        _job_search_instance = RealJobSearch()
    return _job_search_instance
