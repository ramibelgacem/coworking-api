import uuid

from django.db import models

from base.models import (
    EmployeeRole,
    EquipmentStatus,
    TrackTimeModel,
    TypeOfEquipment
)
from base.validators import InternRuleValidator, DevRuleValidator, TechLeadRuleValidator


class Company(TrackTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Employee(TrackTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    role = models.CharField(choices=EmployeeRole.choices, max_length=100)
    company = models.ForeignKey('Company', on_delete=models.RESTRICT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname'], name='unique_booking'),
        ]

    def __str__(self):
        return self.name + ' ' + self.surname

    def revoke_all(self):
        self.equipments.update(status=EquipmentStatus.FREE, employee=None)


class Equipment(TrackTimeModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    equipment_type = models.CharField(choices=TypeOfEquipment.choices, max_length=6)
    memory = models.IntegerField(null=True)
    hard_disk_size = models.IntegerField(null=True)
    size = models.IntegerField(null=True)
    model = models.CharField(max_length=100)
    status = models.CharField(choices=EquipmentStatus.choices, max_length=100)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, related_name='equipments')

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_criteria_matches_equipment_type",
                check=(
                    models.Q(
                        equipment_type=TypeOfEquipment.PC,
                        memory__isnull=False,
                        hard_disk_size__isnull=False,
                        size__isnull=True,
                    )
                    | models.Q(
                        equipment_type=TypeOfEquipment.SCREEN,
                        memory__isnull=True,
                        hard_disk_size__isnull=True,
                        size__isnull=False,
                    )
                ),
            )
        ]

    def __str__(self):
        return self.equipment_type + ' ' + self.model

    def is_valid_assignment(self, employee):
        if employee.role == EmployeeRole.INTERN:
            if not InternRuleValidator(employee, self).is_valid():
                raise ValueError('An intern must have only one PC and one screen')
        if employee.role == EmployeeRole.DEV:
            if not DevRuleValidator(employee, self).is_valid():
                raise ValueError('A developer must have only one PC and two screens')
        if employee.role == EmployeeRole.TECHLEAD:
            if not TechLeadRuleValidator(employee, self).is_valid():
                raise ValueError('A tech lead must have a minimum 32go of memory or 512go of hard disk')

    def assign(self, employee):
        if self.status == EquipmentStatus.USED:
            raise ValueError('You can not assign this equipment, it is already used!')

        self.is_valid_assignment(employee)

        self.employee = employee
        self.status = EquipmentStatus.USED
        self.save()

    def revoke(self):
        self.employee = None
        self.status = EquipmentStatus.FREE
        self.save()
