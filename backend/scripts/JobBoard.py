from abc import ABC, abstractmethod


class JobBoard(ABC):
    @abstractmethod
    def fetch_jobs(self, job_info):
        pass
    
    @abstractmethod
    def get_job_details(self, job_id):
        pass