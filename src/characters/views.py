from django.shortcuts import render

# Import Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Character
from .serializer import CharacterSerializer


@api_view(['GET', 'POST'])
def all_characters(request):
    """
    GET: Get all characters stored in the database.
    POST: Create new character.
    {
        "name": "string",
        "occupation": "string",
        "date_of_birth": "string",
        "suspect": boolean
    }
    """
    if request.method == 'GET':
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)

        return Response({"characters": serializer.data})

    if request.method == 'POST':

        serializer = CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_character(request, id):
    """
    Use this endpoint with any of the following methods
    GET: To get a single character by ID
    POST: To update a single character by ID
    """
    if request.method == 'GET':
        try:
            character = Character.objects.get(id=id)
            serializer = CharacterSerializer(character, many=False)
            if character:
                return Response(serializer.data, status=status.HTTP_302_FOUND)
        except Exception as err:
            return Response({"detail": f"Character with ID {id} not found!"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        try:
            character = Character.objects.get(id=id)
            serializer = CharacterSerializer(instance=character, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({"detail": f"Character with ID {id} not found!"}, status=status.HTTP_404_NOT_FOUND)