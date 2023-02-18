import re
from venv import create
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render , redirect
from .models import User, Requests, Events, Comments, Directory, Profile, Transcripts
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
import os



def index(request):


    if request.user.is_authenticated:

        return render(request, "academiadocapp/index.html", {

            "user": request.user,

        })

    else:
        return render(request, "academiadocapp/login.html", {

            "user": request.user,

        })



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request,('Passwords must match.'))
            return redirect('register')
        #make sure email is valid
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request,('Email is invalid'))
            return redirect('register')             
        # strong password validation
        try:
            validate_password(password, None, None)
        except ValidationError:
            messages.warning(request,('Please do not create passwords that are: too similar to the user details, below length of 8, too common or all numeric'))
            return redirect('register')
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user)

        except IntegrityError:
            messages.warning(request,('Username already taken.'))
            return redirect('register')
 
        login(request, user)
        messages.success(request,('New User '+ username + ' Created'))
        return redirect("home")
    else:
        user = request.user
        if (user.is_authenticated):
            return redirect("home")
        else:
            return render(request, "academiadocapp/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request,('Login Successful'))
            return redirect('home')
        else:
            messages.warning(request,('Error Logging In, Try Again...'))
            return redirect('login')
    else:
        user = request.user
        if (user.is_authenticated):
            return redirect("home")
        else:
            return render(request, "academiadocapp/login.html")



def logout_view(request):
    logout(request)
    messages.warning(request,('Log Out Successful'))
    return redirect('home')

@login_required
def transcript(request):

    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('agree'):
                agreement = True
            transcript_request = Requests(creator=user, delivery_email=request.POST["email"], purpose=request.POST["purpose"], agreement=agreement)
            transcript_request.save()
            messages.success(request,('Request Submitted Successfully'))

    return render(request, "academiadocapp/transcript.html")


@login_required
def status(request):

    user = request.user
    transcript_requests = Requests.objects.filter(creator=user).all()
    count = Requests.objects.filter(creator=user).count()

    context = {
        'requests' : transcript_requests,
        'count' : count
    }

    return render(request, "academiadocapp/status.html", context)

@user_passes_test(lambda user: user.is_staff)
@login_required
def admin_page(request):

    user = request.user
    transcript_requests = Requests.objects.all()
    count = Requests.objects.all().count()

    context = {
        'requests' : transcript_requests,
        'count' : count
    }
    return render(request, "academiadocapp/admin.html", context)

@user_passes_test(lambda user: user.is_staff)
@login_required
def update_status(request, request_id):

    transcript_request = Requests.objects.get(pk=request_id)
    if transcript_request.pdf_file:
        file_name = transcript_request.pdf_file.name.split('/')[-1]
    else:
        file_name = ''

    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        transcript_request.pdf_file = uploaded_file

        transcript_request.save()
        
        messages.success(request, f'File Uploaded successfully!')

        return redirect('update-status', request_id)

    elif request.method == "POST":

        # update the approve date if it exists in the form
        if request.POST.get('approve', '') != '':
            transcript_request.approve_date = request.POST.get('approve')
        # update the process date if it exists in the form
        if request.POST.get('process', '') != '':
            transcript_request.process_date = request.POST.get('process')
        # update the complete date if it exists in the form
        if request.POST.get('complete', '') != '':
            transcript_request.complete_date = request.POST.get('complete')
        # update the close date if it exists in the form
        if request.POST.get('close', '') != '':
            transcript_request.close_date = request.POST.get('close')
        # save the updated request object
        
        transcript_request.save()

        messages.success(request, f'Request updated successfully!')

        return redirect('admin-page')

    context = {
        'request' : transcript_request,
        'file_name': file_name,
    }
    return render(request, "academiadocapp/update.html", context)


@login_required
def download_pdf(request, pk):
    my_request = get_object_or_404(Requests, pk=pk)
    if my_request.pdf_file:
        try:
            # Open the file in a read-only mode
            pdf_file = my_request.pdf_file.path
            with open(pdf_file, 'rb') as fh:
                # Set the mime type
                response = HttpResponse(fh.read(), content_type="application/pdf")
                # Set the file object name
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(pdf_file)
                return response
        except IOError:
            raise Http404
    else:
        return HttpResponse("Sorry, file does not exist")
