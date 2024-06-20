from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, City, ProfileModel, ProfileVideoModel, ProfileImageModel, PhoneVerification


class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'city', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('city',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'city', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(City)
admin.site.register(ProfileVideoModel)
admin.site.register(ProfileModel)
admin.site.register(ProfileImageModel)
admin.site.register(PhoneVerification)
