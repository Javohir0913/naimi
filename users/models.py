from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        db_table = 'City_table'


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, city=None):
        if not phone:
            raise ValueError('The Phone number field is required')
        if not city:
            raise ValueError('The City field is required')

        user = self.model(phone=phone, city=city)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, city=None):
        try:
            city_instance = City.objects.get(id=city)
        except City.DoesNotExist:
            raise ValueError('The City with the given id does not exist')

        user = self.create_user(phone=phone, password=password, city=city_instance)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=255, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['city']

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

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Profile'
        db_table = 'Profile_table'


class ProfileImageModel(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ProfileImages')

    def __str__(self):
        return self.image.name

    class Meta:
        db_table = 'profile_images'
        verbose_name = 'Profile Images'


class ProfileVideoModel(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.FileField(upload_to='ProfileVideos')

    def __str__(self):
        return self.video.name

    class Meta:
        db_table = 'profile_videos'
        verbose_name = 'Profile Videos'


class Favourite(models.Model):
    owner_id = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    profiles_id = models.ManyToManyField(ProfileModel, related_name='profiles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.owner_id.phone
