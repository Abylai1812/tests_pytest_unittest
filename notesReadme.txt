Contest . py

from django.contrib.auth import get_user_model
 

from django.test import TestCase
 

from django.urls import reverse
 


 

from notes.forms import NoteForm
 

from notes.models import Note
 


 


 

User = get_user_model()
 


 


 

class TestDetailPage(TestCase):
 


 

    @classmethod
 

    def setUpTestData(cls):
 
Лучше создать свой класс, наследоваться от TestCase. В нем определить setUpTestData(cls) и вынести в него все фикстуры и реверсы. Во всех модулях тестов уже наследоваться от него.
Там где будет необходимо дополнить setUpTestData(cls) фикстурами, можно его переопределить, сначала вызвать super() и дописать еще.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер

        cls.author = User.objects.create_user(username='Автор')
 

        cls.reader = User.objects.create_user(username='Читатель')
 

        cls.note = Note.objects.create(
 

            title='Заголовок заметки',
 

            text='Просто текст.',
 

            slug='test-slug',
 

            author=cls.author
 

        )
 


 

        cls.list_url = reverse('notes:list')
 

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
 


 

    def test_notes_list_for_different_users(self):
 

        user_statuses = (
 

            (self.author, True),
 

            (self.reader, False),
 

        )
 

        url = self.list_url
 
Лишнее присвоение.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер

        for user, expected_visibility in user_statuses:
 

            self.client.force_login(user)
 
Всю подготовку по созданию и логированию лучше делать в setUpTestData(), оставив в методах только тестирующий код. Клиентов заранее создать можно сколько угодно.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер

            with self.subTest(user=user):
 

                response = self.client.get(url)
 

                object_list = response.context['object_list']
 

                if expected_visibility:
 
Избавься от проверки. В кортеже можно передавать вместо булево ассерты.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер

                    self.assertIn(self.note, object_list)
 

                else:
 

                    self.assertNotIn(self.note, object_list)
 


 

    def test_pages_contains_form(self):
 

        urls = (
 

            ('notes:add', None),
 
Реверсы много где повторяются, лучше их вынести в фикстуры.
Надо исправить
Отметить как выполненный
Игорь Шкода
ревьюер

            ('notes:edit', (self.note.slug,)),
 

        )
 

        for name, args in urls:
 

            with self.subTest(name=name):
 

                url = reverse(name, args=args)
 

                self.client.force_login(self.author)  # доступ только автору
 

                response = self.client.get(url)
 

                self.assertIn('form', response.context)
 

                self.assertIsInstance(response.context['form'], NoteForm)
 