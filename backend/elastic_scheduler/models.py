# models.py
import uuid
from django.db import models
from django.utils.timezone import get_default_timezone, get_current_timezone_name
from tzlocal import get_localzone_name

from .constants import *


class TagModel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BlobModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100, default="Unnamed Blob")
    description = models.TextField(blank=True, null=True)

    tz = models.CharField(max_length=100, default=get_localzone_name)

    default_start = models.DateTimeField()
    default_end = models.DateTimeField()

    schedulable_start = models.DateTimeField()
    schedulable_end = models.DateTimeField()

    is_splittable = models.BooleanField(default=False)
    is_overlappable = models.BooleanField(default=False)
    is_invisible = models.BooleanField(default=False)
    max_splits = models.IntegerField(default=0)
    min_split_duration = models.DurationField(default=0)

    dependencies = models.JSONField(default=list)

    tags = models.ManyToManyField(TagModel, blank=True)

    def __str__(self):
        return self.name
