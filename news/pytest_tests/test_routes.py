import pytest
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects

from http import HTTPStatus

from django.urls import reverse

# Главная страница доступна анонимному пользователю. - Done
# Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям. - Done
@pytest.mark.parametrize(
    'name',  
    ('news:home', 'users:login', 'users:signup'),
)

@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)  
    response = client.get(url)  
    assert response.status_code == HTTPStatus.OK


# Страницы отдельной новости доступно анонимному пользователю - Done
@pytest.mark.django_db
def test_news_availability_for_anonymous_user(client,news):
    url = reverse('news:detail',args=(news.id,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# Удаления и редактирования комментарий доступны только автору комментарий -Done
# Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404. - Done
@pytest.mark.parametrize(
    
    'parametrized_client, expected_status',
    (
        (lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)


@pytest.mark.parametrize(
    'name',
    ('news:edit','news:delete')
)


def test_pages_availability_for_different_users(
        parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status 

# Аноним перенаправляется на страницу логина при попытке редактировать/удалить комментарий
@pytest.mark.parametrize(
    'name,args',
    (
        ('news:edit', lazy_fixture('id_for_args')),
        ('news:delete', lazy_fixture('id_for_args')),
    )
)

def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url) 
