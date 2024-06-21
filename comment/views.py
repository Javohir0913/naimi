from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import FeedbackFilterSet, FeedbackWithSubIdFilterSet
from .models import FeedbackModel, FAQModel, FeedbackImageModel
from .paginations import StandardResultsSetPagination
from .permissions import IsAdminOrReadOnly
from .serializers import FeedbackSerializer, FAQsSerializer, FeedbackImageSerializer,\
    GetFeedbackSerializer
from users.models import ProfileModel
from app_category.models import SubCategory


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = FeedbackModel.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['post', 'delete']

    def perform_create(self, serializer):
        owner = ProfileModel.objects.get(pk=self.request.user.id)
        serializer.save(owner=owner)


class GetFeedBackWithProfileIdView(ListAPIView):
    queryset = FeedbackModel.objects.all()
    serializer_class = GetFeedbackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackFilterSet
    pagination_class = StandardResultsSetPagination


class FeedbackImageViewSet(viewsets.ModelViewSet):
    queryset = FeedbackImageModel.objects.all()
    serializer_class = FeedbackImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['post', ]


class FAQsViewSet(viewsets.ModelViewSet):
    queryset = FAQModel.objects.all()
    serializer_class = FAQsSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        try:
            if self.request.query_params['role'] is not None:
                role = self.request.query_params['role']
                if role in ['Customer', 'Expert']:
                    return FAQModel.objects.filter(role=role)
                return FAQModel.objects.all()
        except:
            return FAQModel.objects.all()


class GetFeedbackWithSubIdView(ListAPIView):
    queryset = FeedbackModel.objects.all()
    serializer_class = GetFeedbackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackWithSubIdFilterSet
    pagination_class = StandardResultsSetPagination

