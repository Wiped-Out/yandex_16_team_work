import pytest
import json
from elasticsearch import AsyncElasticsearch
import aioredis


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, response_json_path, index, filename",
    (
            (
                    {"query": "last"},
                    "../testdata/responses/search_films.json",
                    "movies",
                    "movies.json",
            ),
    )
)
async def test_search_films(
        es_client: AsyncElasticsearch,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_data,

        params: dict,
        response_json_path: str,
        index: str,
        filename: str,
):
    await prepare_for_test(index=index, filename=filename)

    # Выполнение запроса
    response = await make_get_request(f'/films/search', params)

    # Проверка результата
    assert response.status == 200

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=index)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "film_id, response_json_path, index, filename",
    (
            (
                    "4415f91e-53db-4579-a757-d4023b1fa604",
                    "../testdata/responses/get_film_by_id.json",
                    "movies",
                    "movies.json",
            ),
    )
)
async def test_get_film_by_id(
        es_client: AsyncElasticsearch,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_data,

        film_id: str,
        response_json_path: str,
        index: str,
        filename: str,
):
    await prepare_for_test(index=index, filename=filename)

    # Выполнение запроса
    response = await make_get_request(f'/films/{film_id}', dict())

    # Проверка результата
    assert response.status == 200

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=index)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_json_path, index, filename",
    (
            (
                    "../testdata/responses/get_films.json",
                    "movies",
                    "movies.json",
            ),

    )
)
async def test_get_all_films(
        es_client: AsyncElasticsearch,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_data,

        response_json_path: str,
        index: str,
        filename: str,
):
    await prepare_for_test(index=index, filename=filename)

    # Выполнение запроса
    response = await make_get_request('/films', dict())

    # Проверка результата
    assert response.status == 200

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=index)
