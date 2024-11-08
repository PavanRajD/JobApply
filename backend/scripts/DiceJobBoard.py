import json
from bs4 import BeautifulSoup
import requests

from JobBoard import JobBoard

class DiceJobBoard(JobBoard):
    def __init__(self):
        pass
        
    def fetch_jobs(self, job_info):
        try:
            headers = {'X-Api-Key': '1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8'}
            job_id_list = []

            for keyword in job_info['keywords'].split(","):
                for loc in job_info['locations'].split(","):
                    for offset in range(1, 100, 1):
                        params = {
                            'q': keyword, 'countryCode2': loc, 'page': str(offset),
                            'filters.postedDate': job_info['job_posted'],
                            'filters.employmentType': job_info['job_type'],
                            'pageSize': '50', 'fields': 'guid|title|companyName'
                        }
                        
                        response = requests.get('https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search', params=params, headers=headers)
                        if response.status_code == 200:
                            data = response.json()
                            for job in data['data']:
                                job_id_list.append(job['guid'])
                            
                            if len(data['data']) < 50:
                                break

            return job_id_list
        except Exception as e:
            raise e

    def get_job_details(self, job_id):
        try:
            job_page = requests.get(f'https://www.dice.com/job-detail/{job_id}')
            soup = BeautifulSoup(job_page.text, 'html.parser')
            details_script = soup.find(id='__NEXT_DATA__')
            details = json.loads(details_script.text)
            items = list(details['props']['pageProps']['initialState']['api']['queries'].items())
            job_details = items[0][1]

            recruiter_email = job_details['data']['applicationDetail']['email']
            if recruiter_email:
                recruiter_name = job_details['data']['applicationDetail']['email'].split('@')[0]
                skills_list = [skill['name'] for skill in job_details['data']['skills']]
                job_info = {
                    'id': job_id,
                    'title': job_details['data']['titleSanitized'],
                    'company': items[1][1]['data']['employerBrandingAssets']['company_name'],
                    'recruiter_email': recruiter_email,
                    'skills': ", ".join(skills_list),
                    'skills_present': len(skills_list) > 0,
                    'recruiter_name': recruiter_name,
                    'jd': job_details['data']['description']
                }
                return job_info
            return None
        except Exception as e:
            raise e