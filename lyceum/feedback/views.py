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
            text = form.cleaned_data.get("text")
            mail = form.cleaned_data.get("mail")
            new_feedback = feedback.models.FeedbackModel.objects.create(
                text=text,
                mail=mail,
            )
            new_feedback.full_clean()
            new_feedback.save()

            django.core.mail.send_mail(
                "FROM: {}".format(mail),
                text,
                django.conf.settings.EMAIL_ADDRESS,
                [mail],
                fail_silently=False,
            )

            django.contrib.messages.success(
                request=request,
                message="Форма успешно отправлена! Спасибо за Ваш отзыв!",
                extra_tags="alert alert-success",
            )

            return django.shortcuts.redirect("feedback:feedback")

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)
