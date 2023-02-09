from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=250)
    occupation = models.CharField(max_length=250)
    date_of_birth = models.CharField(max_length=250)
    suspect = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name