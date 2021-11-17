from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .utils import get_client_ip, ipLogger


def index(request):

    currentUser = request.user
    if currentUser.is_authenticated:
        ipDict = {'ip_address': str(get_client_ip(request))}
        ipLogger(ipDict, str(request.user))
        logFile = open('./logs/ipAddressUsers.log', 'r')
        logs = logFile.readlines()
        logs = logs[:-1]
        username = str(request.user)
        ip = ipDict['ip_address']
        for log in logs[::-1]:
            attributes = log.split()
            if attributes:
                if attributes[4] == username:
                    if attributes[6] != ip:
                        print(f"WARNING: {username}'s IP ADDRESS CHANGED")
                        messages.warning(request, 'Warning: your IP address has changed from last time')
                        break
                    else:
                        break
        logFile.close()

    return render(request, 'accounts/index.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username just taken, try with an other...')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email just taken, try with an other...')
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name,
                                                last_name=last_name)
                user.save()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('login')

        else:
            messages.info(request, 'Enter the same password to confirm')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'accounts/login.html')

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
