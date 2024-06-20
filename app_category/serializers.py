from rest_framework import serializers

from .models import MiddleCategory, SubCategory, MainCategory


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'


class MiddleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MiddleCategory
        fields = '__all__'
        depth = 1


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        depth = 1
