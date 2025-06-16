from django.urls import path
from . import views

app_name = 'branch'

urlpatterns = [
    path('list/', views.BranchListView.as_view(), name='branch_list'),
    path('create/', views.BranchCreateView.as_view(), name='branch_create'),
    path('edit/<int:pk>/', views.BranchUpdateView.as_view(), name='branch_edit'),
    path('delete/<int:pk>/', views.BranchDeleteView.as_view(), name='branch_delete'),
] 