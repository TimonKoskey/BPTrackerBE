from django.db import models
from authentication.models import (
    clients
)

class ClientDiary(models.Model):
    client_mood = models.CharField(max_length=50, blank=True, null=True)
    event_description = models.CharField(max_length=50, blank=True, null=True)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

class BloodPressureData(models.Model):
    client = models.ForeignKey(clients, null=True, blank=True, on_delete=models.CASCADE)
    average_SBP_per_upload = models.IntegerField(blank=True, null=True)
    average_DBP_per_upload = models.IntegerField(blank=True, null=True)
    average_pulse_rate_per_upload = models.IntegerField(blank=True, null=True)
    blood_pressure_status = models.CharField(max_length=50, blank=True, null=True)
    diary_input = models.OneToOneField(ClientDiary, null=True, blank=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "%s " %(self.client)

class BloodPressureInput(models.Model):
    systolic_blood_pressure = models.IntegerField(blank=True, null=True)
    diastolic_blood_pressure = models.IntegerField(blank=True, null=True)
    pulse_rate = models.IntegerField(blank=True, null=True)
    upload_count = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    average_of_inputs = models.ForeignKey(BloodPressureData, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s " %(self.average_of_inputs)


diary = ClientDiary
bpdata = BloodPressureData
bpinputs = BloodPressureInput