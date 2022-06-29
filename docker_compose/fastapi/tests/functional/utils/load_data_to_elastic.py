import json
from settings import settings
from elasticsearch import AsyncElasticsearch


async def load_data_to_elastic():
    indexes_data = (
        ('movies', 'testdata/movies_data.json'),
        ('persons', 'testdata/persons_data.json'),
        ('genres', 'testdata/genres_data.json'),
    )
    es = AsyncElasticsearch(
        hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}']
    )
    for index, path_to_data in indexes_data:
        with open(path_to_data) as data:
            loaded_json = json.load(data)
            items = loaded_json['items']
            items_for_bulk = []
            for item in items:
                items_for_bulk += \
            [
                {'index': {
                    '_index': index,
                    '_id': item['id']
                    }
                },

                item
             ]

            await es.bulk(index=index, body=items_for_bulk)

    await es.close()
