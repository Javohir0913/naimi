from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ProfileModel, ProfileImageModel, ProfileVideoModel, FavoriteModel
from comment.models import FeedbackImageModel
from comment.serializers import FeedbackImageSerializer, GetFeedbackImageSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['phone', 'lat', 'lan']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(phone=validated_data['phone'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'


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


class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImageModel
        fields = ['image']

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(instance.image.url)
        return instance.image.url


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileVideoModel
        fields = '__all__'
        extra_kwargs = {
            'user_id': {
                'read_only': True
            }
        }


class GetVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileVideoModel
        fields = ['video']

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(instance.video.url)
        return instance.video.url


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteModel
        fields = '__all__'
        extra_kwargs = {
            'owner_id': {'read_only': True}
        }


class GetProfileImagesAndFeedbackImagesSerializer(serializers.ModelSerializer):
    profile_images = serializers.SerializerMethodField()
    profile_videos = serializers.SerializerMethodField()
    feedback_images = serializers.SerializerMethodField()

    class Meta:
        model = ProfileModel
        fields = ['profile_images', 'profile_videos', 'feedback_images']

    def get_profile_images(self, obj):
        images = ProfileImageModel.objects.filter(user_id=obj.id)
        serializer = GetImageSerializer(images, many=True, context={'request': self.context.get('request')})
        return serializer.data

    def get_profile_videos(self, obj):
        videos = ProfileVideoModel.objects.filter(user_id=obj.id)
        serializer = GetVideoSerializer(videos, many=True, context={'request': self.context.get('request')})
        return serializer.data

    def get_feedback_images(self, obj):
        images = FeedbackImageModel.objects.filter(profile_id=obj.id)
        serializer = GetFeedbackImageSerializer(images, many=True, context={'request': self.context.get('request')})
        return serializer.data