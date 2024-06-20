from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import FeedbackModel, FAQModel, FeedbackImageModel
from .permissions import IsAdminOrReadOnly
from .serializers import FeedbackSerializer, FAQsSerializer, FeedbackImageSerializer
from users.models import ProfileModel


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = FeedbackModel.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        owner = ProfileModel.objects.get(pk=self.request.user.id)
        serializer.save(owner=owner)


class FeedbackImageViewSet(viewsets.ModelViewSet):
    queryset = FeedbackImageModel.objects.all()
    serializer_class = FeedbackImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FAQsViewSet(viewsets.ModelViewSet):
    queryset = FAQModel.objects.all()
    serializer_class = FAQsSerializer
    permission_classes = [IsAdminOrReadOnly]

# class GetFeedbackWithSubId(RetrieveAPIView):
#     queryset =
