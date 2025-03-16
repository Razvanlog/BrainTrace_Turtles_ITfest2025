from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import RedirectView
from django.shortcuts import redirect
from .models import PatientData
from .forms import PatientDataForm
# Create your views here.
def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "myapp/about.html")

def chatbot(request):
    return render(request, "myapp/chatbot.html")
def form(request):
    if request.method == "POST":
        form = PatientDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success")  # Redirect to success page
    else:
        form = PatientDataForm()

    return render(request, "myapp/form.html", {"form": form})


def submit_form(request):
    if request.method == "POST":
        form = PatientDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page after saving

    return render(request, 'myapp/form.html', {'form': form})
def success_view(request):
    return render(request, 'myapp/success.html')