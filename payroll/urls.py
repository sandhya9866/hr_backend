from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('salary-type/list/', views.SalaryTypeListView.as_view(), name='salary_type_list'),
    path('salary-type/create/', views.SalaryTypeCreateView.as_view(), name='salary_type_create'),
    path('salary-type/edit/<int:pk>/', views.SalaryTypeUpdateView.as_view(), name='salary_type_edit'),
    path('salary-type/delete/<int:pk>/', views.SalaryTypeDeleteView.as_view(), name='salary_type_delete'),
] 