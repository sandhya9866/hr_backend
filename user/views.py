from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import AuthUser, Profile, WorkingDetail, GENDER, MARITAL_STATUS, JobType
from .forms import ProfileForm, UserForm, WorkingDetailForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

class EmployeeListView(ListView):
    model = AuthUser  
    template_name = 'user/employee/list.html'
    context_object_name = 'employees'
    paginate_by = 10


    def get_queryset(self):
        queryset = AuthUser.objects.filter(is_active=True).select_related('profile', 'working_detail').order_by('-id')
        
        # Get filter parameters from either POST or GET
        request_data = self.request.POST if self.request.method == 'POST' else self.request.GET
        
        username = request_data.get('username')
        gender = request_data.get('gender')
        marital_status = request_data.get('marital_status')
        job_type = request_data.get('job_type')

        # Apply filters
        if username:
            queryset = queryset.filter(profile__user__username__icontains=username)
        if gender:
            queryset = queryset.filter(profile__gender=gender)
        if marital_status:
            queryset = queryset.filter(profile__marital_status=marital_status)
        if job_type:
            queryset = queryset.filter(working_detail__job_type=job_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genders'] = GENDER
        context['marital_statuses'] = MARITAL_STATUS
        context['job_types'] = JobType.choices
        
        # Get list of usernames for the select dropdown
        context['usernames'] = AuthUser.objects.filter(is_active=True).values_list('username', flat=True).distinct().order_by('username')
        
        # Add current filter values to context from either POST or GET
        request_data = self.request.POST if self.request.method == 'POST' else self.request.GET
        context['current_username'] = request_data.get('username', '')
        context['current_gender'] = request_data.get('gender', '')
        context['current_marital_status'] = request_data.get('marital_status', '')
        context['current_job_type'] = request_data.get('job_type', '')
        
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

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
            'action': 'Create'  
        }
        return render(request, self.template_name, context)

    def post(self, request):
        section = request.POST.get('form_section')

        if section == 'profile':
            user_form = UserForm(request.POST, prefix='user')
            profile_form = ProfileForm(request.POST, prefix='profile')

            if user_form.is_valid() and profile_form.is_valid():
                try:
                    with transaction.atomic():
                        user = user_form.save(commit=False)
                        user.set_password('deli@gbl2079')  # Set default password
                        user.save()

                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile_picture = request.FILES.get('profile-profile_picture')
                        if profile_picture:
                            profile.profile_picture = profile_picture
                        profile.save()

                        request.session['new_user_id'] = user.id
                        messages.success(request, "Profile details saved successfully.")
                        return redirect('user:employee_create')
                except Exception as e:
                    messages.error(request, f"Error creating employee: {str(e)}")
            else:
                messages.error(request, "Please correct the errors below.")

        elif section == 'work':
            working_form = WorkingDetailForm(request.POST, prefix='work')
            if working_form.is_valid():
                user_id = request.session.get('new_user_id')
                if user_id:
                    try:
                        with transaction.atomic():
                            user = AuthUser.objects.get(pk=user_id)
                            working = working_form.save(commit=False)
                            working.employee = user
                            working.save()
                            messages.success(request, "Work details saved successfully.")
                            return redirect(self.success_url)
                    except Exception as e:
                        messages.error(request, f"Error saving work details: {str(e)}")
                else:
                    messages.error(request, "No user found for associating work details.")
            else:
                messages.error(request, "Please correct the errors below.")

        context = {
            'user_form': user_form if section == 'profile' else UserForm(prefix='user'),
            'profile_form': profile_form if section == 'profile' else ProfileForm(prefix='profile'),
            'working_form': working_form if section == 'work' else WorkingDetailForm(prefix='work'),
            'action': 'Create'  # Add action in context for both cases
        }
        return render(request, self.template_name, context)


class EmployeeEditView(UpdateView):
    template_name = 'user/employee/create.html'
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
            'working_form': working_form,
            'profile': profile,
            'action': 'Update'
        })

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(AuthUser, pk=kwargs['pk'])
        profile, _ = Profile.objects.get_or_create(user=user)
        working_detail, _ = WorkingDetail.objects.get_or_create(employee=user)

        section = request.POST.get('form_section')
        
        if section == 'profile':
            user_form = UserForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            working_form = WorkingDetailForm(instance=working_detail)

            if user_form.is_valid() and profile_form.is_valid():
                try:
                    with transaction.atomic():
                        user = user_form.save()

                        profile = profile_form.save(commit=False)
                        profile.user = user
                        # Handle profile picture upload
                        if 'profile-profile_picture' in request.FILES:
                            profile.profile_picture = request.FILES['profile-profile_picture']
                        profile.save()
                        
                        messages.success(request, "Profile details updated successfully.")
                        return redirect('user:employee_create')
                except Exception as e:
                    messages.error(request, f"Error updating profile: {str(e)}")
            else:
                messages.error(request, "Please correct the errors below.")

        elif section == 'work':
            user_form = UserForm(instance=user)
            profile_form = ProfileForm(instance=profile)
            working_form = WorkingDetailForm(request.POST, instance=working_detail)

            if working_form.is_valid():
                try:
                    with transaction.atomic():
                        working_detail = working_form.save(commit=False)
                        working_detail.employee = user
                        working_detail.save()
                        
                        messages.success(request, "Work details updated successfully.")
                        return redirect('user:employee_list')
                except Exception as e:
                    messages.error(request, f"Error updating work details: {str(e)}")
            else:
                messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'working_form': working_form,
            'profile': profile,
            'action': 'Update'
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

class EmployeeDetailView(View):
    template_name = 'user/employee/detail.html'

    def get(self, request, pk):
        employee = get_object_or_404(AuthUser, pk=pk, is_active=True)
        profile = getattr(employee, 'profile', None)
        working_detail = getattr(employee, 'working_detail', None)
        
        context = {
            'employee': employee,
            'profile': profile,
            'working_detail': working_detail,
        }
        return render(request, self.template_name, context)
