import json
import logging
import os
import subprocess
from api.usecases.reviews_usecases import insert_reviews_to_database

from api.domain.models.dao.scrapy_review import ScrapyReviewsModel


def run_google_scraper(bussiness_id: int, base_url: str):
    if os.path.exists("../tmp/reviews.json"):
        os.remove("../tmp/reviews.json")
        
    command = [
        "scrapy", "crawl", "google",
        "-a", f"base_url={base_url}",
        "-a", f"bussiness_id={bussiness_id}",
        "-o", "../tmp/reviews.json"
    ]
    subprocess.run(command)
    logging.info("\n\n\n***********************\n\nGOOGLE SCRAPER FINISHED\n\n***********************\\n\n\n")
    
    if os.path.exists("../tmp/reviews.json"):
        with open("../tmp/reviews.json", encoding="utf-8") as reviews_file:
            data = json.load(reviews_file)
            print(data)
            if type(data) == list:
                reviews = [ScrapyReviewsModel(**review) for review in data]
                insert_reviews_to_database(reviews)
            return
    


    
    