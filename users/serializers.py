from rest_framework import serializers
from .models import User, City, ProfileModel, ProfileImageModel, ProfileVideoModel, FavoriteModel
from app_category.models import SubCategory
from app_service.models import Service


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city')

    class Meta:
        model = User
        fields = ['phone', 'city_id']

    def create(self, validated_data):
        city = validated_data.pop('city')
        user = User.objects.create_user(phone=validated_data['phone'], city=city)
        return user


class VerificationSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=255)
    code = serializers.CharField(required=True, max_length=6)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = "__all__"
        extra_kwargs = {
            'user_id': {'read_only': True}
        }


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImageModel
        fields = '__all__'
        extra_kwargs = {
            'user_id': {
                'read_only': True
            }
        }


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileVideoModel
        fields = '__all__'
        extra_kwargs = {
            'user_id': {
                'read_only': True
            }
        }


class GetProfileWithSubIdSerializer(serializers.ModelSerializer):
    profiles = serializers.SerializerMethodField(method_name='get_profiles', read_only=True)
    msg = serializers.SerializerMethodField(method_name='get_msg', read_only=True)

    class Meta:
        model = SubCategory
        fields = ['msg', 'profiles']

    def get_msg(self, obj):
        return 'successfully'

    def get_profiles(self, obj):
        services = Service.objects.filter(category_id=obj.id).values('owner_id', ).distinct()
        profiles = [ProfileModel.objects.filter(id=service.get('owner_id')) for service in services]
        data = []
        for profile in profiles:
            data.append(profile.values())
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteModel
        fields = '__all__'
        extra_kwargs = {
            'owner_id': {'read_only': True}
        }
