from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from .models import FiscalYear
from .forms import FiscalYearForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages

class FiscalYearListView(ListView):
    model = FiscalYear  
    template_name = 'fiscal_year/list.html'
    context_object_name = 'fiscal_years'

    def get_queryset(self):
        return FiscalYear.objects.all().order_by('-id')
    

class FiscalYearCreateView(LoginRequiredMixin, CreateView):
    model = FiscalYear
    form_class = FiscalYearForm
    template_name = 'fiscal_year/create.html'
    success_url = reverse_lazy('fiscal_year:list')

    def form_valid(self, form):
        fiscal_year = form.save(commit=False)
        fiscal_year.created_by = self.request.user
        fiscal_year.save()
        messages.success(self.request, "Fiscal Year created successfully.")
        return redirect(self.success_url)


class FiscalYearEditView(LoginRequiredMixin, UpdateView):
    model = FiscalYear
    form_class = FiscalYearForm
    template_name = 'fiscal_year/edit.html'
    success_url = reverse_lazy('fiscal_year:list')

    def form_valid(self, form):
        fiscal_year = form.save(commit=False)
        fiscal_year.updated_by = self.request.user
        fiscal_year.save()
        messages.success(self.request, "Fiscal Year updated successfully.")
        return redirect(self.success_url)

class FiscalYearDeleteView(View):
    model = FiscalYear
    success_url = reverse_lazy('fiscal_year:list')
    
    def get_object(self, queryset=None):
        return get_object_or_404(FiscalYear, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Fiscal Year deleted successfully.")
        return redirect(self.success_url)