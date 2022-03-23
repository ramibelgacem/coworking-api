from django.db import models

from management.base_model import TrackTimeModel

class Company(TrackTimeModel):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
