import scrapy
from scrapy.http.request import Request
import re
import pytz
from api.utils.date_utils import calcular_data
from api.domain.models.dao.review import InsertReviewModel as _InsertReviewModel
from api.services.repositories.reviews_repository import ReviewsRespository

class GoogleSpider(scrapy.Spider):
    
    name = "google"
    
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        'referer': None
    }
    
    def __init__(self, **kwargs):
        super().__init__(name=self.name, **kwargs)
        self.base_url: str = kwargs.get('base_url')
        self.bussiness_id: int = kwargs.get('bussiness_id')
        self.review_buffer = []

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
        if next_page_token:
            token_in_url = response.url.split("next_page_token:")[1].split(",")[0]
            next_page_url = response.url.replace(f"next_page_token:{token_in_url}", f"next_page_token:{next_page_token}")
            yield Request(url=next_page_url, headers=self.HEADERS, callback=self.parse)

    def parse_reviews(self, response):
        all_reviews = response.xpath('//*[@id="reviewSort"]/div/div[2]/div')
        
        for review in all_reviews:       
            reviewer = review.css('div.TSUbDb a::text').extract_first()
            description = review.xpath('.//span[@class="review-full-text"]/text()').extract_first() or review.css('.Jtu6Td span::text').extract_first() or ''
            review_rating = review.xpath('.//div[@class="PuaHbe"]/span[1]/@aria-label').extract_first()
            if review_rating:
                review_rating = float(re.search(r'(\d.\d)', review_rating.replace(",", ".")).group(1))

            review_date = review.xpath('.//span[@class="dehysf lTi8oc"]/text()').extract_first()

            self.review_buffer.append({
                'reviewer': reviewer,
                'description': description,
                'review_rating': review_rating,
                'review_date': review_date
            })
            
            if len(self.review_buffer) >= 50 or not all_reviews:
                self.insert_reviews_to_database()
            
            yield

    def insert_reviews_to_database(self):
        if self.review_buffer:
            reviews_to_insert = self.review_buffer[:]
            self.review_buffer.clear()
            
            formatted_reviews = [_InsertReviewModel(
                author_name=review_data['reviewer'],
                description=review_data['description'],
                fk_bussiness_id=self.bussiness_id,
                rating=review_data['review_rating'],
                time=calcular_data(review_data['review_date']).astimezone(pytz.timezone('America/Sao_Paulo')).isoformat()
            ) for review_data in reviews_to_insert]
            
            ReviewsRespository().insert_reviews(formatted_reviews)
