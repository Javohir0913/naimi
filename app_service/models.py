from django.db import models
from django.contrib.auth import get_user_model
from users.models import ProfileModel

User = get_user_model()


class Service(models.Model):
    service_name = models.CharField(max_length=255, blank=True, null=True)
    service_price = models.IntegerField(null=True, blank=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    owner_id = models.ForeignKey(ProfileModel, on_delete=models.DO_NOTHING, blank=True, null=True)
    category_id = models.ForeignKey('app_category.SubCategory', blank=True, null=True, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.service_name

    class Meta:
        db_table = 'service'
        verbose_name = 'Service'
        verbose_name_plural = 'Service'
