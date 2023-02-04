from rest_framework import serializers
from .models import Character


# DEPENDENCY SERIALIZER
class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['name', 'occupation', 'date_of_birth', 'suspect']


# # PACKAGE SERIALIZER
# class PackageSerializer(serializers.ModelSerializer):
# 	dependencies = serializers.StringRelatedField(many=True)
#
# 	class Meta:
# 		model = Package
# 		fields = ['id', 'name', 'description', 'dependencies', 'link']
