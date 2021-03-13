from scrapinghub import ScrapinghubClient
import os


class ScrapinghubClientWrapper:

    def __init__(self):
        self.client = ScrapinghubClient(os.environ['apikey'])
        self.project = self.client.projects.get(os.environ['project_id'])

    def create_job(self, spider, days=3):
        self.project.jobs.run(spider, job_args={'days': days})

    def get_job_items(self, job_id):
        return self.project.jobs.get(job_id).items.list()

    def get_list_of_spiders(self):
        return [spider_id['id'] for spider_id in self.project.spiders.list()]

    def get_list_of_jobs_for_spider(self, spider):
        return [job['key']
                for job in self.project.spiders.get(spider).jobs.iter()]
