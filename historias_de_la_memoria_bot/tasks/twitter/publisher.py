import os
import tweepy
import shutil
from logger import logger
from datetime import datetime

from historias_de_la_memoria_bot.constants import MONTH_NAMES, DIR_PATH
from historias_de_la_memoria_bot.tasks.twitter.tweet import Tweet
from historias_de_la_memoria_bot.tasks.picture_manager import download_picture
from historias_de_la_memoria_bot.tasks.db.set_published import set_as_published


RATE_LIMIT_HEADERS = [
    "x-app-limit-24hour-remaining",
    "x-app-limit-24hour-reset",
    "x-user-limit-24hour-remaining",
    "x-user-limit-24hour-reset",
]


class XPublisher:
    def __init__(self) -> None:
        self.CLIENT = tweepy.Client(
            bearer_token=os.getenv('BEARER_TOKEN'),
            consumer_key=os.getenv('CONSUMER_API_KEY'),
            consumer_secret=os.getenv('CONSUMER_API_KEY_SECRET'),
            access_token=os.getenv('ACCESS_TOKEN'),
            access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
        )
        self.API = tweepy.API(auth=tweepy.OAuth1UserHandler(
            consumer_key=os.getenv('CONSUMER_API_KEY'),
            consumer_secret=os.getenv('CONSUMER_API_KEY_SECRET'),
            access_token=os.getenv('ACCESS_TOKEN'),
            access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
        ))

    def __summary_text(self, total: int, today: datetime.date):
        day = today.day
        month = MONTH_NAMES[today.month]
        if total > 1:
            text = f"""Entre 1969 y 1983 hubo un total de {total} víctimas del terrorismo de Estado en la Argentina, asesinadas o desaparecidas un {day}º de {month}. Algunas de ellas:"""
        elif total == 1:
            text = f"""Entre 1969 y 1983 hubo una víctima del terrorismo de Estado en la Argentina, asesinada o desaparecida un {day}º de {month}."""
        return text

    def publish_all(
        self,
        tweets: list[Tweet],
        total: int,
    ) -> str:
        today = datetime.today()
        try:
            response = self.CLIENT.create_tweet(
                text=self.__summary_text(total, today))
            logger.info("Parent tweet published")
        except tweepy.errors.TooManyRequests as error:
            logger.error(f"Error: {error}")
            if hasattr(error, 'response') and error.response is not None:
                headers = error.response.headers
                logger.error("Rate limit headers:")
                for header in RATE_LIMIT_HEADERS:
                    logger.error(f"{header}: {headers.get(header)}")
            else:
                logger.error("No response headers available.")
        except Exception as error:
            logger.error(f"Error during publishing parent tweet: {error} | {str(error)}")
        else:
            try:
                for tweet in tweets:
                    parameters = {
                        'text': tweet.text,
                        'in_reply_to_tweet_id': response.data['id'],
                    }
                    media_ids = []
                    for photo in tweet.photos:
                        logger.debug(f"Tweet {tweet._id} has {len(tweet.photos)} photos.")
                        filename = download_picture(photo, tweet._id)
                        file = self.API.media_upload(filename)
                        media_ids.append(file.media_id)
                    if media_ids:
                        parameters['media_ids'] = media_ids
                    response = self.CLIENT.create_tweet(**parameters)
                    logger.info(f"Tweet related to {tweet._id} published on {datetime.now()}")

                    response = self.CLIENT.create_tweet(
                        text=tweet.links_text,
                        in_reply_to_tweet_id=response.data['id'])
                    logger.info(f"Tweet with links related to {tweet._id} published on {datetime.now()}")

                    set_as_published(tweet._id, today)
                    logger.info(f"Desaparecido with id {tweet._id} marked as published on database")
            except tweepy.errors.TooManyRequests as error:
                logger.error(f"Error: {error}")
                if hasattr(error, 'response') and error.response is not None:
                    headers = error.response.headers
                    logger.error("Rate limit headers:")
                    for header in RATE_LIMIT_HEADERS:
                        logger.error(f"{header}: {headers.get(header)}")
                else:
                    logger.error("No response headers available.")
            except Exception as error:
                logger.error(f"Error during publishing tweet related to {tweet._id}: {error} | {str(error)}")
            finally:
                try:
                    shutil.rmtree(DIR_PATH)
                    logger.debug("Temporary files deleted.")
                except Exception as error:
                    logger.error(f"Error during temporary folder deletion: {error}")
