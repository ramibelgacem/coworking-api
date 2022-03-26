from django.db import models

from management.base_model import TrackTimeModel


EMPLOYEE_ROLE = [
    ('intern', 'Intern'),
    ('dev', 'Dev'),
    ('techlead', 'TechLead'),
    ('it', 'IT'),
    ('cto', 'CTO'),
]

EQUIPMENTS_STATUS = [
    ('free', 'Free'),
    ('Used', 'Used'),
]

EQUIPMENTS_TYPE = [
    ('pc', 'PC'),
    ('screen', 'Screen'),
]

class Company(TrackTimeModel):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Employee(TrackTimeModel):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    role = models.CharField(choices=EMPLOYEE_ROLE, max_length=100)
    company = models.ForeignKey('Company', on_delete=models.RESTRICT)

class Equipment(TrackTimeModel):
    equipment_type = models.CharField(choices=EQUIPMENTS_TYPE, max_length=100)
    memory = models.IntegerField(null=True)
    hard_disk_size = models.IntegerField(null=True)
    size = models.IntegerField(null=True)
    model = models.CharField(max_length=100)
    status = models.CharField(choices=EQUIPMENTS_STATUS, max_length=100)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
