from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import os

from django.urls import reverse_lazy
# from documents.models import ContractDocument, Document
from .forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.utils import timezone

# from profiles.models import UserProfile


@login_required
def dashboard(request):
    user = request.user
    type = user.attendance_status_button
   
    try:
        employee_shift = user.working_detail.shift
    except AttributeError:
        employee_shift = None
        # messages.warning(request, "No profile found for this user.")

    btn_status = 'show'
    if employee_shift != None:
        if type == 'CheckIn':
            if employee_shift.min_start_time:
                if timezone.now().time() < employee_shift.min_start_time:
                    btn_status = 'hide'
                    messages.error(request, "Check-in time is outside of the allowed range.")

        elif type == 'CheckOut':
            if employee_shift.max_end_time:
                if employee_shift.max_end_time < timezone.now().time():
                    btn_status = 'hide'
                    messages.error(request, "Check-out time is outside of the allowed range.")

    context = {
        'btn_status': btn_status,
    }
    return render(request, 'dashboard.html', context)

# def secure_doc(request,user,file,type):
#     if type == 'contracts':
#         document=get_object_or_404(ContractDocument, file=f"contracts/{user}/{file}")
#     else:
#         document=get_object_or_404(Document, file=f"documents/{user}/{file}")
#     # if request.user.has_perm('permissions.employee_document_permission'):
#     #     document=get_object_or_404(ContractDocument, file=f"{type}/{user}/{file}")
#     # else:
#     #     document=get_object_or_404(ContractDocument, file=f"{type}/{user}/{file}", user=request.user)
#     # path,file_name=os.path.split(file)
#     response=FileResponse(document.file)
#     return response


class LoginUserView(View):
    template_name = 'login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")

        return render(request, self.template_name, context={'form':self.form_class()})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password'))

            # if user is not None and user.profile.role == 'Super-Admin':
            if user is not None:
                next_url = self.request.GET.get('next')
                login(self.request, user)
                if next_url:
                    return redirect(next_url)
                return redirect('/')   
            else:
                messages.error(self.request, 'Invalid login credentials')


        return render(request, self.template_name, context={'form':form})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
