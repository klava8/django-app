from django.db import models
import os

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='./')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    exported_at = models.DateTimeField(null=True, blank=True)
    file_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.file.name

    def increment_download_count(self):
        self.download_count += 1
        self.save()

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)

        super().delete(*args, **kwargs)