import os
from typing import Any
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


def murdered() -> list[dict[Any]]:
    mongo_uri = os.getenv('MONGO_DB_URI')
    client = MongoClient(mongo_uri)
    db = client[os.getenv('MONGO_DB_DATABASE')]
    collection = db['desaparecidos']

    page = 1
    items_per_page = 10
    all_results = []
    today = datetime.today()

    while True:
        skip_value = (page - 1) * items_per_page

        pipeline = [
            {'$unwind': '$known_facts'},
            {
                '$match': {
                    '$expr': {
                        '$and': [
                            {'$eq': [{'$dayOfMonth': '$known_facts.date'}, today.day]},
                            {'$eq': [{'$month': '$known_facts.date'}, today.month]},
                            {
                                '$or': [
                                    {
                                        '$and': [
                                            {'$eq': ['$status', 'Asesinado/a']},
                                            {'$eq': ['$known_facts.type', 'Asesinato']}
                                        ]
                                    },
                                    {
                                        '$and': [
                                            {'$eq': ['$status', 'Detenido/a desaparecido/a']},
                                            {'$eq': ['$known_facts.type', 'Secuestro']}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            },
            {
                '$group': {
                    '_id': '$_id',
                    'source_entry': {'$first': '$source_entry'},
                    'name': {'$first': '$name'},
                    'first_name': {'$first': '$first_name'},
                    'last_name': {'$first': '$last_name'},
                    'full_name': {'$first': '$full_name'},
                    'year': {'$first': '$year'},
                    'status': {'$first': '$status'},
                    'known_facts': {'$push': '$known_facts'},
                    'age': {'$first': '$age'},
                    'genre': {'$first': '$genre'},
                    'nationalities': {'$first': '$nationalities'},
                    'number_of_children': {'$first': '$number_of_children'},
                    'pregnant': {'$first': '$pregnant'},
                    'civil_status': {'$first': '$civil_status'},
                    'nicknames': {'$first': '$nicknames'},
                    'militancy': {'$first': '$militancy'},
                    'simultaneous_victims': {'$first': '$simultaneous_victims'},
                    'related_victims': {'$first': '$related_victims'},
                    'photo': {'$first': '$photo'},
                    'observations': {'$first': '$observations'},
                    'identification_data': {'$first': '$identification_data'},
                    'family_data': {'$first': '$family_data'},
                    'studies': {'$first': '$studies'},
                    'news_articles': {'$first': '$news_articles'},
                    'occupations': {'$first': '$occupations'},
                }
            },
            {'$skip': skip_value},
            {'$limit': items_per_page}
        ]

        results = list(collection.aggregate(pipeline))
        if not results:
            break

        all_results.extend(results)
        page += 1

    for result in all_results:
        result['_id'] = str(result['_id'])
        for fact in result.get('known_facts', []):
            if 'date' in fact:
                fact['date'] = fact['date'].strftime('%Y-%m-%d')

    return {
        'current_page': page - 1,
        'items_per_page': items_per_page,
        'results': all_results
    }
