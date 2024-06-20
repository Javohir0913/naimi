from rest_framework.routers import DefaultRouter

from .views import MainCategoryViewSet, MiddleCategoryViewSet, SubCategoryViewSet


router = DefaultRouter()

router.register('main-category', MainCategoryViewSet)
router.register('middle-category', MiddleCategoryViewSet)
router.register('sub-category', SubCategoryViewSet)

urlpatterns = router.urls
