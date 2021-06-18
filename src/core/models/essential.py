from djongo import models

class State(models.Model):
    state = models.TextField()
    url = models.TextField()
    
    class Meta:
        abstract = True

class Essential(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    urls = models.ArrayField(
        model_container=State
    )

class SingleUrlEssential(models.Model):
    _id = models.ObjectIdField()
    name = models.TextField()
    url = models.TextField()