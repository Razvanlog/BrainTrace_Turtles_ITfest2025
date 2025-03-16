from django.urls import path, include
from myapp import views
from django.views.generic import TemplateView
from .views import form, submit_form, success_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('form/', views.form, name='form'),
    path('submit/', views.submit_form, name="submit_form"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path("success/", success_view, name="success"),
   ]
