import json
from settings import settings
from elasticsearch import AsyncElasticsearch


async def create_indexes_in_es():
    indexes_names_mappings = (
        ('movies','testdata/movies.json'),
        ('persons', 'testdata/persons.json'),
        ('genres', 'testdata/genres.json'),
    )
    es = AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )
    for index_name, path_to_json in indexes_names_mappings:
        with open(path_to_json) as index_mapping_file:
            loaded_json = json.load(index_mapping_file)
            await es.indices.create(index=index_name,body=loaded_json)

    await es.close()
