from management.base_model import TypeOfEquipment


class RuleValidator:
    def __init__(self, employee, equipment):
        self.employee = employee
        self.equipment = equipment

    def is_valid(self):
        return NotImplementedError("Subclass must implement this method!")


class InternRuleValidator(RuleValidator):
    def is_valid(self):
        if  ((self.employee.equipments.filter(equipment_type=TypeOfEquipment.PC).count() < 1
                and self.equipment.equipment_type==TypeOfEquipment.PC) \
                or \
                (self.employee.equipments.filter(equipment_type=TypeOfEquipment.SCREEN).count() < 1
                and self.equipment.equipment_type==TypeOfEquipment.SCREEN)):
            return True
        return False


class DevRuleValidator(RuleValidator):
    def is_valid(self):
        if  ((self.employee.equipments.filter(equipment_type=TypeOfEquipment.PC).count() < 1
                and self.equipment.equipment_type==TypeOfEquipment.PC) \
                or \
                (self.employee.equipments.filter(equipment_type=TypeOfEquipment.SCREEN).count() < 2
                and self.equipment.equipment_type==TypeOfEquipment.SCREEN)):
            return True
        return False


class TechLeadRuleValidator(RuleValidator):
    def is_valid(self):
        if self.equipment.equipment_type==TypeOfEquipment.PC \
                and self.equipment.memory >= 32 \
                and self.equipment.hard_disk_size >= 512:
            return True
        return False
