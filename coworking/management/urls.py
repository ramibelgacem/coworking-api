from django.urls import include, path
from rest_framework.routers import DefaultRouter

from management import views


router = DefaultRouter()
router.register(r'equipment', views.EquipmentViewSet, basename="equipment")

urlpatterns = [
    path('company/', views.CompanyList.as_view()),
    path('company/<uuid:pk>/', views.CompanyDetail.as_view()),
    path('employee/', views.EmployeeList.as_view()),
    path('employee/<uuid:pk>/', views.EmployeeDetail.as_view()),
    path('', include(router.urls)),
    path('equipment/<uuid:employee_id>/list/', views.employee_equipment_list, name='employee-equipment-list'),
    path('equipment/<uuid:pk>/<uuid:employee_id>/assign/', views.assign_equipment, name='employee-equipment-assign'),
    path('equipment/<uuid:pk>/<uuid:employee_id>/revoke/', views.revoke_equipment, name='employee-equipment-revoke'),
    path('equipment/<uuid:employee_id>/revoke-all/', views.revoke_all, name='employee-equipment-revoke-all'),
]
