from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class RegistrationTest(APITestCase):

    def test_registration(self):
        response = self.client.post(
            '/api/register/',
            {
                'username':'testuser',
                'email':'test@example.com',
                'password':'StrongPass123!'
            }
        )
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data['username'],'testuser')

    def test_duplicate_email(self):

        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='StrongPass123!'
        )

        response = self.client.post(
            '/api/register/',
            {
                'username':'anotheruser',
                'email':'test@example.com',
                'password':'StrongPass123!'
            }
        )

        self.assertEqual(response.status_code,400)
        self.assertIn('A user with this email already exists.',str(response.data))