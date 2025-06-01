from django.urls import include, path
from .views import RosterListView, ShiftListView, ShiftCreateView, ShiftEditView, ShiftDeleteView, ajax_edit_shift, delete_shift_ajax, get_employees_by_department
from .views import add_shift_ajax

app_name = 'roster'


urlpatterns = [
    path('shift/list/', ShiftListView.as_view(), name='shift_list'),
    path('shift/create/', ShiftCreateView.as_view(), name='shift_create'),
    path('shift/edit/<int:pk>', ShiftEditView.as_view(), name='shift_edit'),
    path('shift/delete/<int:pk>', ShiftDeleteView.as_view(), name='shift_delete'),

    path('list/', RosterListView.as_view(), name='roster_list'),
    path('ajax/get-employees/', get_employees_by_department, name='ajax_get_employees'),
    path('add-shift/', add_shift_ajax, name='add_shift_ajax'),
    path('ajax/edit-shift/', ajax_edit_shift, name='ajax_edit_shift'),
    path('ajax/delete-shift/', delete_shift_ajax, name='delete_shift_ajax'),

]