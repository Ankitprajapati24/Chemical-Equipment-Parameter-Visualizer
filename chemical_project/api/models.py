from django.db import models

class EquipmentFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Statistics columns
    total_count = models.IntegerField(default=0)
    avg_temp = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_flow = models.FloatField(default=0.0)

    def __str__(self):
        return f"Upload at {self.uploaded_at}"