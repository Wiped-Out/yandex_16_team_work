import pytest
import json
from elasticsearch import AsyncElasticsearch
import aioredis
from http import HTTPStatus


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "genre_id, response_json_path, index, filename",
    (
            (
                    "c34a40c0-24ee-40db-9c47-58045917841a",
                    "testdata/responses/get_genre_by_id.json",
                    "genres",
                    "genres.json",
            ),
    )
)
async def test_get_genre_by_id(
        es_client: AsyncElasticsearch,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_data,

        genre_id: str,
        response_json_path: str,
        index: str,
        filename: str,
):
    await prepare_for_test(index=index, filename=filename)

    # Выполнение запроса
    response = await make_get_request(f'/genres/{genre_id}', dict())

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=index)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_json_path, index, filename",
    (
            (
                    "testdata/responses/get_genres.json",
                    "genres",
                    "genres.json",
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
    response = await make_get_request('/genres', dict())

    # Проверка результата
    assert response.status == HTTPStatus.OK

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=index)
