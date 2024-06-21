from rest_framework import serializers
from rest_framework.fields import ListField, ImageField

from users.models import ProfileModel
from .models import FeedbackModel, FAQModel, FeedbackImageModel
from app_category.models import SubCategory
from app_service.models import Service


class GetFeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImageModel
        fields = ['image']

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(instance.image.url)
        return instance.image.url


class FeedbackSerializer(serializers.ModelSerializer):
    uploaded_images = ListField(
        child=ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    images = GetFeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = FeedbackModel
        fields = ['msg', 'mark', 'created_at', 'price', 'service', 'uploaded_images', 'images', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True},
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images')
        comment = FeedbackModel.objects.create(**validated_data)
        profile_id = comment.service.owner_id
        for image in images:
            FeedbackImageModel.objects.create(comment=comment, image=image, profile_id=profile_id)

        return comment


class GetFeedbackSerializer(serializers.ModelSerializer):
    images = GetFeedbackImageSerializer(read_only=True, many=True)

    class Meta:
        model = FeedbackModel
        fields = ['id', 'owner', 'msg', 'mark', 'created_at', 'price', 'service', 'images']


class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImageModel
        fields = '__all__'


class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQModel
        fields = '__all__'
