from dataclasses import dataclass, asdict
from typing import Tuple

from elasticsearch import Elasticsearch
from models import ElasticIndexModel
from state_controller import StateController


@dataclass
class ElasticsearchLoader:
    """Класс для загрузки данных в ElasticSearch"""
    es: Elasticsearch
    es_sc: StateController
    page_size: int = 500

    def load(self, data: Tuple[ElasticIndexModel]):
        ready_data = []
        self.es_sc.get_state()

        for i in range(len(data)):
            ready_data += [{'index': {'_index': 'movies',
                                      '_id': str(data[i].id)}},
                           asdict(data[i])]

        ready_data = ready_data[self.es_sc.state * 2:]

        while len(ready_data) > 0:
            if self.page_size * 2 > len(ready_data):
                ready_data, list_to_load = (), ready_data
            else:
                ready_data, list_to_load = ready_data[self.page_size * 2:], \
                                           (ready_data[:self.page_size * 2])

            self.es.bulk(body=list_to_load)

            self.es_sc.state += self.page_size
            self.es_sc.set_state()
