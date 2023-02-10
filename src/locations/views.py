from rest_framework import status, filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Location
from .serializers import LocationDetailSerializer, LocationListSerializer
from django_filters import rest_framework as f
from .filters import LocationFilter


class LocationList(GenericAPIView):
    """
    This endpoint shows all of the existing locations stored in the database.
    Methods available for this endpoint are GE and POST.
    Documentation: https://drangovski.github.io
    """
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer
    filter_backends = [f.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = LocationFilter
    search_fields = ['name', 'created', 'character']
    ordering_fields = ['coordinates']

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
    """
    This endpoint shows the location details.
    Methods available for this endpoint are GET, PUT and DELETE.
    Documentation: https://drangovski.github.io
    """
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
