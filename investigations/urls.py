from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('landing/', views.landing_page, name='landing_alias'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.analyst_profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('investigate/', views.create_case, name='create_case'),
    path('case/<uuid:pk>/', views.case_detail, name='case_detail'),
    path('case/<uuid:pk>/rerun-ai/', views.rerun_ai, name='rerun_ai'),
    path('case/<uuid:pk>/report/', views.report_pdf, name='report_pdf'),
]
