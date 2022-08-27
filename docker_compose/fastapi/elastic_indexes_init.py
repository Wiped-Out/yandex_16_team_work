from dotenv import load_dotenv
from requests import put


def main():
    load_dotenv()
    url = f"{os.getenv('ELASTIC_HOST')}:{os.getenv('ELASTIC_PORT')}"

    put(url=f"{url}/movies", headers={"Content-Type": "application/json"},
        data='{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"imdb_rating":{"type":"float"},"genre":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"name":{"type":"text","analyzer":"ru_en"}}},"title":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}},"description":{"type":"text","analyzer":"ru_en"},"directors":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en"}}},"actors_names":{"type":"text","analyzer":"ru_en"},"writers_names":{"type":"text","analyzer":"ru_en"},"directors_names":{"type":"text","analyzer":"ru_en"},"actors":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en"}}},"writers":{"type":"nested","dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en"}}}}}}')
    put(url=f"{url}/persons", headers={"Content-Type": "application/json"},
        data='{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"full_name":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}}}}}')
    put(url=f"{url}/genres", headers={"Content-Type": "application/json"},
        data='{"settings":{"refresh_interval":"1s","analysis":{"filter":{"english_stop":{"type":"stop","stopwords":"_english_"},"english_stemmer":{"type":"stemmer","language":"english"},"english_possessive_stemmer":{"type":"stemmer","language":"possessive_english"},"russian_stop":{"type":"stop","stopwords":"_russian_"},"russian_stemmer":{"type":"stemmer","language":"russian"}},"analyzer":{"ru_en":{"tokenizer":"standard","filter":["lowercase","english_stop","english_stemmer","english_possessive_stemmer","russian_stop","russian_stemmer"]}}}},"mappings":{"dynamic":"strict","properties":{"id":{"type":"keyword"},"name":{"type":"text","analyzer":"ru_en","fields":{"raw":{"type":"keyword"}}}}}}')


if __name__ == '__main__':
    main()
