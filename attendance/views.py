from django.shortcuts import render
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from datetime import date,datetime
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Request, RequestStatus, RequestType, Attendance
from .forms import RequestForm

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone

def checkin_view(request):
    today = timezone.localdate()
    if request.user.attendance.filter(date=today).exists():
        messages.info(request, "You have already checked in today.")
        return redirect(reverse_lazy('dashboard'))

    lat = request.POST.get('checkinlat')
    lon = request.POST.get('checkinlon')

    now = timezone.now()
    attendance = Attendance.objects.create(employee=request.user)
    attendance.actual_checkin_time = now.time()
    attendance.checkin_time = now.time()

    # Apply late arrival request time if approved
    approved_late_request = Request.objects.filter(
        employee=request.user,
        date=today,
        type=RequestType.LATE_ARRIVAL_REQUEST,
        status=RequestStatus.APPROVED
    ).first()
    if approved_late_request:
        attendance.checkin_time = approved_late_request.time

    # Respect shift start time if earlier than check-in
    employee_shift = getattr(request.user.profile, 'shift', None)
    if employee_shift and attendance.checkin_time < employee_shift.start_time:
        attendance.checkin_time = employee_shift.start_time

    # Set location if available and valid
    try:
        if lat and lon:
            attendance.checkin_location = {
                'type': 'Point',
                'coordinates': [round(float(lon), 6), round(float(lat), 6)]
            }
    except (ValueError, TypeError):
        messages.warning(request, "Invalid location data received.")

    attendance.save()

    messages.success(request, "Check-In Successful")
    return redirect(reverse_lazy('dashboard'))


def checkout_view(request):
    today = timezone.localdate()
    attendance = request.user.attendance.filter(date=today).first()

    if not attendance:
        messages.error(request, "No check-in record found for today.")
        return redirect(reverse_lazy('dashboard'))

    lat = request.POST.get('checkoutlat')
    lon = request.POST.get('checkoutlon')

    now = timezone.now()
    attendance.actual_checkout_time = now.time()
    attendance.checkout_time = now.time()

    # Apply approved early departure request
    approved_request = Request.objects.filter(
        employee=request.user,
        date=today,
        type=RequestType.EARLY_DEPARTURE_REQUEST,
        status=RequestStatus.APPROVED
    ).first()
    if approved_request:
        attendance.checkout_time = approved_request.time

    # Clamp checkout time to shift end time
    employee_shift = getattr(request.user.profile, 'shift', None)
    if employee_shift and attendance.checkout_time > employee_shift.end_time:
        attendance.checkout_time = employee_shift.end_time

    # Calculate working hours
    if attendance.checkin_time and attendance.checkout_time:
        attendance.working_hours = calculate_working_hours(attendance.checkin_time, attendance.checkout_time)

    # Record checkout location if valid
    try:
        if lat and lon:
            attendance.checkout_location = {
                'type': 'Point',
                'coordinates': [round(float(lon), 6), round(float(lat), 6)]
            }
    except (ValueError, TypeError):
        messages.warning(request, "Invalid location data received.")

    attendance.save()

    messages.success(request, "Checkout Successful")
    return redirect(reverse_lazy('dashboard'))

# Attendance Request
class AttendanceRequestListView(ListView):
    model = Request  
    template_name = 'attendance/request/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return Request.objects.select_related('employee').all().order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_status_choices'] = RequestStatus.choices
        return context
    

class AttendanceRequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'attendance/request/request_create.html'
    success_url = reverse_lazy('attendance:request_list')

    def form_valid(self, form):
        attendance_request = form.save(commit=False)
        attendance_request.created_by = self.request.user
        attendance_request.employee_id = self.request.user.id
        attendance_request.save()
        messages.success(self.request, "Request created successfully.")
        return redirect(self.success_url)


class AttendanceRequestEditView(LoginRequiredMixin, UpdateView):
    model = Request
    form_class = RequestForm
    template_name = 'attendance/request/request_edit.html'
    success_url = reverse_lazy('attendance:request_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Request updated successfully.")
        return redirect(self.success_url)


# 🔹 Delete View (Function-Based)
def delete_attendance_request(request, pk):
    request = get_object_or_404(Request, pk=pk)
    request.delete()
    messages.success(request, "Request deleted successfully.")
    return redirect('attendance:request_list')

# def request_update_status(request, pk):
#     if request.method == 'POST':
#         req = get_object_or_404(Request, pk=pk)
#         new_status = request.POST.get('status')

#         if new_status and new_status in dict(RequestStatus.choices).keys():
#             req.status = new_status
#             req.save()
#             if(new_status == RequestStatus.APPROVED):
#                 attendance = Attendance.objects.filter(employee=req.employee, date=req.date).first()
#                 if req.type == RequestType.LATE_ARRIVAL_REQUEST:
#                     if attendance:
#                         if attendance.checkin_time:
#                             attendance.checkin_time = req.time
#                             if(attendance.checkout_time):
#                                 attendance.working_hours = calculate_working_hours(attendance.checkin_time, attendance.checkout_time)
#                             attendance.save()
#                 elif req.type == RequestType.EARLY_DEPARTURE_REQUEST:
#                     if attendance:
#                         if attendance.checkout_time:
#                             attendance.checkout_time = req.time
#                             if(attendance.checkin_time):
#                                 attendance.working_hours = calculate_working_hours(attendance.checkin_time, attendance.checkout_time)
#                             attendance.save()
#                 elif req.type == RequestType.MISSED_CHECKOUT:
#                     if attendance:
#                         attendance.checkout_time = req.time
#                         if(attendance.checkin_time):
#                             attendance.working_hours = calculate_working_hours(attendance.checkin_time, attendance.checkout_time)
#                         attendance.save()

#             messages.success(request, f'Status updated to {req.get_status_display()}.')
#         else:
#             messages.error(request, 'Invalid status selected.')

#     return redirect('attendance:request_list')

def request_update_status(request, pk):
    if request.method != 'POST':
        return redirect('attendance:request_list')

    req = get_object_or_404(Request, pk=pk)
    new_status = request.POST.get('status')

    valid_statuses = dict(RequestStatus.choices).keys()
    if not new_status or new_status not in valid_statuses:
        messages.error(request, 'Invalid status selected.')
        return redirect('attendance:request_list')

    req.status = new_status
    req.save()

    if new_status == RequestStatus.APPROVED:
        update_attendance_for_request(req)

    messages.success(request, f'Status updated to {req.get_status_display()}.')
    return redirect('attendance:request_list')


def update_attendance_for_request(req):
    attendance = Attendance.objects.filter(employee=req.employee, date=req.date).first()
    if not attendance:
        return

    updated = False

    if req.type == RequestType.LATE_ARRIVAL_REQUEST and attendance.checkin_time:
        attendance.checkin_time = req.time
        updated = True

    elif req.type == RequestType.EARLY_DEPARTURE_REQUEST and attendance.checkout_time:
        attendance.checkout_time = req.time
        updated = True

    elif req.type == RequestType.MISSED_CHECKOUT:
        attendance.checkout_time = req.time
        updated = True

    if updated and attendance.checkin_time and attendance.checkout_time:
        attendance.working_hours = calculate_working_hours(attendance.checkin_time, attendance.checkout_time)

    if updated:
        attendance.save()

def calculate_working_hours(checkin_time, checkout_time):
    if checkin_time and checkout_time:
        start = datetime.combine(date.today(), checkin_time)
        end = datetime.combine(date.today(), checkout_time)
        return (end - start).total_seconds() / 3600
    return 0