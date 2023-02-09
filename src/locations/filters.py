import django_filters
from .models import Location
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class LocationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    created = django_filters.DateRangeFilter()
    character = django_filters.CharFilter(field_name="character__name", lookup_expr="icontains")
    longitude = django_filters.NumberFilter(field_name="longitude", method="filter_by_distance", label="Longitude")
    latitude = django_filters.NumberFilter(field_name="latitude", method="filter_by_distance", label="Latitude")
    radius = django_filters.NumberFilter(field_name="radius", method="filter_by_distance", label="Radius (m)")
    ascending = django_filters.NumberFilter(field_name="ascending", method="filter_by_distance", label="Ascending", required=False)

    class Meta:
        model = Location
        fields = ['name', 'longitude', 'latitude', 'ascending', 'radius', 'created', 'character']

    def filter_by_distance(self, queryset, *args, **kwargs):
        if 'ascending' in self.data:
            order_direction = "coordinates"

            if self.data['ascending'] == '1':
                order_direction = "coordinates"
            if self.data['ascending'] == '0':
                order_direction = "-coordinates"

            point = Point(float(self.data['longitude']), float(self.data['latitude']))
            return queryset.filter(
                coordinates__distance_lte=(point, Distance(m=float(self.data['radius'])))
            ).order_by(order_direction)
        else:
            point = Point(float(self.data['longitude']), float(self.data['latitude']))
            return queryset.filter(
                coordinates__distance_lte=(point, Distance(m=float(self.data['radius'])))
            )
