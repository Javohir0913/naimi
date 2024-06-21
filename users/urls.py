from rest_framework.routers import DefaultRouter
from .views import (RegisterView, VerifyView, PhoneTokenObtainView,
                    ProfileViewSet, LoginView,
                    ImageViewSet, VideoViewSet, GetMyProfileView, GetProfileWithSubId,
                    FavoriteViewSet, GetProfileImagesAndFeedbackImagesView, update_user)

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register('profile', ProfileViewSet, basename='profile')
router.register('profile-images', ImageViewSet, basename='image')
router.register('profile-videos', VideoViewSet, basename='video')
router.register('favourite', FavoriteViewSet, basename='favourite')

urlpatterns = router.urls

urlpatterns += [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/code/', LoginView.as_view(), name='code'),
    path('api/verify/', VerifyView.as_view(), name='verify'),
    path('api/token/phone/', PhoneTokenObtainView.as_view(), name='token_obtain_phone'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-profile/', GetMyProfileView.as_view(), name='my_profile'),
    path('update-admin/<int:pk>/', update_user, name='UpdateAdmin'),
    path('get-profile/sub-id/<int:pk>/', GetProfileWithSubId.as_view(), name='test'),
    path('get-profile-images-videos/<int:pk>/', GetProfileImagesAndFeedbackImagesView.as_view()),
]
