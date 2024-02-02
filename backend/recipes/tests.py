import pytest

from django.test import TestCase

from .models import Tag


# NUM_CHARS_MEALTIME_NAME = 200
# NUM_CHARS_MEALTIME_HEX = 7
# NUM_CHARS_MEALTIME_SLUG = 200


class RecipeTests(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(
            name="S;lfja;sdlfjas;dlfjas;dlfjas;dlfkja;slfkj;aslfj;asdlfjsda;lfj;salfkj;asldfja;slfj;asldfjas;ldfjsa;dlfjas;lfjkas;ldfkjas;dlfkj;aslfkj;saldfkj;sadlfkjs;adlkfj;aslkfj;asldkfj;sadlfj;aslfj;asldjkf;saldjf;",
            color="",
            slug="",
        )
        self.assertTrue(
            tag.name,
            "S;lfja;sdlfjas;dlfjas;dlfjas;dlfkja;slfkj;aslfj;asdlfjsda;lfj;salfkj;asldfja;slfj;asldfjas;ldfjsa;dlfjas;lfjkas;ldfkjas;dlfkj;aslfkj;saldfkj;sadlfkjs;adlkfj;aslkfj;asldkfj;sadlfj;aslfj;asldjkf;saldjf;",
        )
        # User = get_user_model()
        # user = User.objects.create_user(
        #     username="test_uza",
        #     first_name="First",
        #     last_name="Last",
        #     email="normal@user.com",
        #     password="foo",
        # )
        # self.assertEqual(user.username, "test_uza")
        # self.assertEqual(user.first_name, "First")
        # self.assertEqual(user.last_name, "Last")
        # self.assertEqual(user.email, "normal@user.com")
        # self.assertTrue(user.is_active)
        # self.assertFalse(user.is_staff)
        # self.assertFalse(user.is_superuser)

        # with pytest.raises(Error):
        #     Tag.objects.create(
        #         name="S;lfja;sdlfjas;dlfjas;dlfjas;dlfkja;slfkj;aslfj;asdlfjsda;lfj;salfkj;asldfja;slfj;asldfjas;ldfjsa;dlfjas;lfjkas;ldfkjas;dlfkj;aslfkj;saldfkj;sadlfkjs;adlkfj;aslkfj;asldkfj;sadlfj;aslfj;asldjkf;saldjf;123",
        #         color="",
        #         slug="",
        #     )
