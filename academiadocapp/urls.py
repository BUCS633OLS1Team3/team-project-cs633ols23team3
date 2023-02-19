from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('transcript/', views.transcript, name='transcript'),
    path('status/', views.status, name='status'),
    path('admin-page/', views.admin_page, name='admin-page'),
    path('update/<request_id>/', views.update_status, name='update-status'),
    path('requests/<int:pk>/download/', views.download_pdf, name='download_pdf'),
    path('upload/<request_id>/', views.upload_file, name='upload'),

]