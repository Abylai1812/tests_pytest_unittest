from http import HTTPStatus

from pytils.translit import slugify
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TITLE = 'Заголовок заметки'
    NOTE_TEXT = 'Текст заметки'


    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.note = Note.objects.create(title='Заголовок', text='Текст',author=cls.user)
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'title':cls.NOTE_TITLE,'text': cls.NOTE_TEXT,}

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.add_url, data = self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count,1)
    

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.add_url, data = self.form_data)
        self.assertRedirects(response,self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count,2)
        note = Note.objects.latest('id')
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.author, self.user)


    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        response = self.auth_client.post(self.add_url, data=self.form_data)
        form = response.context['form']
        self.assertFormError(
            form=form,
            field='slug',
            errors=self.note.slug + WARNING
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    
    def test_empty_slug(self):
        self.form_data.pop('slug',None)
        response = self.auth_client.post(self.add_url,data=self.form_data)
        self.assertRedirects(response,self.success_url)
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.latest('id')
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

class TestNoteEditDelete(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NOTE_TITLE = 'Заголовок заметки'
    NEW_NOTE_TEXT = 'Обновлённый текст заметки'
    NEW_NOTE_TITLE = 'Обновлённый текст заголовки'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.note = Note.objects.create(title='Заголовок заметки', text='Текст заметки',author=cls.user)
        cls.note_url = reverse('notes:detail',args=(cls.note.slug,))

        cls.author_client = Client()
        cls.author_client.force_login(cls.user)

        cls.reader = User.objects.create(username='Аноним')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.edit_url = reverse('notes:edit',args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))  
        cls.form_data = {'text': cls.NEW_NOTE_TEXT,'title':cls.NEW_NOTE_TITLE}


    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0) 
    
    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1) 

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url,data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)
        self.assertEqual(self.note.title, self.NEW_NOTE_TITLE)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
        self.assertEqual(self.note.title, self.NOTE_TITLE)

