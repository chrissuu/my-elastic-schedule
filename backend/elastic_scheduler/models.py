from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from ..elastisched import Blob

class BlobModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField()

    def save_blob(self, blob):
        """
        Store the blob (instance of your Blob dataclass) into the model.
        """
        self.id = uuid.UUID(blob.id) if not isinstance(blob.id, uuid.UUID) else blob.id
        self.data = blob.to_dict()
        self.save()

    def get_blob(self):
        """
        Return a Blob instance from the stored JSON data.
        """
        return Blob.from_dict(self.data)

    def __str__(self):
        return f"BlobModel {self.id}"
    

