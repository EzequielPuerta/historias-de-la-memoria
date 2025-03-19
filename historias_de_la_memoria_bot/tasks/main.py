from typing import Any
from logger import logger
from datetime import datetime, timedelta
from dotenv import load_dotenv

from historias_de_la_memoria_bot.tasks.db.fetch_db import fetch_from_mongodb_on
from historias_de_la_memoria_bot.tasks.twitter.tweet import Tweet
from historias_de_la_memoria_bot.tasks.twitter.publisher import XPublisher


load_dotenv(override=True)


def __histogram() -> None:
    date = datetime(2024, 1, 1)
    data = {}
    _min = 10
    _max = 0
    days_without = []

    while date.year == 2024:
        total, victims = fetch_from_mongodb_on(date)
        data[date] = {'total': total}
        print(f"{date} | {data[date]}")
        if total > _max:
            _max = total
        elif total < _min:
            _min = total
        elif total == 0:
            days_without.append(date)
        date = date + timedelta(days=1)
    print(f"Min: {_min} | Max: {_max} | Days without victims: {days_without}")
    return data


def execute() -> list[dict[Any]]:
    today = datetime.today()
    total, victims = fetch_from_mongodb_on(today)
    logger.info(f"SE EJECUTÓ: {total}")
    # XPublisher().publish_all(
    #     [Tweet(victim) for victim in victims],
    #     total=total)
