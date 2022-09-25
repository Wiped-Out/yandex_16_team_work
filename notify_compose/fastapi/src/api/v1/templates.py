from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends
from models.models import AddTemplate
from pydantic import UUID4
from schemas.v1_schemas import Created, Template
from services.templates import TemplatesService, get_templates_service

router = APIRouter()


@router.post(
    path='',
    description='Add template',
    response_model=Created,
    status_code=HTTPStatus.CREATED,
)
async def add_template(
        template: AddTemplate,
        templates_service: TemplatesService = Depends(get_templates_service),  # noqa: WPS404, B008
):
    item_id = await templates_service.add_template(template=template)
    return Created(id=item_id)


@router.get(
    path='',
    description='Get templates',
    response_model=list[Template],
    status_code=HTTPStatus.OK,
)
async def get_templates(
        templates_service: TemplatesService = Depends(get_templates_service),  # noqa: WPS404, B008
):
    templates = await templates_service.get_templates()
    return [Template(**template.dict()) for template in templates]


@router.get(
    path='/{template_id}',
    description='Get template',
    response_model=Optional[Template],
    status_code=HTTPStatus.OK,
)
async def get_template(
        template_id: UUID4,
        templates_service: TemplatesService = Depends(get_templates_service),  # noqa: WPS404, B008
):
    template = await templates_service.get_template(template_id=template_id)
    if not template:
        return None
    return Template(**template.dict())


@router.delete(
    path='/{template_id}',
    description='Delete template',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_template(
        template_id: UUID4,
        templates_service: TemplatesService = Depends(get_templates_service),  # noqa: WPS404, B008
):
    await templates_service.delete_template(template_id=template_id)
