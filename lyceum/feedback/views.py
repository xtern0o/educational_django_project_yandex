import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts

import feedback.forms
import feedback.models


__all__ = []


def feedback_view(request):
    template = "feedback/feedback.html"
    form = feedback.forms.FeedbackForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_feedback = feedback.models.Feedback()

            new_feedback.name = form.cleaned_data.get("name")
            new_feedback.text = form.cleaned_data.get("text")
            new_feedback.mail = form.cleaned_data.get("mail")
            new_feedback.save()

            django.core.mail.send_mail(
                "FROM: {}".format(new_feedback.mail),
                new_feedback.text,
                django.conf.settings.EMAIL_ADDRESS,
                [new_feedback.mail],
                fail_silently=False,
            )

            django.contrib.messages.success(
                request=request,
                message="Форма успешно отправлена! Спасибо за Ваш отзыв!",
            )

            return django.shortcuts.redirect("feedback:feedback")

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)
