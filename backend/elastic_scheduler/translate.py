# converters.py
from elastisched.blob import Blob
from elastisched.timerange import TimeRange
import engine
from engine import Tag
from .models import BlobModel, TagModel
from pytz import timezone
from .constants import *


def policy(is_splittable, is_overlappable, is_invisible):
    bitfield = 0
    if is_splittable:
        bitfield |= BIT_SPLITTABLE
    if is_overlappable:
        bitfield |= BIT_OVERLAPPABLE
    if is_invisible:
        bitfield |= BIT_INVISIBLE

    return bitfield


def model_to_tag(model: TagModel) -> Tag:
    return Tag(model.name)


def tag_to_model(tag: Tag) -> TagModel:
    obj, _ = TagModel.objects.get_or_create(name=tag.get_name())
    return obj


def model_to_blob(model: BlobModel) -> Blob:
    return Blob(
        name=model.name,
        description=model.description,
        tz=timezone(model.tz),
        default_scheduled_timerange=TimeRange(
            model.default_start,
            model.default_end,
        ),
        schedulable_timerange=TimeRange(
            model.schedulable_start,
            model.schedulable_end,
        ),
        policy=engine.Policy(
            model.max_splits,
            model.min_split_duration.seconds,
            policy(model.is_splittable, model.is_overlappable, model.is_invisible),
        ),
        dependencies=set(model.dependencies),
        tags={engine.Tag(tag.name) for tag in model.tags.all()},
    )


def blob_to_model(blob: Blob) -> BlobModel:
    obj = BlobModel.objects.create(
        name=blob.name,
        description=blob.description,
        tz=str(blob.tz),
        default_start=blob.default_scheduled_timerange.start,
        default_end=blob.default_scheduled_timerange.end,
        schedulable_start=blob.schedulable_timerange.start,
        schedulable_end=blob.schedulable_timerange.end,
        is_splittable=blob.policy.isSplittable(),
        is_overlappable=blob.policy.isOverlappable(),
        is_invisible=blob.policy.isInvisible(),
        max_splits=blob.policy.max_splits,
        min_split_duration=blob.policy.min_split_duration,
        dependencies=blob.dependencies,
    )
    for tag in blob.tags:
        tag_obj, _ = TagModel.objects.get_or_create(name=tag.name)
        obj.tags.add(tag_obj)
    return obj
