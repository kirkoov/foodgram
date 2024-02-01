from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test_uza",
            first_name="First",
            last_name="Last",
            email="normal@user.com",
            password="foo",
        )
        self.assertEqual(user.username, "test_uza")
        self.assertEqual(user.first_name, "First")
        self.assertEqual(user.last_name, "Last")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="test_admin_uza",
            first_name="John",
            last_name="Doe",
            email="admin@user.com",
            password="fooPawd",
        )

        self.assertEqual(admin_user.username, "test_admin_uza")
        self.assertEqual(admin_user.first_name, "John")
        self.assertEqual(admin_user.last_name, "Doe")
        self.assertEqual(admin_user.email, "admin@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
