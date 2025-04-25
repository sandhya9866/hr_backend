from django.shortcuts import render, get_object_or_404, redirect
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

    def get_queryset(self):
        return Shift.objects.all()
    

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


# 🔹 Delete View (Function-Based)
def delete_shift(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    shift.delete()
    messages.success(request, "Shift deleted successfully.")
    return redirect('roster:shift_list')