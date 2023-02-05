from rest_framework import serializers
from .models import Character, Location


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'occupation', 'date_of_birth', 'suspect']


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'longitude', 'latitude', 'created', 'character']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        character = representation.pop('character')
        representation['character'] = {
            "id": instance.character.id,
            "name": instance.character.name,
            "details": self.context['request'].build_absolute_uri(
                f'/api/characters/{instance.character.id}'
            ),
        }
        return representation


class LocationDetailSerializer(serializers.ModelSerializer):
    character = CharacterSerializer(read_only=True)
    class Meta:
        model = Location
        fields = ['id', 'name', 'longitude', 'latitude', 'created', 'character']
