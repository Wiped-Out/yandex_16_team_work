import asyncio
from external_api import api_methods
from datetime import datetime


async def main():
    print(datetime.now(), flush=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(api_methods.add_notification())
