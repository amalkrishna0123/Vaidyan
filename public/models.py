from django.db import models

class Appointment(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    request = models.TextField(blank=True, null=True)
    sent_date  = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now=False, null=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]
    
