from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ProfileModel, ProfileVideoModel, ProfileImageModel, PhoneVerification


class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone',)
    ordering = ('phone',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(ProfileVideoModel)
admin.site.register(ProfileModel)
admin.site.register(ProfileImageModel)
admin.site.register(PhoneVerification)
