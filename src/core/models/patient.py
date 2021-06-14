from djongo import models
from .point import Point

class Patient(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    phone = models.TextField()
    area = models.TextField()
    address = models.TextField()
    location = models.EmbeddedField(
        model_container=Point
    )
    objects = models.DjongoManager()