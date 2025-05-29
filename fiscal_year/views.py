from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from .models import FiscalYear
from .forms import FiscalYearForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages
from django.db.models import Q

from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import FiscalYear

@method_decorator(csrf_protect, name='dispatch')
class FiscalYearListView(ListView):
    model = FiscalYear  
    template_name = 'fiscal_year/list.html'
    context_object_name = 'fiscal_years'
    paginate_by = 10 

    def get_queryset(self):
        queryset = FiscalYear.objects.all()

        # Use POST data if available
        data = self.request.POST if self.request.method == "POST" else {}

        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        return queryset.order_by('-id')

    def post(self, request, *args, **kwargs):
        # Reuse get method to render template with filtered data
        return self.get(request, *args, **kwargs)

    

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