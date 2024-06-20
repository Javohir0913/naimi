from django.contrib import admin

from .models import FAQModel, FeedbackModel, FeedbackImageModel

admin.site.register(FeedbackModel)
admin.site.register(FAQModel)
admin.site.register(FeedbackImageModel)
