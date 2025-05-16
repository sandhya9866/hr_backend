from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from user.models import Profile
from utils.common import point_down_round
from utils.enums import MARITAL_STATUS
from utils.date_converter import nepali_str_to_english
# from utils.date_converter import nepali_str_to_english 
from .models import EmployeeLeave, Leave, LeaveType
from .forms import LeaveForm, LeaveTypeForm

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q
from fiscal_year.models import FiscalYear

from decimal import Decimal, ROUND_DOWN


class LeaveTypeListView(ListView):
    # num = 20
    # out = (20/12)*1
    value = Decimal(1 * (20 / 12)).quantize(Decimal('0.1'), rounding=ROUND_DOWN)
    leave_no = float(value)
    print(leave_no)
    model = LeaveType  
    template_name = 'leave/leave_type/list.html'
    context_object_name = 'leave_types'
    paginate_by = 20

    def get_queryset(self):
        queryset = LeaveType.objects.all().order_by('-id')

        name = self.request.GET.get('name')
        total_days = self.request.GET.get('total_days')
        fiscal_year = self.request.GET.get('fiscal_year')
        marital_status = self.request.GET.get('marital_status')

        if name:
            queryset = queryset.filter(name=name)
        if total_days:
            queryset = queryset.filter(number_of_days=total_days)
        if fiscal_year:
            queryset = queryset.filter(fiscal_year_id=fiscal_year)
        if marital_status:
            queryset = queryset.filter(marital_status=marital_status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Remove "All" from marital status choices
        marital_status_choices = [choice for choice in MARITAL_STATUS if choice[0] != 'A']

        context.update({
            'name': self.request.GET.get('name', ''),
            'total_days': self.request.GET.get('total_days', ''),
            'fiscal_year': self.request.GET.get('fiscal_year', ''),
            'marital_status': self.request.GET.get('marital_status', ''),
            'fiscal_years': FiscalYear.objects.filter(status='active'),
            'marital_status_choices': marital_status_choices,
        })
        return context

class LeaveTypeCreateView(LoginRequiredMixin, CreateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'leave/leave_type/create.html'
    success_url = reverse_lazy('leave:leave_type_list')

    def form_valid(self, form):
        leave_type = form.save(commit=False)
        leave_type.created_by = self.request.user
        leave_type.save()
        if leave_type.status == 'active':
            updateLeaveTypeDetails(leave_type)

        
        messages.success(self.request, "Leave Type created successfully.")
        return redirect(self.success_url)


class LeaveTypeEditView(LoginRequiredMixin, UpdateView):
    model = LeaveType
    form_class = LeaveTypeForm
    template_name = 'leave/leave_type/edit.html'
    success_url = reverse_lazy('leave:leave_type_list')

    def form_valid(self, form):
        leave_type = form.save(commit=False)
        leave_type.updated_by = self.request.user

        leave_type.save()
        messages.success(self.request, "Leave Type updated successfully.")
        return redirect(self.success_url)


def delete_leave_type(request, pk):
    leave_type = get_object_or_404(LeaveType, pk=pk)
    leave_type.delete()
    messages.success(request, "Leave Type deleted successfully.")
    return redirect('leave:leave_type_list')

#assign leave to employee
def updateLeaveTypeDetails(leave_type):
    fiscal_year = leave_type.fiscal_year
    
    eng_fiscal_year_start_date = nepali_str_to_english(fiscal_year.start_date.strftime('%Y-%m-%d'))
    eng_fiscal_year_end_date = nepali_str_to_english(fiscal_year.end_date.strftime('%Y-%m-%d'))

    total_days = leave_type.number_of_days
    gender = None if leave_type.gender == 'A' else leave_type.gender
    marital_status = None if leave_type.marital_status == 'A' else leave_type.marital_status
    job_type = None if leave_type.job_type == 'all' else leave_type.job_type

    filters = {
        'user__is_active': True,
    }
    if gender:
        filters['gender'] = gender

    if marital_status:
        filters['marital_status'] = marital_status

    if job_type:
        filters['job_type'] = job_type

    employee_list = Profile.objects.filter(**filters).values_list('user', flat=True)

    if employee_list:
        for emp in employee_list:
            joining_date = Profile.objects.filter(user=emp).values_list('joining_date', flat=True).first()
            eng_join_date = nepali_str_to_english(joining_date.strftime('%Y-%m-%d'))
            if eng_join_date <= eng_fiscal_year_start_date:
                leave, created = EmployeeLeave.objects.get_or_create(
                    employee_id=emp,
                    leave_type=leave_type,
                    defaults={
                        'total_leave': total_days,
                        'leave_taken': 0,
                        'leave_remaining': total_days,
                        'created_by': leave_type.created_by,
                    }
                )
                # if not created:
                #     leave.total_leave += total_days
                #     leave.leave_remaining += total_days
                #     leave.save()
            else:
                month_diff = (eng_fiscal_year_end_date - eng_join_date).days // 30
                if month_diff > 0:
                    raw_leave = round(month_diff * (total_days / 12), 1)
                    no_of_leave = point_down_round(raw_leave)
                    leave, created = EmployeeLeave.objects.get_or_create(
                        employee_id=emp,
                        leave_type=leave_type,
                        defaults={
                            'total_leave': no_of_leave,
                            'leave_taken': 0,
                            'leave_remaining': no_of_leave,
                            'created_by': leave_type.created_by,
                        }
                    )


                


# Leave
class LeaveListView(ListView):
    model = Leave  
    template_name = 'leave/leave/list.html'
    context_object_name = 'leaves'
    paginate_by = 10

    def get_queryset(self):
        queryset = Leave.objects.all().order_by('-id')
        leave_type = self.request.GET.get('leave_type')

        if leave_type:
            queryset = queryset.filter(leave_type_id=leave_type)
        

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Remove "All" from marital status choices
        # marital_status_choices = [choice for choice in MARITAL_STATUS if choice[0] != 'A']

        context.update({
            'leave_type': self.request.GET.get('leave_type', ''),
            'leave_types': LeaveType.objects.all(),
        })
        return context

class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leave/leave/create.html'
    success_url = reverse_lazy('leave:leave_list')

    def form_valid(self, form):
        leave = form.save(commit=False)
        leave.employee_id = self.request.user.id
        leave.created_by = self.request.user

        start_date_nep = self.request.POST.get('start_date')
        start_date_eng = nepali_str_to_english(start_date_nep)

        end_date_nep = self.request.POST.get('end_date')
        end_date_eng = nepali_str_to_english(end_date_nep)

        leave.no_of_days = (end_date_eng - start_date_eng).days + 1

        leave.save()
        messages.success(self.request, "Leave  created successfully.")
        return redirect(self.success_url)


class LeaveEditView(LoginRequiredMixin, UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leave/leave/edit.html'
    success_url = reverse_lazy('leave:leave_list')

    def form_valid(self, form):
        leave = form.save(commit=False)
        leave.updated_by = self.request.user

        start_date_nep = self.request.POST.get('start_date')
        start_date_eng = nepali_str_to_english(start_date_nep)

        end_date_nep = self.request.POST.get('end_date')
        end_date_eng = nepali_str_to_english(end_date_nep)

        leave.no_of_days = (end_date_eng - start_date_eng).days + 1

        leave.save()
        messages.success(self.request, "Leave  updated successfully.")
        return redirect(self.success_url)


# 🔹 Delete View (Function-Based)
def delete_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    leave.delete()
    messages.success(request, "Leave deleted successfully.")
    return redirect('leave:leave_list')



    


