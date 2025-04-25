from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Profile
from .forms import ProfileForm, UserForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class EmployeeListView(ListView):
    model = Profile  
    template_name = 'user/employee/list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Profile.objects.all()
    

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
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        user_form = UserForm(instance=profile.user)
        profile_form = ProfileForm(instance=profile)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        user_form = UserForm(request.POST, instance=profile.user)
        profile_form = ProfileForm(request.POST, instance=profile)

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
    profile = get_object_or_404(Profile, pk=pk)
    print(profile)
    
    # Optionally, you can also delete the user associated
    user = profile.user

    # Delete profile first, then user (to respect foreign key constraints)
    profile.delete()
    user.delete()

    messages.success(request, "Employee deleted successfully.")
    return redirect('user:employee_list')