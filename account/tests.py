from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Создаём пользователей с разными ролями
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass',
            role='admin'
        )
        self.editor_user = User.objects.create_user(
            username='editor',
            email='editor@test.com',
            password='editorpass',
            role='editor'
        )
        self.viewer_user = User.objects.create_user(
            username='viewer',
            email='viewer@test.com',
            password='viewerpass',
            role='viewer'
        )

    def test_register_user(self):
        """Тест регистрации нового пользователя"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass',
            'role': 'viewer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        """Тест логина и получения JWT"""
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'adminpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_list_access_admin(self):
        """Админ может видеть список всех пользователей"""
        url = reverse('users')
        login_response = self.client.post(
            reverse('login'),
            {'username': 'admin', 'password': 'adminpass'},
            format='json'
        )
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)

    def test_user_list_access_editor(self):
        """Редактор не может видеть список пользователей"""
        url = reverse('users')
        login_response = self.client.post(
            reverse('login'),
            {'username': 'editor', 'password': 'editorpass'},
            format='json'
        )
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_access_viewer(self):
        """Viewer не может видеть список пользователей"""
        url = reverse('users')
        login_response = self.client.post(
            reverse('login'),
            {'username': 'viewer', 'password': 'viewerpass'},
            format='json'
        )
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_and_login_flow(self):
        """Проверяем полный цикл: регистрация -> логин -> JWT"""
        # Регистрация
        reg_data = {
            'username': 'flowuser',
            'email': 'flow@test.com',
            'password': 'flowpass',
            'role': 'editor'
        }
        reg_response = self.client.post(reverse('register'), reg_data, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)

        # Логин
        login_data = {'username': 'flowuser', 'password': 'flowpass'}
        login_response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)
