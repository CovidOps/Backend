from djongo import models
from .point import Point

class CommunityPost(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    phone = models.TextField()
    area = models.TextField()
    details = models.TextField()
    item = models.TextField()
    type = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    location = models.EmbeddedField(
        model_container=Point
    )
    person_id = models.TextField()
    objects = models.DjongoManager()