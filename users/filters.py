from django_filters.filterset import FilterSet, CharFilter

from app_service.models import Service
from .models import ProfileModel


class GetProfileWithSubIdFilterSet(FilterSet):
    sub_id = CharFilter(method='filter_by_sub_id', label='SubCategory Id')

    class Meta:
        model = ProfileModel
        fields = []

    def filter_by_sub_id(self, queryset, name, value):
        services = Service.objects.filter(category_id=value).values_list('owner_id', flat=True).distinct()
        return queryset.filter(id__in=services).order_by('id')
