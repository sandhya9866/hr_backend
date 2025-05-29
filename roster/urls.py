from django.urls import include, path
from .views import RosterListView, ShiftListView, ShiftCreateView, ShiftEditView, ShiftDeleteView

app_name = 'roster'


urlpatterns = [
    path('shift/list/', ShiftListView.as_view(), name='shift_list'),
    path('shift/create/', ShiftCreateView.as_view(), name='shift_create'),
    path('shift/edit/<int:pk>', ShiftEditView.as_view(), name='shift_edit'),
    path('shift/delete/<int:pk>', ShiftDeleteView.as_view(), name='shift_delete'),

    path('list/', RosterListView.as_view(), name='roster_list'),

]