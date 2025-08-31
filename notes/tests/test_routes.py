from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='TestUser')
        cls.note = Note.objects.create(title='Заголовок', text='Текст',author=user)
        cls.author = User.objects.create(username='Писатель')
        cls.reader = User.objects.create(username='Читатель')
    # Здесь я создаю 2 объекта Note. Так как я переписал его из News Первый cls.note - эта созадание одного новостья
    # второй  cls.note - эта создание комментария , 
    # а если его убрать тесты подают , надо придумать как эта исправить 
        cls.note = Note.objects.create(
            author=cls.author,
            text='Текст комментария'
        )


    def test_pages_availability(self):
        urls = (
            ('notes:home',None),
            ('users:login', None),
            ('users:signup', None),
        )
        for name,args in urls:
            with self.subTest(name=name):
                url = reverse(name,args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    
    def test_pages_availability_for_auth_user(self):
        urls = (
            ('notes:add',None),
            ('notes:success',None),
            ('notes:list',None),
        )
        for name,args in urls:
            with self.subTest(name=name):
                url = reverse(name,args=args)
                self.client.force_login(self.author)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    
    def test_availability_for_notes_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user,status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit','notes:delete','notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=[self.note.slug,])
                    response = self.client.get(url)
                    self.assertEqual(response.status_code,status)


    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:success', None),
            ('notes:add',None),
            ('notes:list',None),
        )
        for name,args in urls:
            with self.subTest(name=name):
                url = reverse(name,args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response,redirect_url)
