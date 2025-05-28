from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from .models import Shift
from .forms import ShiftForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages

class ShiftListView(ListView):
    model = Shift
    template_name = 'roster/shift/list.html'
    context_object_name = 'shifts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Shift.objects.all().order_by('-id')
        
        # Get filter parameters from either POST or GET
        request_data = self.request.POST if self.request.method == 'POST' else self.request.GET
        
        title = request_data.get('title')

        # Apply filters
        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get list of titles for the select dropdown
        context['titles'] = Shift.objects.values_list('title', flat=True).distinct().order_by('title')
        
        # Add current filter values to context from either POST or GET
        request_data = self.request.POST if self.request.method == 'POST' else self.request.GET
        context['current_title'] = request_data.get('title', '')
        
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
    

class ShiftCreateView(LoginRequiredMixin, CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'roster/shift/create.html'
    success_url = reverse_lazy('roster:shift_list')

    def form_valid(self, form):
        shift = form.save(commit=False)
        shift.created_by = self.request.user
        shift.save()
        messages.success(self.request, "Shift created successfully.")
        return redirect(self.success_url)


class ShiftEditView(LoginRequiredMixin, UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'roster/shift/edit.html'
    success_url = reverse_lazy('roster:shift_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Shift updated successfully.")
        return redirect(self.success_url)

class ShiftDeleteView(View):
    model = Shift
    success_url = reverse_lazy('roster:shift_list')
    
    def get_object(self, queryset=None):
        return get_object_or_404(Shift, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Shift deleted successfully.")
        return redirect(self.success_url)