from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_google_scraper(base_url: str, bussiness_id: int):
    process = CrawlerProcess(get_project_settings())
    process.crawl("google", base_url=base_url, bussiness_id=bussiness_id)
    process.start()