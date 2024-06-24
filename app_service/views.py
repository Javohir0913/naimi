from app_service.models import Service
from users.models import ProfileModel
from app_service.serializers import GetServiceSerializers, ServiceSerializers
from rest_framework import viewsets, permissions
from .permissions import IsStaffOrReadOnly


class ServiceViewset(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetServiceSerializers
        return ServiceSerializers

    def perform_create(self, serializer):
        profile = ProfileModel.objects.get(id=self.request.user.id)
        serializer.save(owner_id=profile)
