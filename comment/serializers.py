from rest_framework import serializers
from .models import FeedbackModel, FAQModel, FeedbackImageModel


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackModel
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackImageModel
        fields = '__all__'


class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQModel
        fields = '__all__'
