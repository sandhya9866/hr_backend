from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

from payroll.forms import SalaryReleaseForm, SalaryTypeForm
from user.models import AuthUser

from .models import SalaryRelease, SalaryType


# Create your views here.
class SalaryTypeListView(LoginRequiredMixin, ListView):
    model = SalaryType
    template_name = 'payroll/salary_type_list.html'
    context_object_name = 'salary_types'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.GET.get('reset'):
            request.session.pop('salary_type_name', None)
            return redirect('payroll:salary_type_list')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = SalaryType.objects.all()
        name = self.request.session.get('salary_type_name', '')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset.order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_salary_types'] = SalaryType.objects.all().order_by('name')
        context['name'] = self.request.session.get('salary_type_name', '')
        return context

    def post(self, request, *args, **kwargs):
        request.session['salary_type_name'] = request.POST.get('name', '')
        return self.get(request, *args, **kwargs)

class SalaryTypeCreateView(LoginRequiredMixin, CreateView):
    model = SalaryType
    form_class = SalaryTypeForm
    template_name = 'payroll/salary_type_create.html'
    success_url = reverse_lazy('payroll:salary_type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        messages.success(self.request, 'Salary type created successfully!')
        return super().form_valid(form)

class SalaryTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = SalaryType
    form_class = SalaryTypeForm
    template_name = 'payroll/salary_type_create.html'
    success_url = reverse_lazy('payroll:salary_type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Salary type updated successfully!')
        return response

class SalaryTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = SalaryType
    success_url = reverse_lazy('payroll:salary_type_list')

    def get_object(self, queryset=None):
        return get_object_or_404(SalaryType, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Salary type deleted successfully.")
        return redirect(self.success_url)

#Salary Release
class SalaryReleaseListView(LoginRequiredMixin, ListView):
    model = SalaryRelease
    template_name = 'payroll/salary_release/list.html'
    context_object_name = 'salary_releases'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        if request.GET.get('reset'):
            request.session.pop('employee', None)
            return redirect('payroll:salary_release_list')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = SalaryRelease.objects.all()
        employee = self.request.session.get('employee', '')

        if employee.isdigit():
            queryset = queryset.filter(employee_id=int(employee))
        
        return queryset.order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_list'] = AuthUser.get_active_users()
        employee_id = self.request.session.get('employee', '')
        context['employee'] = int(employee_id) if employee_id.isdigit() else None
        return context

    def post(self, request, *args, **kwargs):
        request.session['employee'] = request.POST.get('employee', '')
        return self.get(request, *args, **kwargs)

class SalaryReleaseCreateView(LoginRequiredMixin, CreateView):
    model = SalaryRelease
    form_class = SalaryReleaseForm
    template_name = 'payroll/salary_release/create_edit.html'
    success_url = reverse_lazy('payroll:salary_release_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        messages.success(self.request, 'Salary release created successfully!')
        return super().form_valid(form)


class SalaryReleaseUpdateView(LoginRequiredMixin, UpdateView):
    model = SalaryRelease
    form_class = SalaryReleaseForm
    template_name = 'payroll/salary_release/create_edit.html'
    success_url = reverse_lazy('payroll:salary_release_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Salary release updated successfully!')
        return response

class SalaryReleaseDeleteView(LoginRequiredMixin, DeleteView):
    model = SalaryRelease
    success_url = reverse_lazy('payroll:salary_release_list')

    def get_object(self, queryset=None):
        return get_object_or_404(SalaryRelease, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Salary release deleted successfully.")
        return redirect(self.success_url)