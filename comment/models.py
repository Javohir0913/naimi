from django.db import models
from users.models import ProfileModel


from app_service.models import Service

User = ProfileModel


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)

    class Meta:
        abstract = True


class FeedbackModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Owner')
    msg = models.TextField()
    mark = models.IntegerField()
    created_at = models.DateField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service')

    def __str__(self):
        return f'Comment {self.pk} on Service {self.service}'

    class Meta:
        db_table = "feedback"


class FeedbackImageModel(models.Model):
    image = models.ImageField(upload_to='static/FeedbackImage/')
    comment = models.ForeignKey(FeedbackModel, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'CommentImage {self.pk} for Comment {self.comment}'

    class Meta:
        db_table = "FeedbackImage"


class FAQModel(BaseModel):
    class RoleChoice(models.TextChoices):
        customer = 'Customer', 'customer'
        expert = 'Expert', 'expert'

    question = models.TextField()
    answer = models.TextField()
    role = models.CharField(max_length=100, choices=RoleChoice.choices, default=RoleChoice.customer)

    def __str__(self) -> str:
        return self.answer

    class Meta:
        unique_together = (('question', 'answer'),)
        db_table = 'question_answer'
        verbose_name = 'Question Answer'

