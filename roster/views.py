from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from department.models import Department
from user.models import AuthUser
from .models import Roster, Shift
from .forms import ShiftForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages

class ShiftListView(ListView):
    model = Shift
    template_name = 'roster/shift/list.html'
    context_object_name = 'shifts'
    paginate_by = 2

    def get_queryset(self):
        queryset = Shift.objects.all().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    

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
    
def get_week_days(selected_date):
    # Get ISO calendar details
    year, week, day = selected_date.isocalendar()
    week_days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

    # Determine the start of the week (Sunday)
    start_of_week = selected_date - timedelta(days=(day % 7))  # Align to Sunday

    # Generate all days of the week starting from Sunday
    week_info = [(start_of_week + timedelta(days=i), week_days[i]) for i in range(7)]
    return week_info

class RosterListView(ListView):
    model = Roster  
    template_name = 'roster/roster/list.html'
    context_object_name = 'rosters'
    # paginate_by = 20

    # def get_queryset(self):
    #     queryset = Roster.objects.all().order_by('-id')

    #     name = self.request.GET.get('name')
    #     total_days = self.request.GET.get('total_days')
    #     fiscal_year = self.request.GET.get('fiscal_year')
    #     marital_status = self.request.GET.get('marital_status')

    #     if name:
    #         queryset = queryset.filter(name=name)
    #     if total_days:
    #         queryset = queryset.filter(number_of_days=total_days)
    #     if fiscal_year:
    #         queryset = queryset.filter(fiscal_year_id=fiscal_year)
    #     if marital_status:
    #         queryset = queryset.filter(marital_status=marital_status)

    #     return queryset
    date=timezone.now()
    week_info = get_week_days(date)
    dates = week_info
    # print(dates)
    # breakpoint()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_departments'] = Department.objects.all().order_by('name')
        context['all_users'] = AuthUser.objects.filter(is_active=True).all().order_by('first_name')
        context['all_shifts'] = Shift.objects.all().order_by('title')
        # context['search_query'] = self.request.GET.get('q', '')

        context['days'] = self.dates
        return context
    
