from rest_framework import serializers
from .models import BlobModel, TagModel
from django.db import transaction


class TagListField(serializers.Field):
    """
    Custom field to handle tag creation/retrieval properly
    Accepts a list of tag dictionaries like [{"name": "tag1"}, {"name": "tag2"}]
    """

    def to_representation(self, value):
        """Convert tags to serialized format"""
        if not value:
            return []
        return [{"id": tag.id, "name": tag.name} for tag in value.all()]

    def to_internal_value(self, data):
        """Convert input data to internal format"""
        if not isinstance(data, list):
            raise serializers.ValidationError("Tags must be a list")

        tag_names = []
        for item in data:
            if isinstance(item, dict) and "name" in item:
                tag_name = str(item["name"]).strip()
                if tag_name:
                    tag_names.append(tag_name)
            elif isinstance(item, str):
                tag_name = item.strip()
                if tag_name:
                    tag_names.append(tag_name)
            else:
                raise serializers.ValidationError("Each tag must have a 'name' field")

        return tag_names


class BlobSerializer(serializers.ModelSerializer):
    tags = TagListField(required=False)

    class Meta:
        model = BlobModel
        fields = [
            "id",
            "name",
            "description",
            "tz",
            "default_start",
            "default_end",
            "schedulable_start",
            "schedulable_end",
            "is_splittable",
            "is_overlappable",
            "is_invisible",
            "max_splits",
            "min_split_duration",
            "dependencies",
            "tags",
        ]
        read_only_fields = ["id"]

    @transaction.atomic
    def create(self, validated_data):
        tag_names = validated_data.pop("tags", [])
        blob = BlobModel.objects.create(**validated_data)

        # Handle tags
        for tag_name in tag_names:
            tag_obj, created = TagModel.objects.get_or_create(name=tag_name)
            blob.tags.add(tag_obj)

        return blob

    @transaction.atomic
    def update(self, instance, validated_data):
        tag_names = validated_data.pop("tags", None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle tags if provided
        if tag_names is not None:
            instance.tags.clear()
            for tag_name in tag_names:
                tag_obj, created = TagModel.objects.get_or_create(name=tag_name)
                instance.tags.add(tag_obj)

        return instance


# Keep the original TagSerializer for other uses if needed
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ["id", "name"]
        read_only_fields = ["id"]
