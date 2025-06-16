from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Branch
from .forms import BranchForm

# Create your views here.

class BranchListView(LoginRequiredMixin, ListView):
    model = Branch
    template_name = 'branch/branch_list.html'
    context_object_name = 'branches'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.GET.get('reset'):
            request.session.pop('branch_name', None)
            request.session.pop('branch_code', None)
            return redirect('branch:branch_list')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Branch.objects.all()
        name = self.request.session.get('branch_name', '')
        code = self.request.session.get('branch_code', '')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__icontains=code)
        
        return queryset.order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_branches'] = Branch.objects.all().order_by('name')
        context['name'] = self.request.session.get('branch_name', '')
        context['code'] = self.request.session.get('branch_code', '')
        return context

    def post(self, request, *args, **kwargs):
        request.session['branch_name'] = request.POST.get('name', '')
        request.session['branch_code'] = request.POST.get('code', '')
        return self.get(request, *args, **kwargs)

class BranchCreateView(LoginRequiredMixin, CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branch/branch_create.html'
    success_url = reverse_lazy('branch:branch_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Branch created successfully!')
        return super().form_valid(form)

class BranchUpdateView(LoginRequiredMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'branch/branch_create.html'
    success_url = reverse_lazy('branch:branch_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Branch updated successfully!')
        return response

class BranchDeleteView(LoginRequiredMixin, DeleteView):
    model = Branch
    success_url = reverse_lazy('branch:branch_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Branch, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Branch deleted successfully.")
        return redirect(self.success_url)
