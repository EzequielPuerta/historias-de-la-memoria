import os
from typing import Any, Tuple
from datetime import datetime
from pymongo import MongoClient

from historias_de_la_memoria.constants import MAX_AMOUNT_OF_DAILY_VICTIMS


MODEL_ATTRIBUTES = {
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
    'photos': {'$first': '$photos'},
    'observations': {'$first': '$observations'},
    'identification_data': {'$first': '$identification_data'},
    'family_data': {'$first': '$family_data'},
    'studies': {'$first': '$studies'},
    'news_articles': {'$first': '$news_articles'},
    'occupations': {'$first': '$occupations'},
}


def __SAME_DAY(date: datetime) -> dict[str, list[dict[str, str], int]]:
    return {'$eq': [{'$dayOfMonth': '$known_facts.date'}, date.day]}


def __SAME_MONTH(date: datetime) -> dict[str, list[dict[str, str], int]]:
    return {'$eq': [{'$month': '$known_facts.date'}, date.month]}


__WAS_MURDERED = {
    '$and': [
        {'$eq': ['$status', 'Asesinado/a']},
        {'$eq': ['$known_facts.type', 'Asesinato']}
    ]
}


__WAS_DISSAPEARED = {
    '$and': [
        {'$eq': ['$status', 'Detenido/a desaparecido/a']},
        {'$eq': ['$known_facts.type', 'Secuestro']}
    ]
}


def __MATCH_FILTER(date: datetime, excluded_ids: list[str]) -> dict[Any]:
    return {
        '$expr': {
            '$and': [
                __SAME_DAY(date),
                __SAME_MONTH(date),
                {'$not': {'$in': ['$_id', excluded_ids]}},
                {'$or': [__WAS_MURDERED, __WAS_DISSAPEARED]}
            ]
        }
    }


def fetch_from_mongodb_on(date: datetime) -> Tuple[int, list[dict[Any]]]:
    mongo_uri = os.getenv('MONGO_DB_URI')
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[os.getenv('MONGO_DB_DATABASE')]
    desaparecidos = db['desaparecidos']
    published = db['published']

    day = date.day
    month = date.month
    published_document = published.find_one({'day': day, 'month': month})
    excluded_ids = published_document['desaparecidos'] if published_document else []

    page = 1
    items_per_page = 100
    all_results = []

    while True:
        skip_value = (page - 1) * items_per_page
        pipeline = [
            {'$unwind': '$known_facts'},
            {'$match': __MATCH_FILTER(date, excluded_ids)},
            {'$group': MODEL_ATTRIBUTES},
            {'$skip': skip_value},
            {'$limit': items_per_page}
        ]

        results = list(desaparecidos.aggregate(pipeline))
        if not results:
            break

        all_results.extend(results)
        page += 1

    total = len(all_results)
    all_results = sorted(all_results, key=lambda x: bool(x.get('photos')), reverse=True)
    all_results = all_results[:MAX_AMOUNT_OF_DAILY_VICTIMS]
    for result in all_results:
        result['_id'] = str(result['_id'])
        for fact in result.get('known_facts', []):
            if 'date' in fact:
                fact['date'] = fact['date'].strftime('%Y-%m-%d')
    return (total, all_results)
