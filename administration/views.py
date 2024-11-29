from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from django.http import HttpResponse
from django.urls import reverse
from .models import Account
from .forms import AccountForm
from django.core.mail import send_mail
from administration.models import Account, OTP
from datetime import timedelta
from .models import OTP, Session
from django.contrib.auth.models import User
from django.contrib import messages
import random

def generate_otp():
    return random.randint(100000, 999999)

# datas = Account.objects.all()

def login1(responce):
    if responce.method == 'POST':
        print("POST...")
        username = responce.POST.get('username')
        password = responce.POST.get('password')
        print(password)
        
        try:
            
            user = Account.objects.get(username=username)
            print(user.username)
            if check_password(password, user.password):
                print("password match")
                return render(responce,'success.html')
            else:
                print("password not match")
                return render(responce,'login.html', {'warning_message':"Password does not match.", 'flag':"forget"})
            

        except Exception as e:
            print("Exception:",e)
            messages.error(responce, "Username does not exist. Please register.")
            return render(responce,'login.html')
            # return render(responce,'login.html')
            
    else:
        return render(responce,'login.html')

# def login(responce):
#     userflag=False
#     if responce.method == 'POST':
#             print("POST OK")
#             password = responce.POST.get('password')
#             for data in datas:
#                 print(data.username)
        
#                 if responce.POST.get('username') == data.username:
#                      print("username exist")
#                      print(data.password)
#                      if check_password(password, data.password):
#                          print("password match")
#                          userflag=True
#                          return render(responce,'success.html')
#                          break
#                      else:
#                          print("password not match")
#                          userflag=True
#                          return render(responce,'login.html', {'warning_message':"Password does not match.", 'flag':"forget"})
                     
#                      #break            
            
#             if userflag==False:
#                  print("username not exist")
#                  return render(responce,'login.html', {'warning_message':"Username does not exist. Please register. "})
#             #print(username)
#             return render(responce,'login.html')
#     else:
#         print("Method", responce.method)
#         return render(responce,'login.html')


# Create your views here.
#def signup(responce):
#    if responce.method == 'POST':
#        pass
#    else:
#        return render(responce,'signup.html')


def signup(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data['username'])
            return render(request, 'success.html')
            #return redirect('success')  # Replace 'success' with your success URL name
    else:
        form = AccountForm()
    return render(request, 'signup.html', {'form': form})

def verifyEmail(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            #print(email)
            user = Account.objects.get(email=email)
            print(user.email, user.username)
            #generate_otp(request, user.username)
            request.session['username'] = user.username
            request.session['email'] = user.email
            return redirect('generate_otp')

        except Account.DoesNotExist:
            return render(request, "generate_otp_new.html", {"email": "Account Doesn't Exist", "username": "Username Doesn't Exist"})
    else:
        return render(request, "verifyEmail.html")
   

def generate_otp(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        print(username)
        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            print( f"User does not exist for. {username}")
            messages.error(request, "User does not exist.")
            return redirect("verifyemail")

        # Generate or update OTP for the user
        otp, created = OTP.objects.get_or_create(user=user, is_verified=False)
        otp.generate_otp()

        # Simulate sending OTP (integrate email/SMS here)
        s = send_mail("OTP - OTP",f"Your OTP IS--> {otp.otp_code}","admin@django.com",["anupam.dutta@weaversweb.com"])
        if s==1:
            print(s)
            print(f"Generated OTP for {user.username}: {otp.otp_code}")
            messages.success(request, "OTP has been sent! Please check your email or phone.")
            return redirect("verify_otp")
    else:
        username = request.session.get('username')
        print( "Username:",username)
        return render(request, "generate_otp_new.html", {'username':username})


def verify_otp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        entered_otp = request.POST.get("otp")
        try:
            
            user = Account.objects.get(username=username)

           
            otp = OTP.objects.filter(user=user, is_verified=False).latest('created_at')

           
            if otp.is_expired():
                messages.error(request, "The OTP has expired. Please request a new one.")
                return redirect("generate_otp")

            # Verify the OTP
            if otp.otp_code == entered_otp:
                otp.is_verified = True
                otp.save()

                # Check if a session exists for the user, or explicitly create one
                session, created = Session.objects.get_or_create(
                    user=user,
                    defaults={
                        "session_key": f"{user.username}_{now().timestamp()}",
                        "expires_at": now() + timedelta(hours=1),
                    },
                )
                # Update the session if it already exists
                if not created:
                    session.session_key = f"{user.username}_{now().timestamp()}"
                    session.expires_at = now() + timedelta(hours=1)
                    session.save()

                messages.success(request, "OTP verified successfully!")
                return redirect("newpassword")
            else:
                messages.error(request, "Invalid OTP. Please try again.")

        except Account.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("generate_otp")
        except OTP.DoesNotExist:
            messages.error(request, "No OTP found for this user. Please request a new one.")
            return redirect("generate_otp")
    else:
        username = request.session.get('username')
        print("In verify otp: ",username)
        return render(request, "verify_otp.html",{'username':username})
def success_page(request):
    return render(request, "success.html")

def newpassword(request):
    if request.method == "POST":
        print("inside POSt")
        confirm_password = request.POST.get("confirm_password")
        username = request.POST.get("username")
        print("Password: ", confirm_password)
        print("username: ",username)

        try:
            print("Edited...")
            user = Account.objects.get(username=username)
            print("Edited...2", user.username)
            
            
            user.password = confirm_password                                                                                                                                                                                                                           
            user.save()
            

            print("Password updated successfully.")
            return redirect('login')
        except Exception as e:
            print(e)
            print("Password Not updated.")
            return redirect('verifyemail')

        print(username)
        
    else:
        username = request.session.get('username')
        email = request.session.get('email')
        return render(request, "newpassword.html", {'username':username,'email':email})


