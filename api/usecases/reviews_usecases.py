import logging
from fastapi.encoders import jsonable_encoder as _json_encoder
from api.domain.models.dao.review import \
    InsertReviewModel as _InsertReviewModel
from api.domain.models.dao.review import ReviewModel as _ReviewModel
from api.domain.models.dao.scrapy_review import \
    ScrapyReviewsModel as _ScrapyReviewsModel
from api.services.repositories.reviews_repository import ReviewsRespository

__reviews_repository = ReviewsRespository()

def insert_reviews_to_database(json_reviews: list[_ScrapyReviewsModel]) -> list[_ReviewModel]:
    reviews_list = json_reviews
    reviews_to_insert = [_InsertReviewModel(
        author_name=review.reviewer,
        description=review.description,
        rating=review.review_rating,
        time=review.review_date,
        fk_bussiness_id=review.bussiness_id
    ) for review in reviews_list]
        
    try:
        __reviews_repository.insert_reviews(_json_encoder(reviews_to_insert))
    except Exception as e:
        logging.error("Error occured while inserting reviews: ", e)
        raise e