from django.urls import path
from vendedor.views import *

app_name = 'admini'

urlpatterns = [
    path('list/', AdminListView.as_view() ,name="AdminListView"),
    path('vend_list/', admin_list ,name="admin_list"),
    path('vend_create/', AdminCreateView.as_view() ,name="AdminCreateView"),
    path('vend_update/<int:pk>/', AdminUpdateView.as_view() ,name="AdminUpdateView"),
    path('vend_delete/<int:pk>/', AdminDeleteView.as_view() ,name="AdminDeleteView"),

]