from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class LoggedInTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="patrick@gmail.com",
            first_name="Patrick",
            last_name="Smith",
            password="123456789"
        )

    # TODO : revoir ce test ( status_code = 200 ? )
    """def test_valid_login(self):
        data = {"email": "patrick@gmail.com", "password": "123456789"}
        resp = self.client.post(reverse("accounts:login"), data=data)
        self.assertTemplateUsed(resp, "accounts/login.html")
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse("store:index"))
        self.assertIn("Mon profil", str(resp.content))"""

    def test_invalid_login(self):
        data = {"email": "patrick@gmail.com", "password": "1234"}
        resp = self.client.post(reverse("accounts:login"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "accounts/login.html")

    def test_profile_change(self):
        self.client.login(email="patrick@gmail.com", password="123456789")
        data = {"email": "patrick@gmail.com",
                "password": "123456789",
                "first_name": "Patrick",
                "last_name": "Martin"}
        resp = self.client.post(reverse("accounts:profile"), data=data)

        self.assertEqual(resp.status_code, 302)

        patrick = User.objects.get(email="patrick@gmail.com")
        self.assertEqual(patrick.last_name, "Martin")

    # TODO : reprendre ce test ( resp.content = b'' ? )
    """def test_profile_change_wrong_password(self):
        self.client.login(email="patrick@gmail.com", password="123456789")

        data = {"email": "patrick@gmail.com",
                "password": "1234",
                "first_name": "Patrick",
                "last_name": "Martin"}
        resp = self.client.post(reverse("accounts:profile"), data=data)

        self.assertEqual(resp.status_code, 302)
        self.assertIn("Le mot de passe n'est pas valide.", str(resp.content))"""
