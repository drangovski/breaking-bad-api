from django.db import models


# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=250)
    occupation = models.CharField(max_length=250)
    date_of_birth = models.CharField(max_length=250)
    suspect = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=250)
    longitude = models.FloatField()
    latitude = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete=models.DO_NOTHING, related_name='character')

    def __str__(self):
        return self.name