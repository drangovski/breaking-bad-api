import django_filters
from .models import Character


class CharacterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    occupation = django_filters.CharFilter(lookup_expr='icontains')
    suspect = django_filters.BooleanFilter()

    class Meta:
        model = Character
        fields = ['name', 'occupation', 'suspect']


