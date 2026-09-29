from django.urls import path

from . import views

urlpatterns = [
    path('', views.sub_list, name='sub_list'),
    path('add/', views.sub_create, name='sub_create'),
    path('<int:pk>/edit/', views.sub_edit, name='sub_edit'),
    path('<int:pk>/delete/', views.sub_delete, name='sub_delete'),
    path('<int:pk>/pay/', views.sub_pay, name='sub_pay'),
    path('payments/', views.payment_history, name='payment_history'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
]
