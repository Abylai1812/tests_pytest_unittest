import pytest
from http import HTTPStatus
from django.conf import settings

from news.models import News
from news.forms import CommentForm
from django.urls import reverse


HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client,create_news_list):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE

@pytest.mark.django_db
def test_news_order(client,create_news_list):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates




@pytest.mark.django_db
def test_anonymous_client_has_no_form(client,news):
    url = reverse('news:detail',args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context

@pytest.mark.django_db
def test_authorized_client_has_form(author_client,news):
    url = reverse('news:detail',args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)

    