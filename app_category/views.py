from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .models import MainCategory, MiddleCategory, SubCategory
from .serializers import MainCategorySerializer, MiddleCategorySerializer, SubCategorySerializer
from .permissions import GetOrAdmin


# Create your views here.
class MainCategoryViewSet(ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    permission_classes = (GetOrAdmin,)


class MiddleCategoryViewSet(ModelViewSet):
    queryset = MiddleCategory.objects.all()
    serializer_class = MiddleCategorySerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    permission_classes = (GetOrAdmin,)


class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    permission_classes = (GetOrAdmin,)
