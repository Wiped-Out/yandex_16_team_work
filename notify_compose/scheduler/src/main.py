import argparse
import asyncio

from external_api import api_methods
from templates.templates import TemplateNamesEnum, templates

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scheduler')
    parser.add_argument(
        'template_name',
        type=TemplateNamesEnum,
        choices=list(TemplateNamesEnum),
    )

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        api_methods.add_notification(
            notification_template=templates[args.template_name],
        )
    )
