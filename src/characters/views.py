import django_filters

from rest_framework import status, filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Character, Location
from .serializer import CharacterSerializer, LocationDetailSerializer, LocationListSerializer
from django_filters import rest_framework as f

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class CharacterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    occupation = django_filters.CharFilter(lookup_expr='icontains')
    suspect = django_filters.BooleanFilter()

    class Meta:
        model = Character
        fields = ['name', 'occupation', 'suspect']


class LocationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    created = django_filters.DateRangeFilter()
    character = django_filters.CharFilter(field_name="character__name", lookup_expr="icontains")
    longitude = django_filters.NumberFilter(field_name="longitude", method="filter_by_distance", label="longitude")
    latitude = django_filters.NumberFilter(field_name="latitude", method="filter_by_distance", label="latitude")
    radius = django_filters.NumberFilter(field_name="radius", method="filter_by_distance", label="Radius")

    class Meta:
        model = Location
        fields = ['name', 'longitude', 'latitude', 'radius', 'created', 'character']

    def filter_by_distance(self, queryset, name, value):
        point = Point(float(self.data['longitude']), float(self.data['latitude']))
        return queryset.filter(
            coordinates__distance_lte=(point, Distance(m=float(self.data['radius'])))
        )


class CharacterList(GenericAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = [f.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CharacterFilter
    search_fields = ['name', 'occupation', 'suspect', 'date_of_birth']
    ordering_fields = ['name', 'date_of_birth']

    def get(self, request):
        characters = self.filter_queryset(self.get_queryset())

        ordering = self.request.query_params.get('ordering', 'name')
        ordering_direction = self.request.query_params.get('ascending', '1')

        if ordering_direction == '0':
            ordering = '-' + ordering

        characters = characters.order_by(ordering)

        serializer = self.serializer_class(characters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacterDetail(GenericAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    filter_backends = [f.DjangoFilterBackend]
    filterset_class = CharacterFilter

    def get_character(self, pk):
        try:
            return Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            return Response({"detail": f"Character with ID {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            character = self.get_character(pk)
            serializer = CharacterSerializer(character)
            return Response(serializer.data)
        except Exception as err:
            return Response({"detail": f"Character with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            character = self.get_character(pk)
            serializer = CharacterSerializer(character, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"detail": f"Character with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            character = self.get_character(pk)
            character.delete()
            return Response({"detail": f"Character with ID {pk} was removed!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response({"detail": f"Character with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)


class LocationList(GenericAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer
    filter_backends = [f.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LocationFilter
    search_fields = ['name', 'created', 'character']

    def get(self, request):
        locations = self.filter_queryset(self.get_queryset())

        serializer = self.serializer_class(locations, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = LocationListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetail(GenericAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer

    def get_location(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return Response({"detail": f"Location with ID {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            location = self.get_location(pk)
            serializer = LocationDetailSerializer(location)
            return Response(serializer.data)
        except Exception as err:
            return Response({"detail": f"Location with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            location = self.get_location(pk)
            serializer = LocationDetailSerializer(location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"detail": f"Location with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            location = self.get_location(pk)
            location.delete()
            return Response({"detail": f"Location with ID {pk} was removed!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response({"detail": f"Location with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)