import asyncio
from glob import glob
import pytest


def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture) for fixture in glob("fixtures/*.py") if "__" not in fixture
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def prepare_for_test(
        create_table,
        load_data,
        flush_redis,
):
    async def inner(table_name: str, filename: str):
        await create_table(table=table_name)
        await load_data(table=table_name, filename=filename)
        await asyncio.sleep(1)
        await flush_redis()

    return inner
