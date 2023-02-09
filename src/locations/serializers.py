from rest_framework import serializers
from .models import Location
from characters.serializers import CharacterSerializer


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
