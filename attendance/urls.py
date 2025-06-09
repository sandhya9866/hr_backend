from django.urls import include, path
from .views import AttendanceRequestDeleteView, CalendarViewReport, CheckInView, CheckoutView, AttendanceRequestListView, AttendanceRequestCreateView, AttendanceRequestEditView, RequestUpdateStatusView

app_name = 'attendance'

urlpatterns = [
    path("checkin/", CheckInView.as_view(), name="checkin"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path('request/list/', AttendanceRequestListView.as_view(), name='request_list'),
    path('request/create/', AttendanceRequestCreateView.as_view(), name='request_create'),
    path('request/edit/<int:pk>', AttendanceRequestEditView.as_view(), name='request_edit'),
    path('request/delete/<int:pk>', AttendanceRequestDeleteView.as_view(), name='request_delete'),

    path('request/<int:pk>/update-status/', RequestUpdateStatusView.as_view(), name='request_update_status'),

    #Report
    path('calendar-view-report/', CalendarViewReport.as_view(), name='calendar_view_report'),
]