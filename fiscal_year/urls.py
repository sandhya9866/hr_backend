from django.urls import include, path
from .views import FiscalYearListView, FiscalYearCreateView, FiscalYearEditView, delete_fiscal_year

app_name = 'fiscal_year'


urlpatterns = [
    path('list/', FiscalYearListView.as_view(), name='list'),
    path('create/', FiscalYearCreateView.as_view(), name='create'),
    path('edit/<int:pk>', FiscalYearEditView.as_view(), name='edit'),
    path('delete/<int:pk>', delete_fiscal_year, name='delete'),
]