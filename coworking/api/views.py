from datetime import date
from datetime import datetime

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dateutil.relativedelta import relativedelta

from base.generics import ActivateAPIView, DesactivateAPIView
from base.models import EmployeeRole
from management.models import Company, Employee, Equipment
from api.serializers import (
    CompanySerializer,
    CompanyActiveSerializer,
    EmployeeSerializer,
    EmployeeActiveSerializer,
    EquipmentSerializer
)


class CompanyActivate(ActivateAPIView):
    """
    Activate a company APIView
    """

    queryset = Company.objects.all()
    serializer_class = CompanyActiveSerializer


class CompanyDesactivate(DesactivateAPIView):
    """
    Desactivate a company APIView
    """

    queryset = Company.objects.all()
    serializer_class = CompanyActiveSerializer


class CompanyList(generics.ListCreateAPIView):
    """
    List all companies, or create a new one
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a company.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class EmployeeActivate(ActivateAPIView):
    """
    Activate a employee APIView
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeActiveSerializer


class EmployeeDesactivate(DesactivateAPIView):
    """
    Desactivate a employee APIView
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeActiveSerializer


class EmployeeList(generics.ListCreateAPIView):
    """
    List all Employees, or create a new one
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a employee.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for all equipment endpoints.
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


@api_view(['GET'])
def employee_equipment_list(request, employee_id):
    """
    List all employee's equipments
    """
    try:
        employee = Employee.objects.get(pk=employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    equipments = employee.equipments
    serializer = EquipmentSerializer(equipments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def assign_equipment(request, pk, employee_id):
    """
    Assign an equipment to an employee
    """
    try:
        equipment = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        employee = Employee.objects.get(pk=employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    equipment.assign(employee)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def revoke_equipment(request, pk, employee_id):
    """
    Revoke an equipment from an employee
    """
    try:
        equipment = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        employee = Employee.objects.get(pk=employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if equipment.employee != employee:
        return Response(
            data={'detail': 'The employee is not assigned to this equipment'},
            status=status.HTTP_400_BAD_REQUEST
        )

    equipment.revoke()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def revoke_all(request, employee_id):
    """
    Revoke all employee's equipment
    """
    try:
        employee = Employee.objects.get(pk=employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    employee.revoke_all()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def employees_lastyear(request):
    today = datetime.combine(date.today(), datetime.min.time())

    same_day_last_year = today - relativedelta(years=1)
    employees = Employee.objects.filter(
        role=EmployeeRole.TECHLEAD,
        created_at__gte=same_day_last_year,
    )

    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def employee_period(request, start_year, end_year):
    start_year = datetime(start_year, 1, 1)
    end_year = datetime(end_year, 12, 31)

    if start_year > end_year:
        raise ValueError('second path parameter must be greater than the first one')

    employees = Employee.objects.filter(
        role=EmployeeRole.INTERN,
        created_at__gte=start_year,
        created_at__lte=end_year,
    )

    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
