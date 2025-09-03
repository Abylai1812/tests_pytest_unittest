Routes.py

from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse
from news.forms import WARNING, BAD_WORDS
from news.models import Comment
 

@pytest.mark.django_db
 

def test_user_can_create_comment(author_client, author, form_data, news):
 

    url = reverse('news:detail', args=(news.id,))
 

    response = author_client.post(url, data=form_data)
 

    assertRedirects(response, f'{url}#comments')
 

    assert Comment.objects.count() == 1
 

    new_comment = Comment.objects.get()
 
Не надежно, а если БД будет не пустой. В начале теста нужно обязательно почистить БД сначала.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер

    assert new_comment.news == news
 

    assert new_comment.author == author
 

    assert new_comment.text == form_data['text']
 
@pytest.mark.django_db
 

def test_anonymous_user_cant_create_comment(client, form_data, news):
 

    url = reverse('news:detail', args=(news.id,))
 

    response = client.post(url, data=form_data)
 

    login_url = reverse('users:login')
 

    expected_url = f'{login_url}?next={url}'
 

    assertRedirects(response, expected_url)
 

    assert Comment.objects.count() == 0
 
А если по какой-то причине в БД есть записи? Лучше не так явно проверять на значение. 
Вначале теста считаем комментарии в БД и тут уже сравниваем, "количество было" и "количество стало". 
В тестах ниже это же замечание.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер


def test_user_cant_use_bad_words(author_client, news):
 

    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
 

    url = reverse('news:detail', args=(news.id,))
 

    response = author_client.post(url, data=bad_words_data)
 

    assertFormError(response.context['form'], 'text', WARNING)
 

    assert Comment.objects.count() == 0
 
Правильнее сначала проверить на количество, так как если количество изменилось, то проверка на ошибку форму уже не важна.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер


def test_author_can_edit_comment(author_client, form_data, comment):
 

    url = reverse('news:edit', args=(comment.id,))
 

    response = author_client.post(url, form_data)
 

    expected_url = reverse(
 

        'news:detail',
 

        args=(comment.news.id,)
 

    ) + '#comments'
 

    assertRedirects(response, expected_url)
 

    comment.refresh_from_db()
 
Метод refresh_from_db() тут не подойдет. Да, мы получим объект, но он будет новый и при этом потеряем доступ к прежнему состоянию(а оно нам еще может пригодиться). Достаем комментарий методом get по id комментария из фикстуры.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер

    assert comment.text == form_data['text']
 


 
Стоит еще проверить, что автор не поменялся. Новость также могла измениться.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер


 

def test_other_user_cant_edit_comment(not_author_client, form_data, comment):
 

    url = reverse('news:edit', args=(comment.id,))
 

    response = not_author_client.post(url, form_data)
 

    assert response.status_code == HTTPStatus.NOT_FOUND
 

    note_from_db = Comment.objects.get(id=comment.id)
 

    assert comment.text == note_from_db.text
 


 
Стоит еще проверить, что автор не поменялся. Новость также могла измениться.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер


 

def test_author_can_delete_comment(author_client, id_for_args, comment):
 

    url = reverse('news:delete', args=id_for_args)
 

    response = author_client.post(url)
 

    expected_url = reverse(
 

        'news:detail',
 

        args=(comment.news.id,)
 

    ) + '#comments'
 

    assertRedirects(response, expected_url)
 

    assert Comment.objects.count() == 0
 


 
Нужно убедиться, что именно удаляемый комментарий покинул БД.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер


 

def test_other_user_cant_delete_comment(not_author_client, id_for_args):
 

    url = reverse('news:delete', args=id_for_args)
 

    response = not_author_client.post(url)
 

    assert response.status_code == HTTPStatus.NOT_FOUND
 

    assert Comment.objects.count() == 1
 

 
Стоит еще проверить, что комментарий при попытке удаления не мутировал. Достаем его и проверяем по полям.