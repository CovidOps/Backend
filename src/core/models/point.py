from django.utils.translation import deactivate
from djongo import models
    

class Point(models.Model):
    _id = models.ObjectIdField()
    type = models.TextField(default="Point")
    coordinates = models.JSONField()

    def __str__(self):
        return self.coordinates
