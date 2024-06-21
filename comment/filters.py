from django_filters.filterset import FilterSet, CharFilter

from .models import FeedbackModel


class FeedbackFilterSet(FilterSet):
    profile_id = CharFilter(field_name='service__owner_id', lookup_expr='exact', required=True)
    category_id = CharFilter(field_name='service__category_id', lookup_expr='exact')

    class Meta:
        model = FeedbackModel
        fields = ['profile_id', 'category_id']


class FeedbackWithSubIdFilterSet(FilterSet):
    sub_id = CharFilter(field_name='service__category_id', lookup_expr='exact', required=True)

    class Meta:
        model = FeedbackModel
        fields = ['sub_id', ]
