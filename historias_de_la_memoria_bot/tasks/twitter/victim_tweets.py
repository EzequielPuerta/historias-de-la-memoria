import json
import math
from typing import Any
from openai import OpenAI
from logger import logger

from api.constants import OPENAI_TEMPERATURE, X_CHARACTER_LIMIT
from bot.tasks.twitter.tweet import Tweet


PROMPT_MESSAGE = {
    "role": "user",
    "content": """
You are a tweets creator. You will receive a list with many json objects with data about "desaparecidos" during the last argentine dictatorship. I want you to create a short text about each victim, to publish them on X (ex Twitter).
- Text must be in Spanish
- Each tweet text must have up to 220 characters
- You must sound very professional and ethical, because this subject is very sensitive
- Don't use emojis
- Don't use hashtags
- Don't include links
- Don't include opinions, ideas, reflections or conclusions, only facts
- Don't mention that their family, loved ones, etc. remember them. Don't speak on behalf of other people.
- Keep it short, simple and direct
- Center the view in the studies, jobs, their families and relationships (especially if they were also simultaneous victims), or any other valuable information
- If there is no information about militancy, mention it
- Don't be creative. Set the temperature to 0
"""
}
# EXTRA PROMPTS:
# - If you have more information about the victim, feel free to add more tweets with it. But keep the same format and just add true facts


class VictimTweets:
    def __init__(self, victim: dict[Any]) -> None:
        self.victim = victim
        self._id = self.victim['_id']
        self.url = self.victim['source_entry']['url']

        try:
            self.photos = [photo['url'] for photo in self.victim['photos']]
        except (KeyError, IndexError):
            self.photos = []

        try:
            self.news_article = self.victim['news_article'][0]['url']
        except (KeyError, IndexError):
            self.news_article = None

        self.link_text = self.__create_links_text()
        self.tweets = self.__create_tweets(self.__fetch_openai_text_proposal())

    def __fetch_openai_text_proposal(self) -> str:
        messages = [PROMPT_MESSAGE]
        messages.append({"role": "user", "content": json.dumps(self.victim)})

        openai_client = OpenAI()
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=OPENAI_TEMPERATURE,
        )
        tweet_text = completion.choices[0].message.content
        logger.debug(tweet_text)
        return tweet_text

    def __create_links_text(self) -> str:
        profile_text = f"👤 Fuente: {self.url}"
        if self.news_article:
            article_text = f" | 📰 Artículo: {self.news_article}"
        else:
            article_text = ""
        hashtag = " | #NuncaMás"
        return f"{profile_text}{article_text}{hashtag}"

    def __create_tweets(self, text_proposal: str) -> list[Tweet]:
        if len(text_proposal) <= X_CHARACTER_LIMIT:
            return [
                self.tweet(text_proposal, self.photos),
                self.tweet(self.link_text)
            ]
        else:
            try:
                sentences = [sentence for sentence in text_proposal.split('.') if sentence != '']
                expected_splits = math.ceil(len(text_proposal) / 280) - 1
                tweets_texts = []

                while expected_splits >= 0:
                    dot_index = 0
                    possible_text = ''

                    while (len(possible_text) <= X_CHARACTER_LIMIT) and (dot_index <= len(sentences)):
                        dot_index = dot_index + 1
                        possible_text = ' '.join(sentences[:dot_index])
                    dot_index = dot_index - 1
                    assert dot_index > 0
                    possible_text = ' '.join(sentences[:dot_index])
                    tweets_texts.append(possible_text)
                    expected_splits = expected_splits - 1
                    sentences = sentences[dot_index:]
            except Exception as error:
                raise RuntimeError(f"It was impossible to convert the text propossed by OpenAI into tweets: {error}")
            else:
                tweets = [self.tweet(tweets_texts[0], self.photos)]
                [tweets.append(self.tweet(text)) for text in tweets_texts[1:]]
                tweets.append(self.tweet(self.link_text))
                return tweets

    def tweet(self, text: str, photos: list[str] = []) -> Tweet:
        return Tweet(text, photos, self._id)
