# from django.test import TestCase
# from django.contrib.auth import get_user_model

# from django.urls import reverse

# from notes.models import Note
# from notes.forms import NoteForm

# User = get_user_model()

# class TestDetailPage(TestCase):
    
#     @classmethod
#     def setUpTestData(cls):
#         cls.notes = Note.objects.create(
#             title='Тестовая новость', text='Просто текст.'
#         )
#         cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
#         cls.author = User.objects.create(username='Автор')
    
#     def test_anonymous_client_has_no_form(self):
#         response = self.client.get(self.detail_url)
#         self.assertNotIn('form', response.context)
        
#     def test_authorized_client_has_form(self):
#         # Авторизуем клиент при помощи ранее созданного пользователя.
#         self.client.force_login(self.author)
#         response = self.client.get(self.detail_url)
#         self.assertIn('form', response.context)
#         # Проверим, что объект формы соответствует нужному классу формы.
#         self.assertIsInstance(response.context['form'], NoteForm)