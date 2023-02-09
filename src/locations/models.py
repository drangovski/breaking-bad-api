from django.db import models
from characters.models import Character
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point


class Location(models.Model):
    name = models.CharField(max_length=250)
    longitude = models.FloatField()
    latitude = models.FloatField()
    coordinates = gis_models.PointField(default=Point(0, 0), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name='character')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.coordinates = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)