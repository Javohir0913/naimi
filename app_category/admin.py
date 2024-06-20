from django.contrib import admin

from .models import SubCategory, MainCategory, MiddleCategory


class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_name',)
    search_fields = ('main_name',)


class MiddleCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'middle_name',)
    list_filter = ('middle_name',)
    search_fields = ('middle_name',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_name', 'main_category_id', 'middle_category_id')
    list_filter = ('main_category_id', 'middle_category_id')
    search_fields = ('sub_name', 'main_category_id', 'middle_category_id')


# Register your models here.
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(MiddleCategory, MiddleCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
