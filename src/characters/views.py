from django.shortcuts import render

# Import Django Rest Framework

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Character
from .serializer import CharacterSerializer
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Q


class CharacterList(APIView):
    """
    List all characters or create a new one.
    """
    def get(self, request, format=None):
        all_characters = Character.objects.all()

        name = request.query_params.get('name')
        occupation = request.query_params.get('occupation')
        suspect = request.query_params.get('suspect')

        characters = all_characters

        if name is None and occupation:
            characters = characters.filter(Q(occupation__icontains=occupation))
        elif occupation is None and name:
            characters = characters.filter(Q(name__icontains=name))
        elif name and occupation:
            characters = characters.filter(Q(name__icontains=name) | Q(occupation__icontains=occupation))

        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacterDetail(APIView):
    def get_character(self, pk):
        try:
            return Character.objects.get(pk=pk)
        except Character.DoesNotExist:
            return Response({"detail": f"Character with ID {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        try:
            character = self.get_character(pk)
            serializer = CharacterSerializer(character)
            return Response(serializer.data)
        except Exception as err:
            return Response({"detail": f"Character with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        try:
            character = self.get_character(pk)
            serializer = CharacterSerializer(character, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"detail": f"Character with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        try:
            character = self.get_character(pk)
            character.delete()
            return Response({"detail": f"Character with ID {pk} was removed!"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response({"detail": f"Character with id {pk} does not exist!"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET', 'POST'])
# def all_characters(request):
#     """
#     GET: Get all characters stored in the database.
#     POST: Create new character.
#     {
#         "name": "string",
#         "occupation": "string",
#         "date_of_birth": "string",
#         "suspect": boolean
#     }
#     """
#     if request.method == 'GET':
#         characters = Character.objects.all()
#         serializer = CharacterSerializer(characters, many=True)
#
#         return Response({"characters": serializer.data})
#
#     if request.method == 'POST':
#
#         serializer = CharacterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def get_character(request, id):
#     """
#     Use this endpoint with any of the following methods
#     GET: To get a single character by ID
#     POST: To update a single character by ID
#     """
#     if request.method == 'GET':
#         try:
#             character = Character.objects.get(id=id)
#             serializer = CharacterSerializer(character, many=False)
#             if character:
#                 return Response(serializer.data, status=status.HTTP_302_FOUND)
#         except Exception as err:
#             return Response({"detail": f"Character with ID {id} not found!"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'PUT':
#         try:
#             character = Character.objects.get(id=id)
#             serializer = CharacterSerializer(instance=character, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as err:
#             return Response({"detail": f"Character with ID {id} not found!"}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'DELETE':
#         try:
#             character = Character.objects.get(id=id)
#             character.delete()
#             return Response({"detail": f"Character with ID {id} was removed!"}, status=status.HTTP_204_NO_CONTENT)
#         except Exception as err:
#             return Response({"detail": f"Character with ID {id} not found!"}, status=status.HTTP_404_NOT_FOUND)