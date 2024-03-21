import subprocess
import os

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
    
    