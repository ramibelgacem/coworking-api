from django.db import models


class TrackTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class TypeOfEquipment(models.TextChoices):
    PC = 'pc', 'PC'
    SCREEN = 'screen', 'Screen'


class EmployeeRole(models.TextChoices):
    INTERN = 'intern', 'Intern'
    DEV = 'dev', 'Dev'
    TECHLEAD = 'techlead', 'TechLead'
    IT = 'it', 'IT'
    CTO = 'cto', 'CTO'


class EquipmentStatus(models.TextChoices):
    FREE = 'free', 'Free'
    USED = 'used', 'Used'
