import pytest
import json
from elasticsearch import AsyncElasticsearch
import aioredis


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, response_json_path, index, filename",
    (
            (
                    {"query": "andrea"},
                    "../testdata/responses/search_persons.json",
                    "persons",
                    "persons.json",
            ),
    )
)
async def test_search_persons(
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
    response = await make_get_request(f'/persons/search', params)

    # Проверка результата
    assert response.status == 200

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=index)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id, response_json_path, index, filename",
    (
            (
                    "3c9eef22-b727-4354-80b6-8f836ab5e860",
                    "../testdata/responses/get_person_by_id.json",
                    "persons",
                    "persons.json",
            ),
    )
)
async def test_get_person_by_id(
        es_client: AsyncElasticsearch,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_data,

        person_id: str,
        response_json_path: str,
        index: str,
        filename: str,
):
    await prepare_for_test(index=index, filename=filename)

    # Выполнение запроса
    response = await make_get_request(f'/persons/{person_id}', dict())

    # Проверка результата
    assert response.status == 200

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=index)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id, response_json_path, person_index, person_filename, movies_index, movies_filename",
    (
            (
                    "958acb12-9cd3-4784-b374-42c4fc8face2",
                    "../testdata/responses/get_films_for_person.json",
                    "persons",
                    "persons.json",
                    "movies",
                    "movies.json"
            ),

    )
)
async def test_get_films_for_person(
        es_client: AsyncElasticsearch,
        redis_client: aioredis.Redis,
        prepare_for_test,
        make_get_request,
        delete_data,

        person_id: str,
        response_json_path: str,
        person_index: str,
        person_filename: str,
        movies_index: str,
        movies_filename: str,
):
    await prepare_for_test(index=movies_index, filename=movies_filename)
    await prepare_for_test(index=person_index, filename=person_filename)

    # Выполнение запроса
    response = await make_get_request(f'/persons/{person_id}/film', dict())

    # Проверка результата
    assert response.status == 200

    with open(response_json_path) as expected_response:
        expected = json.load(expected_response)
        assert response.body == expected

    await delete_data(index=person_index)
    await delete_data(index=movies_index)
