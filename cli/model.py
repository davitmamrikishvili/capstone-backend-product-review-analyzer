from enum import Enum


class Order(str, Enum):
    relevancy = "relevancy"
    submission_desc = "submission-desc"
    helpful = "helpful"
    rating_desc = "rating-desc"
    rating_asc = "rating-asc"
