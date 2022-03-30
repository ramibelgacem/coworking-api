from base.models import TypeOfEquipment


class RuleValidator:
    """
    Abstract class for all business rules
    """
    def __init__(self, employee, equipment):
        self.employee = employee
        self.equipment = equipment

    def is_valid(self):
        """
        Check if a rule is valid
        """
        return NotImplementedError("Subclass must implement this method!")


class InternRuleValidator(RuleValidator):
    """
    Rule validator for Intern employees
    """
    def is_valid(self):
        """
        An Intern can have only 1 pc and 1 screen
        """
        if ((self.employee.equipments.filter(equipment_type=TypeOfEquipment.PC).count() < 1
                and self.equipment.equipment_type == TypeOfEquipment.PC)
                or
                (self.employee.equipments.filter(equipment_type=TypeOfEquipment.SCREEN).count() < 1
                 and self.equipment.equipment_type == TypeOfEquipment.SCREEN)):
            return True
        return False


class DevRuleValidator(RuleValidator):
    """
    Rule validator for developers employees
    """
    def is_valid(self):
        """
        A developer can have only  1 pc and no more than 2 screens.
        """
        if ((self.employee.equipments.filter(equipment_type=TypeOfEquipment.PC).count() < 1
                and self.equipment.equipment_type == TypeOfEquipment.PC)
                or
                (self.employee.equipments.filter(equipment_type=TypeOfEquipment.SCREEN).count() < 2
                 and self.equipment.equipment_type == TypeOfEquipment.SCREEN)):
            return True
        return False


class TechLeadRuleValidator(RuleValidator):
    """
    Rule validator for tech lead employees
    """
    def is_valid(self):
        """
        A Tech Lead pc must have minimum 32gb of memory and 512 hard disk.
        """
        if self.equipment.equipment_type == TypeOfEquipment.PC \
                and self.equipment.memory >= 32 \
                and self.equipment.hard_disk_size >= 512:
            return True
        return False
