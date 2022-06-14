Для проверки задания нужно:\
Сделать свои .env наподобии .env.sample или переимеиновать .env.sample в .env
.env.sample есть в:
- docker_compose
- docker_compose/app/config
- docker_compose/etl
- docker_compose/fastapi
- sqlite_to_postgres
````
cd docker_compose
docker-compose up -d
````
<!-- Лично у меня curl без minified json не выполнялся, смотрится так себе конечно -->
Стоит подождать секунд 20 после запуска контейнеров чтобы elasticsearch правильно ответил на следующую команду
````
curl -XPUT 127.0.0.1:9200/movies -H 'Content-Type: application/json' -d '{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"imdb_rating":{"type":"float"},"genre":{"type":"keyword"},"title":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}},"description":{"type":"text","analyzer":"ru_en"},"director":{"type":"text","analyzer":"ru_en"},"actors_names":{"type":"text","analyzer":"ru_en"},"writers_names":{"type":"text","analyzer":"ru_en"},"actors":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"name":{"type":"text","analyzer":"ru_en"}}},"writers":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"name":{"type":"text","analyzer":"ru_en"}}}}}}'
curl -XPUT 127.0.0.1:9200/persons -H 'Content-Type: application/json' -d '{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}},"role":{"type":"text","analyzer":"ru_en"},"film_ids":{"type":"keyword"}}}}'
 
````
````
cd ..
cd sqlite_to_postgres
pip install -r requirements.txt
python3 load_data.py
````
ETL работает раз в 10 минут с задержкой в 60 сек после старта контейнера, если не успеть сделать индекс или заполнить бд, то нужно пересоздать контейнер с ETL или удалить .state файлы в нем
После чего данные должны быть как в Postgres, так и в Elasticsearch