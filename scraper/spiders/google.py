import scrapy
from scrapy.http.request import Request
import re
from api.utils.url_utils import mount_bussiness_review_url as _mount_bussiness_review_url 

class GoogleSpider(scrapy.Spider):
    
    name = "google"
    
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        'referer': None
    }
    
    def __init__(self, **kwargs):
        super().__init__(name=self.name, **kwargs)
        self.base_url = kwargs.get('base_url')
        self.bussiness_maps_id = kwargs.get('bussiness_maps_id')
    
    def start_requests(self):
        yield Request(url=self.base_url, headers=self.HEADERS, callback=self.parse_first_page)
        
    def parse_first_page(self, response):
        lrd = response.xpath('.//span[@class="hqzQac"]/span/a/@data-fid').extract_first()
        ajax_url = f"https://www.google.com/async/reviewDialog?async=feature_id:{lrd},review_source:All%20reviews,sort_by:newestFirst,is_owner:false,filter_text:,associated_topic:,next_page_token:,async_id_prefix:,_pms:s,_fmt:pc"
        yield Request(url=ajax_url, headers=self.HEADERS, callback=self.parse)
    
    def parse(self, response):        
        # Chama a função que extrai as reviews desta primeira página
        yield from self.parse_reviews(response)

        # Se houver um token de próxima página, faça outra solicitação para a próxima página
        next_page_token = response.xpath('//*[@id="reviewSort"]/div/div[2]/@data-next-page-token').extract_first()
        print(f"\n\n *********** next_page_token ************* \n\n{next_page_token}\n\n ***************** \n\n")
        if next_page_token:
            token_in_url = response.url.split("next_page_token:")[1].split(",")[0]
            next_page_url = response.url.replace(f"next_page_token:{token_in_url}", f"next_page_token:{next_page_token}")
            print(f"\n\n *********** next_page_url ************* \n\n{next_page_url}\n\n ***************** \n\n")
            yield Request(url=next_page_url, headers=self.HEADERS, callback=self.parse)

    def parse_reviews(self, response):
        all_reviews = response.xpath('//*[@id="reviewSort"]/div/div[2]/div')
        
        print(f"\n\n *********** all_reviews ************* \n\n{all_reviews}\n\n ***************** \n\n")
        
        for review in all_reviews:       
            reviewer = review.css('div.TSUbDb a::text').extract_first()
            print(f"\n\n *********** reviewer ************* \n\n{reviewer}\n\n ***************** \n\n") 
            description = review.xpath('.//span[@class="review-full-text"]/text()').extract_first()
            if description is None:
                description = review.css('.Jtu6Td span::text').extract_first()
                if description is None:
                    description = ''
            print(f"\n\n *********** description ************* \n\n{description}\n\n ***************** \n\n")
            review_rating = review.xpath('.//div[@class="PuaHbe"]/span[1]/@aria-label').extract_first()
            print(f"\n\n *********** review_rate_raw ************* \n\n{review_rating}\n\n ***************** \n\n")
            if review_rating is not None:
                review_rating = review_rating.replace(",", ".")
                review_rating = float(re.search(r'(\d.\d)', review_rating).group(1))
            
            review_date = review.xpath('.//span[@class="dehysf lTi8oc"]/text()').extract_first()
            
            yield {
                "reviewer": reviewer,
                "description": description,
                "rating": review_rating,
                "date": review_date
            } 
