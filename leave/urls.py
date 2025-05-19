from django.urls import include, path
from .views import LeaveTypeListView, LeaveTypeCreateView, LeaveTypeEditView, delete_leave_type, LeaveListView, LeaveCreateView, LeaveEditView, delete_leave, LeaveStatusUpdateView

app_name = 'leave'

urlpatterns = [
    #Leave
    path('list/', LeaveListView.as_view(), name='leave_list'),
    path('create/', LeaveCreateView.as_view(), name='leave_create'),
    path('edit/<int:pk>', LeaveEditView.as_view(), name='leave_edit'),
    path('delete/<int:pk>', delete_leave, name='leave_delete'),
    path('<int:pk>/update-status/', LeaveStatusUpdateView.as_view(), name='leave_update_status'),



    #Leave Type
    path('leave-type/list/', LeaveTypeListView.as_view(), name='leave_type_list'),
    path('leave-type/create/', LeaveTypeCreateView.as_view(), name='leave_type_create'),
    path('leave-type/edit/<int:pk>', LeaveTypeEditView.as_view(), name='leave_type_edit'),
    path('leave-type/delete/<int:pk>', delete_leave_type, name='leave_type_delete'),

]