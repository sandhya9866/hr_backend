from django.urls import include, path
from .views import EmployeeListView, EmployeeCreateView, EmployeeEditView, EmployeeDeleteView

app_name = 'user'


urlpatterns = [
    path('list/', EmployeeListView.as_view(), name='employee_list'),
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('edit/<int:pk>', EmployeeEditView.as_view(), name='employee_edit'),
    path('delete/<int:pk>', EmployeeDeleteView.as_view(), name='employee_delete'),
]