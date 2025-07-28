from rest_framework import serializers
from .models import BlobModel, TagModel

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['id', 'name', 'group']
        read_only_fields = ['id']

class BlobSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)  # Nested serialization

    class Meta:
        model = BlobModel
        fields = [
            'id',
            'name',
            'description',
            'tz',
            'default_start',
            'default_end',
            'schedulable_start',
            'schedulable_end',
            'is_splittable',
            'is_overlappable',
            'is_invisible',
            'max_splits',
            'min_split_duration',
            'dependencies',
            'tags'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blob = BlobModel.objects.create(**validated_data)
        for tag in tags_data:
            tag_obj, _ = TagModel.objects.get_or_create(**tag)
            blob.tags.add(tag_obj)
        return blob

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.clear()
            for tag in tags_data:
                tag_obj, _ = TagModel.objects.get_or_create(**tag)
                instance.tags.add(tag_obj)

        return instance
