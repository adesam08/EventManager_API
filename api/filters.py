import django_filters   
from .models import Event
from rest_framework import filters


class EventFilter(django_filters.FilterSet):
    mine = django_filters.BooleanFilter(method='filter_mine', label='My events only')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['title', 'mine']

    def filter_mine(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(organizer__user=user)
        return queryset