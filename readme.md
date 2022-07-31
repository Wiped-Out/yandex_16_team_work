Если вы будете заполнять бд через наш скрипт для фейковых данных, то раскомментите 9-10 строчку в docker_compose/docker-compose.yaml


Для проверки задания нужно:\
Запустить rename_script.py | 
Сделать свои .env наподобии .env.sample или переимеиновать .env.sample в .env
.env.sample есть в:
- docker_compose
- docker_compose/app/config
- docker_compose/etl
- docker_compose/fastapi
- fake_data_to_postgres
- auth_service_compose/auth_service/app
- auth_service_compose/auth_service/tests/functional
````
docker network create services_network
cd auth_service_compose
docker-compose up -d
cd ../docker_compose
docker-compose up -d
````
После этого лучше всего сразу выключить контейнер с ETL в docker_compose и запустить его только после загрузки данных в Postgres
<!-- Лично у меня curl без minified json не выполнялся, смотрится так себе конечно -->
Стоит подождать секунд 20 после запуска контейнеров чтобы elasticsearch правильно ответил на следующую команду
````
curl -XPUT 127.0.0.1:9200/movies -H 'Content-Type: application/json' -d '{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"imdb_rating":{"type":"float"},"genre":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"name":{"type":"text","analyzer":"ru_en"}}},"title":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}},"description":{"type":"text","analyzer":"ru_en"},"directors":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en"}}},"actors_names":{"type":"text","analyzer":"ru_en"},"writers_names":{"type":"text","analyzer":"ru_en"},"directors_names":{"type":"text","analyzer":"ru_en"},"actors":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en"}}},"writers":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en"}}}}}}'
curl -XPUT 127.0.0.1:9200/persons -H 'Content-Type: application/json' -d '{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}}}}}'
curl -XPUT 127.0.0.1:9200/genres -H 'Content-Type: application/json' -d '{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"name":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}}}}}'
 
````
````
cd ..
cd fake_data_to_postgres
pip install -r requirements.txt
python3 load_data.py
````
ETL работает раз в 10 минут с задержкой в 60 сек после старта контейнера, если не успеть сделать индекс или заполнить бд, то нужно пересоздать контейнер с ETL или удалить .state файлы в нем
После чего данные должны быть как в Postgres, так и в Elasticsearch

FastAPI находится на http://127.0.0.1/fapi/