from django.test import TestCase
from django.contrib.auth import get_user_model

from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestDetailPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='Автор', password='pass123')
        cls.reader = User.objects.create_user(username='Читатель', password='pass123')

        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Просто текст.',
            slug='test-slug',
            author=cls.author
        )

        cls.list_url = reverse('notes:list',)
        cls.edit_url = reverse()

        



    def test_notes_list_for_different_users(self):
        user_statuses = (
            (self.author, True),
            (self.reader, False),
        )
        url = reverse(self.list_url)
        for user, expected_visibility in user_statuses:
            self.client.force_login(user)
            with self.subTest(user=user):
                response = self.client.get(url)
                object_list = response.context['object_list']
                if expected_visibility:
                    self.assertIn(self.note, object_list)
                else:
                    self.assertNotIn(self.note, object_list)


    def test_pages_contains_form(self):

    

    # def test_anonymous_client_has_no_form(self):
    #     response = self.client.get(self.detail_url)
    #     self.assertNotIn('form', response.context)
        
    # def test_authorized_client_has_form(self):
    #     # Авторизуем клиент при помощи ранее созданного пользователя.
    #     self.client.force_login(self.author)
    #     response = self.client.get(self.detail_url)
    #     self.assertIn('form', response.context)
    #     # Проверим, что объект формы соответствует нужному классу формы.
    #     self.assertIsInstance(response.context['form'], NoteForm)