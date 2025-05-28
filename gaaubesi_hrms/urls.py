from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginUserView, UserLogoutView, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", dashboard, name= "dashboard"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('employee/', include("user.urls")),
    path('roster/', include("roster.urls")),

    path("leave/", include("leave.urls")),
    path("attendance/", include("attendance.urls")),
    path("fiscal-year/", include("fiscal_year.urls")),

    path('departments/', include('department.urls', namespace='department')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

