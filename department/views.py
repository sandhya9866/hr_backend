from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Department
from user.models import AuthUser
from .forms import DepartmentForm

# Create your views here.

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'department/department_list.html'
    context_object_name = 'departments'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        if request.GET.get('reset'):
            request.session.pop('department_name', None)
            request.session.pop('department_head', None)
            return redirect('department:department_list')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Department.objects.all().prefetch_related('department_head')
        name = self.request.session.get('department_name', '')
        department_head = self.request.session.get('department_head', '')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if department_head:
            queryset = queryset.filter(department_head__id=department_head).distinct()
        
        return queryset.order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_departments'] = Department.objects.all().order_by('name')
        context['all_users'] = AuthUser.objects.filter(department_head__isnull=False).distinct().order_by('first_name')
        context['name'] = self.request.session.get('department_name', '')
        context['department_head'] = self.request.session.get('department_head', '')
        return context

    def post(self, request, *args, **kwargs):
        request.session['department_name'] = request.POST.get('name', '')
        request.session['department_head'] = request.POST.get('department_head', '')
        return self.get(request, *args, **kwargs)


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department/department_create.html'
    success_url = reverse_lazy('department:department_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Department created successfully!')
        return super().form_valid(form)

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department/department_create.html'
    success_url = reverse_lazy('department:department_list')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Department updated successfully!')
        return response

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    success_url = reverse_lazy('department:department_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Department, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Department deleted successfully.")
        return redirect(self.success_url)
