from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register(r'', views.EquipmentViewSet, basename="equipment")

urlpatterns = [
    path('company/', views.CompanyList.as_view(), name='company-list'),
    path('company/<uuid:pk>/', views.CompanyDetail.as_view(), name='company-detail'),
    path('employee/', views.EmployeeList.as_view(), name='employee-list'),
    path('employee/<uuid:pk>/', views.EmployeeDetail.as_view(), name='employee-detail'),
    path('equipment/', include(router.urls)),
    path('equipment/<uuid:employee_id>/list/', views.employee_equipment_list, name='employee-equipment-list'),
    path('equipment/<uuid:pk>/<uuid:employee_id>/assign/', views.assign_equipment, name='employee-equipment-assign'),
    path('equipment/<uuid:pk>/<uuid:employee_id>/revoke/', views.revoke_equipment, name='employee-equipment-revoke'),
    path('equipment/<uuid:employee_id>/revoke-all/', views.revoke_all, name='employee-equipment-revoke-all'),
]
