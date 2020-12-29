from django.db import models

# Create your models here.



class SwitchControl(models.Model):
    NodeID = models.CharField(max_length=30)
    SwitchID = models.CharField(max_length=30)
    DeviceID = models.CharField(max_length=30)
    Description = models.CharField(max_length=30)
    Power = models.DecimalField

    def __str__(self):
        return self.title


class SwitchState(models.Model):
    NodeID = models.CharField(max_length=30)
    SwitchID = models.CharField(max_length=30)
    State = models.BooleanField
    EventTime = models.DateTimeField

    def __str__(self):
        return self.title
