from django.contrib import admin


import feedback.models


__all__ = []


@admin.register(feedback.models.FeedbackModel)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.FeedbackModel.name.field.name,
        feedback.models.FeedbackModel.status.field.name,
    )

    list_display_links = (feedback.models.FeedbackModel.name.field.name,)

    readonly_fields = (
        feedback.models.FeedbackModel.name.field.name,
        feedback.models.FeedbackModel.text.field.name,
        feedback.models.FeedbackModel.mail.field.name,
    )

    list_editable = (feedback.models.FeedbackModel.status.field.name,)

    def save_model(self, request, obj, form, change):
        user = request.user
        old_status = feedback.models.FeedbackModel.objects.get(
            pk=obj.pk
        ).status
        super().save_model(request, obj, form, change)
        new_status = form.cleaned_data["status"]

        feedback.models.StatusLog.objects.create(
            user=user,
            from_status=old_status,
            to=new_status,
            feedback=obj,
        )
