from .models import BlobModel, TagModel
from .serializers import BlobSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .constants import *
from .translate import model_to_blob, blob_to_model
from datetime import datetime, timedelta
from typing import List
from elastisched.blob import Blob
from elastisched.timerange import TimeRange
import engine
import traceback
import json


class BlobViewSet(viewsets.ModelViewSet):
    queryset = BlobModel.objects.all()
    serializer_class = BlobSerializer

    def create(self, request):
        print("=== REQUEST DATA ===")
        print(request.data)

        try:
            request_data = dict(request.data)
            tags_data = request_data.pop("tags", [])

            print(f"Extracted tags_data: {tags_data} (type: {type(tags_data)})")

            normalized_tags = []
            if tags_data:
                for tag_item in tags_data:
                    if isinstance(tag_item, dict) and "name" in tag_item:
                        normalized_tags.append(tag_item["name"].strip())
                    elif isinstance(tag_item, str):
                        normalized_tags.append(tag_item.strip())
                    else:
                        print(f"Skipping invalid tag item: {tag_item}")

            print(f"Normalized tags: {normalized_tags}")

            serializer = self.get_serializer(data=request_data)

            print("=== SERIALIZER VALIDATION ===")
            if not serializer.is_valid():
                print("Serializer errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            print("Serializer is valid")

            blob_name = serializer.validated_data.get("name")
            print(f"=== CHECKING FOR EXISTING BLOB: {blob_name} ===")

            existing_blob = BlobModel.objects.filter(name=blob_name).first()
            if existing_blob:
                print(f"Blob already exists with ID: {existing_blob.id}")
                return Response(
                    {"message": "Model already exists", "id": existing_blob.id},
                    status=status.HTTP_200_OK,
                )

            print("=== CREATING NEW BLOB ===")

            new_blob_model = BlobModel.objects.create(**serializer.validated_data)
            print(f"Blob created successfully with ID: {new_blob_model.id}")

            if normalized_tags:
                print("=== PROCESSING TAGS ===")
                for i, tag_name in enumerate(normalized_tags):
                    if tag_name:  # Skip empty tag names
                        print(f"Processing tag {i+1}: '{tag_name}'")
                        try:
                            tag_obj, created = TagModel.objects.get_or_create(
                                name=tag_name
                            )
                            new_blob_model.tags.add(tag_obj)
                            print(
                                f"  Tag '{tag_name}' {'created' if created else 'found'} and added"
                            )
                        except Exception as tag_error:
                            print(f"  Error with tag '{tag_name}': {tag_error}")
                            continue

            print("=== BLOB CREATION COMPLETE ===")

            start = datetime.now()

            blob_models = BlobModel.objects.filter(
                schedulable_start__gte=start,
                schedulable_end__lte=start + SCHEDULING_WINDOW,
            )

            if not blob_models.exists():
                response_serializer = BlobSerializer(new_blob_model)
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )

            print("=== STARTING SCHEDULING OPTIMIZATION ===")
            blobs = [model_to_blob(blob_model) for blob_model in blob_models]

            blob_id_to_model_id = {
                blob.get_id(): blob_model.id
                for blob_model, blob in zip(blob_models, blobs)
            }

            blobs: List[Blob] = sorted(
                blobs, key=lambda blob: blob.get_schedulable_timerange().start
            )

            DAY: timedelta = timedelta(
                days=blobs[0].get_schedulable_timerange().start.weekday() + 1
            )
            NORMALIZE: datetime = blobs[0].get_schedulable_timerange().start
            START_EPOCH: datetime = NORMALIZE - DAY

            jobs = [blob.to_job(START_EPOCH) for blob in blobs]

            optimized_schedule = engine.schedule_jobs(
                jobs, int(FIFTEEN_MINUTES.total_seconds()), 1000.0, 1.0, 10000
            )

            assert len(optimized_schedule) == len(jobs)

            for job in optimized_schedule.scheduledJobs:
                if job.id in blob_id_to_model_id:
                    model_id = blob_id_to_model_id[job.id]

                    try:
                        print("Attempting to schedule...")
                        blob_model = BlobModel.objects.get(id=model_id)

                        blob_model.schedulable_start = (
                            timedelta(seconds=job.schedulableTimeRange.getLow())
                            + START_EPOCH
                        )
                        blob_model.schedulable_end = (
                            timedelta(seconds=job.schedulableTimeRange.getHigh())
                            + START_EPOCH
                        )
                        blob_model.default_start = (
                            timedelta(seconds=job.scheduledTimeRange.getLow())
                            + START_EPOCH
                        )
                        blob_model.default_end = (
                            timedelta(seconds=job.scheduledTimeRange.getHigh())
                            + START_EPOCH
                        )

                        blob_model.save()
                        print("Success!")

                    except BlobModel.DoesNotExist:
                        continue

            return Response(
                {"message": "Blob created and schedule updated."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print(f"=== FULL ERROR TRACEBACK ===")
            print(traceback.format_exc())
            return Response(
                {"error": f"Failed to process scheduling optimization with error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
