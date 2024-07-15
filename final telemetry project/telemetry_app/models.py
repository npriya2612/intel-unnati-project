from django.db import models

class TelemetryData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    platform = models.CharField(max_length=50)
    cpu_usage_percent = models.FloatField()
    cpu_frequency = models.FloatField()
    cpu_frequency_max = models.FloatField()
    cpu_frequency_min = models.FloatField()
    memory_usage_percent = models.FloatField()
    memory_total = models.BigIntegerField()
    memory_used = models.BigIntegerField()
    memory_free = models.BigIntegerField()
    bytes_sent = models.BigIntegerField()
    bytes_received = models.BigIntegerField()
    packets_sent = models.BigIntegerField()
    packets_received = models.BigIntegerField()
    energy_consumed = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Telemetry Data at {self.timestamp}"
