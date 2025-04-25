from django.shortcuts import render
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from datetime import date
from attendance.models import Attendance

# Create your views here.
# @transaction.atomic
def checkin_view(request):
    # print(request)
    todays_attendance = request.user.attendance.filter(date=timezone.datetime.today())
    lat=request.POST.get('checkinlat')
    lon=request.POST.get('checkinlon')
    # if not lat:
    #     messages.error(request, "Please allow device location.")
    #     return redirect(reverse_lazy('dashboard'))
    
    if not todays_attendance.exists():
        attendance = Attendance.objects.create(employee=request.user)
        attendance.checkin_time = timezone.now().time()
        if lat and lon:
            attendance.checkin_location = {'type': 'Point', 'coordinates': [round(float(lon),6),round(float(lat),6)]}

        attendance.save()           

    messages.success(request, "CheckIn Successful")
    return redirect(reverse_lazy('dashboard'))

# @transaction.atomic
def checkout_view(request):
    # print(request)
    todays_attendance = request.user.attendance.filter(date=timezone.datetime.today())
    lat=request.POST.get('checkoutlat')
    lon=request.POST.get('checkoutlon')
    # if not lat:
    #     messages.error(request, "Please allow device location.")
    #     return redirect(reverse_lazy('dashboard'))

    attendance = todays_attendance.first()
    attendance.checkout_time = timezone.now().time()
    attendance.working_hours = (timezone.datetime.combine(date.today(), attendance.checkout_time) - timezone.datetime.combine(date.today(), attendance.checkin_time)).seconds / 3600
    if lat and lon:
        attendance.checkout_location = {'type': 'Point', 'coordinates': [float(lon),float(lat)]}
    # attendance.checkout_devices = request.user_agent
    attendance.save()
    messages.success(request, "Checkout Successful")
    return redirect(reverse_lazy('dashboard'))

    # if not todays_attendance.exists():
    #     attendance = Attendance.objects.create(employee=request.user)
    #     attendance.checkin_time = timezone.now().time()
    #     if lat and lon:
    #         attendance.checkin_location = {'type': 'Point', 'coordinates': [round(float(lon),6),round(float(lat),6)]}

    #     attendance.save()           

    # messages.success(request, "CheckIn Successful")
    # return redirect(reverse_lazy('dashboard'))
