from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from accounts.models import User
import requests


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        # Check passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "signup.html")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "signup.html")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            role=role
        )

        # Send welcome email through serverless email service
        try:
            payload = {
                "type": "SIGNUP_WELCOME",
                "email": email,
                "name": username,
            }

            requests.post(
                "http://localhost:3000/dev/email",
                json=payload,
                timeout=5
            )

        except Exception as e:
            print(f"Email service not available: {e}")

        login(request, user)
        return redirect("dashboard")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def dashboard_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "doctor":
        return redirect("doctor_dashboard")

    return redirect("patient_dashboard")