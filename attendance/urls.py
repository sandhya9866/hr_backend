from django.urls import include, path
from .views import checkin_view, checkout_view, AttendanceRequestListView, AttendanceRequestCreateView, AttendanceRequestEditView, delete_attendance_request, request_update_status

app_name = 'attendance'

urlpatterns = [
    path("checkin/", checkin_view, name="checkin"),
    path("checkout/", checkout_view, name="checkout"),

    path('request/list/', AttendanceRequestListView.as_view(), name='request_list'),
    path('request/create/', AttendanceRequestCreateView.as_view(), name='request_create'),
    path('request/edit/<int:pk>', AttendanceRequestEditView.as_view(), name='request_edit'),
    path('delete/<int:pk>', delete_attendance_request, name='request_delete'),

    path('request/<int:pk>/update-status/', request_update_status, name='request_update_status'),

]