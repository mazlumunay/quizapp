from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import auth


# Views for user authentication and registration

class RegistrationView(View):
    """
    View for user registration.

    GET: Renders the registration form.
    POST: Validates user input, creates a new user account if input is valid.
    """

    def get(self, request):
        """Render the registration form."""
        return render(request, 'authentication/register.html')

    def post(self, request):
        """Handle form submission for user registration."""
        # Get user data from form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {'fieldValues': request.POST}

        # Check if username exists
        if not User.objects.filter(username=username).exists():
            # Check if email exists
            if not User.objects.filter(email=email).exists():
                # Validate password length
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                # Create user account
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()

                messages.success(request, 'Account created successfully')
                return redirect('login')

        return render(request, 'authentication/register.html')


class UsernameValidationView(View):
    """
    View for validating username uniqueness and format.

    POST: Validates the username format and checks if it's unique.
    """

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, username is already taken'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    """
    View for validating email uniqueness and format.

    POST: Validates the email format and checks if it's unique.
    """

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, email is already taken'}, status=409)
        return JsonResponse({'email_valid': True})


class LoginView(View):
    """
    View for user login.

    GET: Renders the login form.
    POST: Authenticates user credentials and logs in the user if valid.
    """

    def get(self, request):
        """Render the login form."""
        return render(request, 'authentication/login.html')

    def post(self, request):
        """Handle form submission for user login."""
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    # Redirect to the homepage after successful login
                    return redirect('index_page')

            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill username and password')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    """
    View for user logout.

    POST: Logs out the currently authenticated user.
    """

    def post(self, request):
        """Handle user logout."""
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
