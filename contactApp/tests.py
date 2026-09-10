from django.test import TestCase
from django.urls import reverse

from .models import Ad


class ContactMessageFlowTests(TestCase):
    url = reverse('contactApp:contact')

    def post(self, **data):
        return self.client.post(self.url, data)

    def test_contact_page_renders(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="messageForm"')

    def test_valid_message_persists_once(self):
        response = self.post(nickname='御主', message='欢迎来到迦勒底')

        self.assertRedirects(response, self.url + '?saved=1')
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(Ad.objects.get().title, '御主')
        self.assertEqual(Ad.objects.get().description, '欢迎来到迦勒底')

    def test_contact_info_persists(self):
        self.post(
            nickname='御主',
            message='请联系我',
            contact_info='master@example.com',
        )

        self.assertEqual(Ad.objects.get().contact_info, 'master@example.com')

    def test_contact_info_is_not_rendered_publicly(self):
        Ad.objects.create(
            title='Stored name',
            description='Stored message',
            contact_info='private@example.com',
        )

        response = self.client.get(self.url)

        self.assertNotContains(response, 'private@example.com')

    def test_blank_nickname_is_rejected(self):
        response = self.post(nickname='', message='A message')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors['nickname'])
        self.assertEqual(Ad.objects.count(), 0)

    def test_whitespace_only_nickname_is_rejected(self):
        response = self.post(nickname='   ', message='A message')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors['nickname'])
        self.assertEqual(Ad.objects.count(), 0)

    def test_blank_message_is_rejected(self):
        response = self.post(nickname='御主', message='')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors['message'])
        self.assertEqual(Ad.objects.count(), 0)

    def test_whitespace_only_message_is_rejected(self):
        response = self.post(nickname='御主', message='   ')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors['message'])
        self.assertEqual(Ad.objects.count(), 0)

    def test_message_over_500_characters_is_rejected(self):
        response = self.post(nickname='御主', message='x' * 501)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors['message'])
        self.assertEqual(Ad.objects.count(), 0)

    def test_invalid_post_does_not_redirect_to_success(self):
        response = self.post(nickname='', message='')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ad.objects.count(), 0)

    def test_nickname_maximum_length_is_enforced(self):
        response = self.post(nickname='x' * 51, message='A message')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors['nickname'])
        self.assertEqual(Ad.objects.count(), 0)

    def test_contact_info_is_optional_and_trimmed(self):
        response = self.post(
            nickname=' 御主 ',
            message=' 留言 ',
            contact_info='  email@example.com  ',
        )

        self.assertRedirects(response, self.url + '?saved=1')
        record = Ad.objects.get()
        self.assertEqual(record.title, '御主')
        self.assertEqual(record.description, '留言')
        self.assertEqual(record.contact_info, 'email@example.com')
