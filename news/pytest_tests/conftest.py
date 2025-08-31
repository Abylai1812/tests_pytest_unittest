import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client

from news.models import News,Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author): 
    client = Client()
    client.force_login(author) 
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client



@pytest.fixture
def news(db):
    news = News.objects.create(  
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author,news):
    comment = Comment.objects.create(
        text='Текст комментарий',
        author=author,
        news=news
    )
    return comment

@pytest.fixture
def id_for_args(comment):  
    return (comment.id,) 

@pytest.fixture
def form_data():
    return {
        'text': 'Новый комментарий'
    } 

@pytest.fixture
def create_news_list(db):
    today = datetime.today()
    news_list = [
        News(
            title = 'Заголовок',
            text = 'Текст',
            date = today - timedelta(index + 1)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(news_list)
