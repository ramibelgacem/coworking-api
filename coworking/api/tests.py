import datetime
import pytz
from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.models import EmployeeRole
from management.models import Company, Employee, Equipment


class CompanyTests(APITestCase):
    url_list = reverse('company-list')
    url_detail = 'company-detail'
    company_data = {'name': 'LtuTech'}

    def test_create(self):
        """
        Ensure we can create a new company object.
        """
        response = self.client.post(self.url_list, self.company_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, 'LtuTech')
        self.assertEqual(Company.objects.get().active, False)

    def test_toggle_company(self):
        """
        Ensure we can activate and desactivate a company.
        """
        Company.objects.create(**self.company_data)
        self.assertEqual(Company.objects.get().active, False)

        self.client.get(
            reverse('company-activate', args=(Company.objects.get().id,))
        )
        self.assertEqual(Company.objects.get().active, True)

        self.client.get(
            reverse('company-desactivate', args=(Company.objects.get().id,))
        )
        self.assertEqual(Company.objects.get().active, False)

    def test_list(self):
        """
        Ensure we can get companies.
        """
        Company.objects.create(**self.company_data)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_get_company_detail(self):
        """
        Ensure we can get a company details
        """
        company = Company.objects.create(**self.company_data)
        url = reverse(self.url_detail, args=(company.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['id'], str(company.id))
        self.assertEqual(data['name'], company.name)

    def test_delete_company(self):
        """
        Ensure we can delete a company
        """
        company = Company.objects.create(**self.company_data)
        url = reverse(self.url_detail, args=(company.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)


class EmployeeTests(APITestCase):
    company_data = {'name': 'LtuTech', 'active': True}
    employee_data = {
        "name": "Rami",
        "surname": "Belgacem",
        "active": False,
        "role": "intern",
    }

    def test_toggle_employee(self):
        """
        Ensure we can activate and desactivate an employee.
        """
        company = Company.objects.create(**self.company_data)
        self.employee_data.update({'company': company})
        Employee.objects.create(**self.employee_data)
        self.assertEqual(Employee.objects.get().active, False)

        self.client.get(
            reverse('employee-activate', args=(Employee.objects.get().id,))
        )
        self.assertEqual(Employee.objects.get().active, True)

        self.client.get(
            reverse('employee-desactivate', args=(Employee.objects.get().id,))
        )
        self.assertEqual(Employee.objects.get().active, False)


class EquipmentTests(APITestCase):
    company_data = {'name': 'LtuTech', 'active': True}
    employee_data1 = {
        "name": "Rami",
        "surname": "Belgacem",
        "active": True,
        "role": EmployeeRole.INTERN,
    }
    employee_data2 = {
        "name": "Philippe",
        "surname": "Richard",
        "active": True,
        "role": EmployeeRole.TECHLEAD,
    }
    employee_data3 = {
        "name": "Sarah",
        "surname": "Marcu",
        "active": True,
        "role": EmployeeRole.TECHLEAD,
    }
    equipment_data1 = {
        "equipment_type": "screen",
        "size": 24,
        "model": "ACER",
        "status": "free",
    }
    equipment_data2 = {
        "equipment_type": "pc",
        "memory": 32,
        "hard_disk_size": 512,
        "model": "HP",
        "status": "free",
    }

    def test_employee_equipment_assign(self):
        """
        Ensure we can assign an equipment to an employee
        """
        company = Company.objects.create(**self.company_data)
        self.employee_data1.update({'company': company})
        employee = Employee.objects.create(**self.employee_data1)
        equipment = Equipment.objects.create(**self.equipment_data1)
        self.assertEqual(equipment.employee, None)

        response = self.client.post(
            reverse('employee-equipment-assign', args=(equipment.id, employee.id))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        equipment = Equipment.objects.get(pk=equipment.id)
        self.assertEqual(equipment.employee, employee)

    def test_employee_equipment_revoke(self):
        """
        Ensure we can revoke an equipment from an employee
        """
        company = Company.objects.create(**self.company_data)
        self.employee_data1.update({'company': company})
        employee = Employee.objects.create(**self.employee_data1)
        equipment = Equipment.objects.create(**self.equipment_data1)
        self.assertEqual(equipment.employee, None)

        self.client.post(
            reverse('employee-equipment-assign', args=(equipment.id, employee.id))
        )

        response = self.client.post(
            reverse('employee-equipment-revoke', args=(equipment.id, employee.id))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        equipment = Equipment.objects.get(pk=equipment.id)
        self.assertEqual(equipment.employee, None)

    def test_employee_equipment_revoke_all(self):
        """
        Ensure we can revoke all employee's equipments
        """
        company = Company.objects.create(**self.company_data)
        self.employee_data1.update({'company': company})
        employee = Employee.objects.create(**self.employee_data1)
        equipment1 = Equipment.objects.create(**self.equipment_data1)
        equipment2 = Equipment.objects.create(**self.equipment_data2)
        self.assertEqual(employee.equipments.count(), 0)

        self.client.post(
            reverse('employee-equipment-assign', args=(equipment1.id, employee.id))
        )
        self.client.post(
            reverse('employee-equipment-assign', args=(equipment2.id, employee.id))
        )

        employee = Employee.objects.get(pk=employee.id)
        self.assertEqual(employee.equipments.count(), 2)

        response = self.client.post(
            reverse('employee-equipment-revoke-all', args=(employee.id,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee = Employee.objects.get(pk=employee.id)
        self.assertEqual(employee.equipments.count(), 0)

    def test_employee_equipment_list(self):
        """
        Ensure we can get all equipments of an employee
        """
        company = Company.objects.create(**self.company_data)
        self.employee_data1.update({'company': company})
        employee = Employee.objects.create(**self.employee_data1)
        equipment1 = Equipment.objects.create(**self.equipment_data1)
        equipment2 = Equipment.objects.create(**self.equipment_data2)

        self.client.post(
            reverse('employee-equipment-assign', args=(equipment1.id, employee.id))
        )
        self.client.post(
            reverse('employee-equipment-assign', args=(equipment2.id, employee.id))
        )

        response = self.client.get(
            reverse('employee-equipment-list', args=(employee.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_employees_lastyear(self):
        """
        Ensure we can get only employees of the last year
        """
        company = Company.objects.create(**self.company_data)
        self.employee_data2.update({'company': company})
        employee2 = Employee.objects.create(**self.employee_data2)

        mocked = datetime.datetime(2018, 1, 1, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            self.employee_data3.update({'company': company})
            employee3 = Employee.objects.create(**self.employee_data3)
            self.assertEqual(employee3.created_at, mocked)

        response = self.client.get(reverse('employee-last-year'))
        self.assertEqual(len(response.json()), 1)
        data = response.json()
        self.assertEqual(data[0]['name'], employee2.name)
        self.assertEqual(data[0]['surname'], employee2.surname)
