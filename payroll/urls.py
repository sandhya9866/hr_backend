from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('salary-type/list/', views.SalaryTypeListView.as_view(), name='salary_type_list'),
    path('salary-type/create/', views.SalaryTypeCreateView.as_view(), name='salary_type_create'),
    path('salary-type/edit/<int:pk>/', views.SalaryTypeUpdateView.as_view(), name='salary_type_edit'),
    path('salary-type/delete/<int:pk>/', views.SalaryTypeDeleteView.as_view(), name='salary_type_delete'),

    path('salary-release/list/', views.SalaryReleaseListView.as_view(), name='salary_release_list'),
    path('salary-release/create/', views.SalaryReleaseCreateView.as_view(), name='salary_release_create'),
    path('salary-release/edit/<int:pk>/', views.SalaryReleaseUpdateView.as_view(), name='salary_release_edit'),
    path('salary-release/delete/<int:pk>/', views.SalaryReleaseDeleteView.as_view(), name='salary_release_delete'),
] 