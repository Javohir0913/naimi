from app_service.views import ServiceViewset
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'service', ServiceViewset)

urlpatterns = router.urls
