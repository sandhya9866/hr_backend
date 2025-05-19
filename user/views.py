from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import AuthUser, Profile
from .forms import ProfileForm, UserForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class EmployeeListView(ListView):
    model = AuthUser  
    template_name = 'user/employee/list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return AuthUser.objects.filter(is_active=True).select_related('profile').order_by('-id')
    

class EmployeeCreateView(CreateView):
    template_name = 'user/employee/create.html'
    success_url = reverse_lazy('user:employee_list')

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password('deli@gbl2079')
            user.save()

            # Then save the profile form, but don't commit yet
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect(self.success_url)

        # If forms are not valid, re-render with errors
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })


class EmployeeEditView(UpdateView):
    template_name = 'user/employee/edit.html'
    success_url = reverse_lazy('user:employee_list')

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(AuthUser, pk=kwargs['pk'])
        # Get or create profile if missing
        profile, _ = Profile.objects.get_or_create(user=user)

        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(AuthUser, pk=kwargs['pk'])
        profile, _ = Profile.objects.get_or_create(user=user)

        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

def delete_employee(request, pk):
    user = get_object_or_404(AuthUser, pk=pk)
    # Delete profile first if it exists
    if hasattr(user, 'profile'):
        user.profile.delete()
        
    user.delete()

    messages.success(request, "Employee deleted successfully.")
    return redirect('user:employee_list')