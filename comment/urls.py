from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet, FAQsViewSet, FeedbackImageViewSet

router = DefaultRouter()

router.register(r'feedbacks', FeedbackViewSet)
router.register(r'faqs', FAQsViewSet)
router.register(r'feedback-images', FeedbackImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
