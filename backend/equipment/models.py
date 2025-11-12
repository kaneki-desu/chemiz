from django.db import models

class EquipmentDataset(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField(default=dict)

    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
