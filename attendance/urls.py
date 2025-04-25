from django.urls import include, path
from attendance.views import checkin_view, checkout_view

app_name = 'attendance'

urlpatterns = [
    path("checkin/", checkin_view, name="checkin"),
    path("checkout/", checkout_view, name="checkout"),

]