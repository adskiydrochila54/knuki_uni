from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ContactMessage

User = get_user_model()


class ContactMessageTests(APITestCase):

    def test_create_contact_message(self):
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "topic": "Test topic",
            "message": "This is a test contact message",
        }

        response = self.client.post(
            "/api/v1/contacts/create/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_create_contact_message_invalid(self):
        payload = {
            "name": "A",
            "email": "test@example.com",
            "message": "short",
        }

        response = self.client.post(
            "/api/v1/contacts/create/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_can_list_messages(self):
        admin = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@test.com",
        )
        self.client.force_authenticate(admin)

        ContactMessage.objects.create(
            name="User",
            email="u@test.com",
            message="Test message content",
        )

        response = self.client.get("/api/v1/contacts/list/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_non_admin_cannot_list_messages(self):
        user = User.objects.create_user(
            username="user",
            password="user123",
        )
        self.client.force_authenticate(user)

        response = self.client.get("/api/v1/contacts/list/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_message_as_read(self):
        admin = User.objects.create_superuser(
            username="admin2",
            password="admin123",
            email="admin2@test.com",
        )
        self.client.force_authenticate(admin)

        message = ContactMessage.objects.create(
            name="User",
            email="u@test.com",
            message="Test message content",
        )

        response = self.client.patch(
            f"/api/v1/contacts/{message.id}/read/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        message.refresh_from_db()
        self.assertTrue(message.is_read)
