from django.urls import path
from . import views

app_name = 'department'

urlpatterns = [
    path('list/', views.DepartmentListView.as_view(), name='department_list'),
    path('create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('edit/<int:pk>/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('delete/<int:pk>/', views.DepartmentDeleteView.as_view(), name='department_delete'),
] 