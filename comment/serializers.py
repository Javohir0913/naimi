from rest_framework import serializers
from .models import FeedbackModel, FAQModel, FeedbackImageModel
from app_category.models import SubCategory
from app_service.models import Service


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


class GetFeedbackWithSubIdSerializer(serializers.ModelSerializer):
    msg = serializers.SerializerMethodField(method_name='get_msg', read_only=True)
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)

    class Meta:
        model = SubCategory
        fields = ['msg', 'comments']

    def get_msg(self, obj):
        return 'successfully'

    def get_comments(self, obj):
        profiles = Service.objects.filter(category_id=obj.id).values('id', 'owner_id', ).distinct()
        print(profiles)
        comments = [FeedbackModel.objects.filter(owner=profile.get('owner_id'), service=profile.get('id'))
                    for profile in profiles]
        print(comments)
        data = []
        for comment in comments:
            if comment.values():
                data.append(comment.values())
        return data

