from typing import Optional

from fastapi import APIRouter, Depends
from services.templates import TemplatesService, get_templates_service
from pydantic import BaseModel
from schemas.v1_schemas import Template

router = APIRouter()


class TemplateFieldItem(BaseModel):
    name: str
    url: str
    body: dict
    headers: dict


class AddTemplate(BaseModel):
    body: str
    type: str
    fields: list[TemplateFieldItem]


@router.post(
    path='',
    description='Add template',
)
async def add_template(
        template: AddTemplate,
        templates_service: TemplatesService = Depends(get_templates_service),
):
    # todo
    pass


@router.get(
    path='',
    description='Get templates',
    response_model=list[Template],
)
async def get_templates(
        templates_service: TemplatesService = Depends(get_templates_service),
):
    # todo
    pass


@router.get(
    path='/{template_id}',
    description='Get template',
    response_model=Optional[Template],
)
async def get_template(
        template_id: str,
        templates_service: TemplatesService = Depends(get_templates_service),
):
    # todo
    pass


@router.delete(
    path='/{template_id}',
    description='Delete template',
)
async def delete_template(
        templates_service: TemplatesService = Depends(get_templates_service),
):
    # todo
    pass
