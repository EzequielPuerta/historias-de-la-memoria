from unittest.mock import Mock

from bot.tasks.twitter.tweet import Tweet
from bot.tasks.twitter.victim_tweets import VictimTweets


def test___create_tweets_from_short_proposal() -> None:
    victim_tweets = Mock()
    victim_tweets.victim = {}
    victim_tweets._id = '123'
    victim_tweets.url = 'http://mock.com/victim1'
    victim_tweets.photos = ['http://mock.com/victim1/photo1']
    victim_tweets.news_article = ['http://mock.com/victim1/news1']
    victim_tweets.link_text = f"👤 Fuente: http://mock.com/victim1 | 📰 Artículo: http://mock.com/victim1/news1 | #NuncaMás"

    short_proposal = 'Amalia Rosa Franchelli Mendez Dobelli, conocida como "Coca", fue secuestrada el 20 de marzo de 1976 en Ramos Mejía, Buenos Aires. Tenía 28 años y era estudiante universitaria de Filosofía. Su esposo, Raúl Aurelio Dobelli, también fue víctima.'
    victim_tweets.tweet = lambda text, photos=[]: Tweet(text, photos, victim_tweets._id)

    tweets = VictimTweets._VictimTweets__create_tweets(victim_tweets, short_proposal)
    assert len(tweets) == 2


def test___create_tweets_from_long_proposal() -> None:
    victim_tweets = Mock()
    victim_tweets.victim = {}
    victim_tweets._id = '123'
    victim_tweets.url = 'http://mock.com'
    victim_tweets.photos = ['http://mock.com/victim2/photo1']
    victim_tweets.news_article = ['http://mock.com/victim2/news1']
    victim_tweets.link_text = f"👤 Fuente: http://mock.com/victim2 | 📰 Artículo: http://mock.com/victim2/news1 | #NuncaMás"

    long_proposal = 'Luis Daniel Aisenberg Yuhjtman, conocido como "Roni", fue secuestrado el 20 de marzo de 1977 en Capital Federal. Tenía 22 años y era estudiante de Medicina en la UBA, cursando el 5to año. Militaba en la Juventud Universitaria Peronista. Su hermano, Ariel Aisenberg, también fue víctima del terrorismo de Estado.'
    victim_tweets.tweet = lambda text, photos=[]: Tweet(text, photos, victim_tweets._id)

    tweets = VictimTweets._VictimTweets__create_tweets(victim_tweets, long_proposal)
    assert len(tweets) == 3
