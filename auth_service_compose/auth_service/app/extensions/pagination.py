from flask_restx import reqparse
from pydantic import BaseModel

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, location='args', default=1)
pagination_parser.add_argument('per_page', type=int, location='args', default=20)


class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: list

    def prepare_items_for_answer(self, model):
        self.items = [model(**item.dict()).dict() for item in self.items]
