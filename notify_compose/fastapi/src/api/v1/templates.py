from typing import Optional

from fastapi import APIRouter, Depends
from services.templates import TemplatesService, get_templates_service
from schemas.v1_schemas import Template
from models.models import AddTemplate

router = APIRouter()


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
    templates = await templates_service.get_templates()
    return [Template(**template.dict()) for template in templates]


@router.get(
    path='/{template_id}',
    description='Get template',
    response_model=Optional[Template],
)
async def get_template(
        template_id: str,
        templates_service: TemplatesService = Depends(get_templates_service),
):
    template = await templates_service.get_template(template_id=template_id)
    if not template:
        return None
    return Template(**template.dict())


@router.delete(
    path='/{template_id}',
    description='Delete template',
)
async def delete_template(
        template_id: str,
        templates_service: TemplatesService = Depends(get_templates_service),
):
    await templates_service.delete_template(template_id=template_id)
    return {"message": "Template deleted"}
