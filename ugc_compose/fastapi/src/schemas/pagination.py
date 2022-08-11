from typing import Optional

from fastapi import Query


class PaginatedParams:
    def __init__(self,
                 page_size: Optional[int] = Query(default=50, le=100, alias="page[size]"),
                 page: Optional[int] = Query(default=1, alias="page[number]")
                 ):
        self.page_size = page_size
        self.page = page
