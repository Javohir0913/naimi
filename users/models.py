from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, lat, lan, password=None):

        user = self.model(phone=phone, lan=lan, lat=lat)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, lan, lat,password=None):

        user = self.create_user(phone=phone, password=password, lan=lan, lat=lat)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    lan = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['lan', 'lat']

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'User'
        db_table = 'users'


class PhoneVerification(models.Model):
    phone = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.phone} - {self.code}'

    def generate_code(self):
        self.code = ''.join(random.choices(string.digits, k=6))
        self.save()


class ProfileModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to="profile")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rule = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Profile'
        db_table = 'Profile_table'


class ProfileImageModel(models.Model):
    user_id = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='owner')
    image = models.ImageField(upload_to='ProfileImages')

    def __str__(self):
        return self.image.name

    class Meta:
        db_table = 'profile_images'
        verbose_name = 'Profile Images'


class ProfileVideoModel(models.Model):
    user_id = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='profile')
    video = models.FileField(upload_to='ProfileVideos')

    def __str__(self):
        return self.video.name

    class Meta:
        db_table = 'profile_videos'
        verbose_name = 'Profile Videos'


class FavoriteModel(models.Model):
    owner_id = models.ForeignKey(ProfileModel, related_name='favorite_profile', on_delete=models.CASCADE)
    profile_id = models.ForeignKey(ProfileModel, related_name='favorite_profiles', blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.owner_id.first_name)
