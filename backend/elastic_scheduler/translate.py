# converters.py
from elastisched.blob import Blob
from elastisched.policy import Policy
from elastisched.tag import Tag
from elastisched.timerange import TimeRange
from .models import BlobModel, TagModel
from datetime import timezone

def model_to_blob(model: BlobModel) -> Blob:
    return Blob(
        id=str(model.id),
        name=model.name,
        description=model.description,
        tz=timezone.utc if str(model.tz) == "UTC" else timezone(tz=model.tz),
        default_scheduled_timerange=TimeRange(
            start=model.default_start,
            end=model.default_end,
        ),
        schedulable_timerange=TimeRange(
            start=model.schedulable_start,
            end=model.schedulable_end,
        ),
        policy=Policy(
            is_splittable=model.is_splittable,
            is_overlappable=model.is_overlappable,
            is_invisible=model.is_invisible,
            max_splits=model.max_splits,
            min_split_duration=model.min_split_duration,
        ),
        dependencies=model.dependencies,
        tags={Tag(name=tag.name) for tag in model.tags.all()}
    )

def blob_to_model(blob: Blob) -> BlobModel:
    obj = BlobModel.objects.create(
        id=blob.id,
        name=blob.name,
        description=blob.description,
        tz=str(blob.tz),
        default_start=blob.default_scheduled_timerange.start,
        default_end=blob.default_scheduled_timerange.end,
        schedulable_start=blob.schedulable_timerange.start,
        schedulable_end=blob.schedulable_timerange.end,
        is_splittable=blob.policy.is_splittable,
        is_overlappable=blob.policy.is_overlappable,
        is_invisible=blob.policy.is_invisible,
        max_splits=blob.policy.max_splits,
        min_split_duration=blob.policy.min_split_duration,
        dependencies=blob.dependencies,
    )
    for tag in blob.tags:
        tag_obj, _ = TagModel.objects.get_or_create(name=tag.name)
        obj.tags.add(tag_obj)
    return obj
