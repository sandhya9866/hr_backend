from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import AuthUser, Profile, WorkingDetail
from .forms import ProfileForm, UserForm, WorkingDetailForm
from django.urls import reverse_lazy
from django.contrib import messages

class EmployeeListView(ListView):
    model = AuthUser  
    template_name = 'user/employee/list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return AuthUser.objects.filter(is_active=True).select_related('profile').order_by('-id')
    

# class EmployeeCreateView(CreateView):
#     template_name = 'user/employee/create.html'
#     success_url = reverse_lazy('user:employee_list')

#     def get(self, request, *args, **kwargs):
#         user_form = UserForm()
#         profile_form = ProfileForm()
#         return render(request, self.template_name, {
#             'user_form': user_form,
#             'profile_form': profile_form
#         })

#     def post(self, request, *args, **kwargs):
#         user_form = UserForm(request.POST)
#         profile_form = ProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password('deli@gbl2079')
#             user.save()

#             # Then save the profile form, but don't commit yet
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()

#             return redirect(self.success_url)

#         # If forms are not valid, re-render with errors
#         return render(request, self.template_name, {
#             'user_form': user_form,
#             'profile_form': profile_form
#         })

class EmployeeCreateView(View):
    template_name = 'user/employee/create.html'
    success_url = reverse_lazy('user:employee_list')

    def get(self, request):
        context = {
            'user_form': UserForm(prefix='user'),
            'profile_form': ProfileForm(prefix='profile'),
            'working_form': WorkingDetailForm(prefix='work'),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        section = request.POST.get('form_section')

        context = {
            'user_form': UserForm(request.POST, prefix='user') if section == 'profile' else UserForm(prefix='user'),
            'profile_form': ProfileForm(request.POST, prefix='profile') if section == 'profile' else ProfileForm(prefix='profile'),
            'working_form': WorkingDetailForm(request.POST, prefix='work') if section == 'work' else WorkingDetailForm(prefix='work'),
        }

        if section == 'profile':
            user_form = context['user_form']
            profile_form = context['profile_form']

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password('deli@gbl2079')
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                request.session['new_user_id'] = user.id
                messages.success(request, "Profile details saved successfully.")
                return redirect('user:employee_create')

        elif section == 'work':
            working_form = context['working_form']
            if working_form.is_valid():
                user_id = request.session.get('new_user_id')
                if user_id:
                    user = AuthUser.objects.get(pk=user_id)
                    working = working_form.save(commit=False)
                    working.employee = user
                    working.save()
                    messages.success(request, "Work details saved successfully.")
                    return redirect('user:employee_create')
                else:
                    messages.error(request, "No user found for associating work details.")

        return render(request, self.template_name, context)


class EmployeeEditView(UpdateView):
    template_name = 'user/employee/edit.html'
    success_url = reverse_lazy('user:employee_list')

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(AuthUser, pk=kwargs['pk'])
        profile, _ = Profile.objects.get_or_create(user=user)
        working_detail, _ = WorkingDetail.objects.get_or_create(employee=user)

        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        working_form = WorkingDetailForm(instance=working_detail)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'working_form': working_form
        })

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(AuthUser, pk=kwargs['pk'])
        profile, _ = Profile.objects.get_or_create(user=user)
        working_detail, _ = WorkingDetail.objects.get_or_create(employee=user)

        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        working_form = WorkingDetailForm(request.POST, instance=working_detail)

        if all([user_form.is_valid(), profile_form.is_valid(), working_form.is_valid()]):
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            working_detail = working_form.save(commit=False)
            working_detail.employee = user
            working_detail.save()
            # return redirect(self.success_url)
            return redirect('user:employee_edit', pk=user.pk)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'working_form': working_form
        })


   
class EmployeeDeleteView(View):
    model = AuthUser
    success_url = reverse_lazy('user:employee_list')

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        # Delete related Profile and WorkingDetail if exist
        profile = getattr(user, 'profile', None)
        if profile:
            profile.delete()

        try:
            working_detail = WorkingDetail.objects.get(employee=user)
            working_detail.delete()
        except WorkingDetail.DoesNotExist:
            pass

        user.delete()

        messages.success(request, "Employee and related data deleted successfully.")
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
