# models.py
import uuid
from django.db import models
from django.utils.timezone import get_default_timezone

from .constants import *

class TagModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    group = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BlobModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100, default="Unnamed Blob")
    description = models.TextField(blank=True, null=True)

    tz = models.CharField(max_length=100, default=str(get_default_timezone()))

    default_start = models.CharField(default=ISOFORMAT_STRLEN)
    default_end = models.CharField(default=ISOFORMAT_STRLEN)

    schedulable_start = models.CharField(default=ISOFORMAT_STRLEN)
    schedulable_end = models.CharField(default=ISOFORMAT_STRLEN)

    is_splittable = models.BooleanField(default=False)
    is_overlappable = models.BooleanField(default=False)
    is_invisible = models.BooleanField(default=False)
    max_splits = models.IntegerField(default=0)
    min_split_duration = models.DurationField(default=0)

    dependencies = models.JSONField(default=list)

    tags = models.ManyToManyField(TagModel, blank=True)

    def __str__(self):
        return self.name
