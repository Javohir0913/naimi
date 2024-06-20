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
        services = Service.objects.filter(category_id=obj.id)

        data = []
        for service in services:
            if service:
                comments = FeedbackModel.objects.filter(service=service)
                for comment in comments:
                    images = FeedbackImageModel.objects.filter(comment=comment)
                    image_urls = [self.context['request'].build_absolute_uri(image.image.url) for image in images]

                    comment_info = {
                        'id': comment.id,
                        'msg': comment.msg,
                        'mark': comment.mark,
                        'created_at': comment.created_at,
                        'price': comment.price,
                        'images': image_urls
                    }
                    data.append(comment_info)
        return data


