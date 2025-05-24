from django.urls import include, path
from .views import ShiftListView, ShiftCreateView, ShiftEditView, ShiftDeleteView

app_name = 'roster'


urlpatterns = [
    path('list/', ShiftListView.as_view(), name='shift_list'),
    path('create/', ShiftCreateView.as_view(), name='shift_create'),
    path('edit/<int:pk>', ShiftEditView.as_view(), name='shift_edit'),
    path('delete/<int:pk>', ShiftDeleteView.as_view(), name='shift_delete'),
]