from functools import lru_cache


class TemplatesService:
    pass


@lru_cache()
def get_templates_service() -> TemplatesService:
    return TemplatesService()
