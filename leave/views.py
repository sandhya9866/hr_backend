from urllib.request import Request
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from user.models import AuthUser, Profile
from utils.common import point_down_round
from utils.enums import MARITAL_STATUS
from utils.date_converter import nepali_str_to_english
# from utils.date_converter import nepali_str_to_english 
from .models import EmployeeLeave, Leave, LeaveType
from .forms import LeaveForm, LeaveTypeForm

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Q, F, Case, When, Value, IntegerField
from fiscal_year.models import FiscalYear

from decimal import Decimal, ROUND_DOWN


class LeaveTypeListView(ListView):
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

class LeaveTypeDeleteView(View):
    model = LeaveType
    success_url = reverse_lazy('leave:leave_type_list')
    
    def get_object(self, queryset=None):
        return get_object_or_404(LeaveType, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Leave Type deleted successfully.")
        return redirect(self.success_url)

#assign leaves to employees
def updateLeaveTypeDetails(leave_type):
    fiscal_year = leave_type.fiscal_year
    
    eng_fiscal_year_start_date = nepali_str_to_english(fiscal_year.start_date.strftime('%Y-%m-%d'))
    eng_fiscal_year_end_date = nepali_str_to_english(fiscal_year.end_date.strftime('%Y-%m-%d'))

    total_days = leave_type.number_of_days
    gender = None if leave_type.gender == 'A' else leave_type.gender
    marital_status = None if leave_type.marital_status == 'A' else leave_type.marital_status
    job_type = None if leave_type.job_type == 'all' else leave_type.job_type

    user_filters = {
        'is_active': True,
    }

    if gender:
        user_filters['profile__gender'] = gender

    if marital_status:
        user_filters['profile__marital_status'] = marital_status

    if job_type:
        user_filters['profile__job_type'] = job_type

    employee_list = AuthUser.objects.filter(**user_filters).select_related('profile')
    
    if employee_list:
        for emp in employee_list:
            try:
                profile = emp.profile
            except Profile.DoesNotExist:
                continue  # Skip users without a profile

            joining_date = profile.joining_date
            if not joining_date:
                continue  # Skip if joining date is missing

            eng_join_date = nepali_str_to_english(joining_date.strftime('%Y-%m-%d'))

            if eng_join_date <= eng_fiscal_year_start_date:
                leave, created = EmployeeLeave.objects.get_or_create(
                    employee=emp,
                    leave_type=leave_type,
                    defaults={
                        'total_leave': total_days,
                        'leave_taken': 0,
                        'leave_remaining': total_days,
                        'created_by': leave_type.created_by,
                    }
                )
            else:
                month_diff = (eng_fiscal_year_end_date - eng_join_date).days // 30
                if month_diff > 0:
                    raw_leave = round(month_diff * (total_days / 12), 1)
                    no_of_leave = point_down_round(raw_leave)
                    leave, created = EmployeeLeave.objects.get_or_create(
                        employee=emp,
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
            'leave_status_choices': Leave.LEAVE_STATUS,
        })
        return context
    
class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leave/leave/create.html'
    success_url = reverse_lazy('leave:leave_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['remaining_leaves'] = EmployeeLeave.objects.filter(
            employee=self.request.user,
            leave_type__fiscal_year__is_current=True
        ).select_related('leave_type')  # Optimizes DB queries
        return context



class LeaveEditView(LoginRequiredMixin, UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leave/leave/edit.html'
    success_url = reverse_lazy('leave:leave_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['remaining_leaves'] = EmployeeLeave.objects.filter(
            employee=self.request.user,
            leave_type__fiscal_year__is_current=True
        ).select_related('leave_type')
        return context

class LeaveDeleteView(View):
    model = Leave
    success_url = reverse_lazy('leave:leave_list')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Leave, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Leave deleted successfully.")
        return redirect(self.success_url)

class LeaveStatusUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        leave = get_object_or_404(Leave, pk=pk)
        new_status = request.POST.get('status')

        valid_statuses = dict(Leave.LEAVE_STATUS)
        if new_status not in valid_statuses:
            messages.error(request, "Invalid status selected.")
            return redirect('leave:leave_list')
        
        #update leave taken and remaining
        if new_status == 'Approved':
            update_employee_leaves(leave)

        # if new_status == 'Declined':
        #     EmployeeLeave.objects.filter(
        #         employee=leave.employee,
        #         leave_type=leave.leave_type
        #     ).update(
        #         leave_taken=Case(
        #             When(leave_taken__gte=leave.no_of_days,
        #                     then=F('leave_taken') - leave.no_of_days),
        #             default=Value(0),
        #             output_field=IntegerField()
        #         ),
        #         leave_remaining=F('leave_remaining') + leave.no_of_days
        #     )

        leave.status = new_status
        leave.save()
        messages.success(request, f'Leave status updated to {leave.get_status_display()}.')
        return redirect('leave:leave_list')
    
def update_employee_leaves(leave):
    leave_type = leave.leave_type
    employee = leave.employee

    employee_leave = EmployeeLeave.objects.filter(
        employee=employee,
        leave_type=leave_type
    ).first()
    employee_leave.leave_taken += leave.no_of_days
    employee_leave.leave_remaining -= leave.no_of_days
    employee_leave.save()



    


