from django.db import models


# Create your models here.
class MainCategory(models.Model):
    main_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.main_name}"

    class Meta:
        verbose_name_plural = 'MainCategories'
        verbose_name = 'MainCategory'
        db_table = 'main_category'


class MiddleCategory(models.Model):
    middle_name = models.CharField(max_length=255)
    middle_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    main_category_id = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.middle_name}"

    class Meta:
        verbose_name_plural = 'MiddleCategories'
        verbose_name = 'MiddleCategory'
        db_table = 'middle_category'


class SubCategory(models.Model):
    sub_name = models.CharField(max_length=255)
    middle_category_id = models.ForeignKey(MiddleCategory, on_delete=models.CASCADE)
    main_category_id = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sub_name}"

    class Meta:
        verbose_name_plural = 'SubCategories'
        verbose_name = 'SubCategory'
        db_table = 'sub_category'
