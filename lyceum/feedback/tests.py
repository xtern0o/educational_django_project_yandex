import django.test
import django.urls
import parameterized

import feedback.forms
import feedback.models


__all__ = []


class FeedbackTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_feedback_context(self):
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback"),
        )
        form = response.context["form"]
        self.assertIsInstance(form, feedback.forms.FeedbackForm)

    @parameterized.parameterized.expand(
        [
            ("text", "Ваш текст"),
            ("mail", "Почта"),
            ("name", "Имя отправителя"),
        ],
    )
    def test_feedback_labels(self, field, expected_text):
        label = self.form.fields[field].label
        self.assertEqual(label, expected_text)

    @parameterized.parameterized.expand(
        [
            ("text", "Ваши впечатления, вопросы"),
            ("mail", "Ваш электронный адрес"),
            ("name", "Имя, указанное в качестве автора письма"),
        ],
    )
    def test_feedback_help_texts(self, field, expected_text):
        help_text = self.form.fields[field].help_text
        self.assertEqual(help_text, expected_text)

    def test_feedback_redirect_after_submit(self):
        form_data = {
            "text": "Test text for feedback",
            "mail": "test@mail.com",
            "name": "Test Name",
        }
        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )

    def test_correct_data_form_submit(self):
        form_data = {
            "text": "Good text",
            "mail": "good@mail.ru",
            "name": "Test Name",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertTrue(form.is_valid())

    def test_incorrect_data_form_submit(self):
        form_data = {
            "text": "Bad text",
            "mail": "a@a.a",
            "name": "bad name",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Некорректный e-mail адрес", form.errors["mail"])

    def test_empty_fields(self):
        form_data = {
            "text": "",
            "mail": "",
            "name": "",
        }
        form = feedback.forms.FeedbackForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("mail"))
        self.assertTrue(form.has_error("text"))

    def test_save_correct_feedback_form_in_model(self):
        form_data = {
            "text": "some text",
            "mail": "test@mail.com",
            "name": "Some Name",
        }
        count = feedback.models.Feedback.objects.count()
        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            count + 1,
        )

    def test_save_incorrect_feedback_form_in_model(self):
        form_data = {
            "text": "some text",
            "mail": "a@ma.a",
            "name": "Some Name",
        }
        count = feedback.models.Feedback.objects.count()
        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            count,
        )
