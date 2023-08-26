import os

from django.test import TestCase
from django.urls import reverse

from django.conf import settings


class ShellTests(TestCase):
    def setUp(self):
        self.headers = {'HTTP_AGENT_TOKEN': settings.AGENT_TOKEN}

    def test_get_shell_no_command(self):
        response = self.client.get(reverse('shell'), **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['error'])

    def test_get_shell_with_command(self):
        response = self.client.get(reverse('shell'), {'command': 'echo 1'}, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['error'])
        self.assertEqual(response.json()['stdout'], f'1{os.linesep}')

    def test_post_shell_no_command(self):
        response = self.client.post(reverse('shell'), **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['error'])

    def test_post_shell_with_command(self):
        response = self.client.post(reverse('shell'), {'command': 'echo 1'}, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['error'])
        self.assertEqual(response.json()['stdout'], f'1{os.linesep}')

    def test_post_shell_invalid_json(self):
        response = self.client.post(reverse('shell'), data='{}', content_type='application/json', **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['error'])

    def test_post_shell_valid_json(self):
        response = self.client.post(reverse('shell'), data='{"command": "echo 1"}', content_type='application/json',
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['error'])
        self.assertEqual(response.json()['stdout'], f'1{os.linesep}')
