from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import FeedbackModel, FAQModel, FeedbackImageModel
from .permissions import IsAdminOrReadOnly
from .serializers import FeedbackSerializer, FAQsSerializer, FeedbackImageSerializer, GetFeedbackWithSubIdSerializer
from users.models import ProfileModel
from app_category.models import SubCategory


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = FeedbackModel.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        owner = ProfileModel.objects.get(pk=self.request.user.id)
        serializer.save(owner=owner)

    def get_queryset(self):
        try:
            if self.request.query_params['role'] is not None:
                role = self.request.query_params['role']
                if role in ['Customer', 'Expert']:
                    return FAQModel.objects.filter(role=role)
                return FAQModel.objects.all()
        except:
            return FAQModel.objects.all()


class FeedbackImageViewSet(viewsets.ModelViewSet):
    queryset = FeedbackImageModel.objects.all()
    serializer_class = FeedbackImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FAQsViewSet(viewsets.ModelViewSet):
    queryset = FAQModel.objects.all()
    serializer_class = FAQsSerializer
    permission_classes = [IsAdminOrReadOnly]


class GetFeedbackWithSubIdView(RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = GetFeedbackWithSubIdSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)


