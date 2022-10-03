import re
from django.shortcuts import render,HttpResponse,redirect
from home.models import Signup
from django.contrib.auth.hashers import make_password,check_password
import random,string
import math,random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site 
from django.utils.encoding import force_bytes, force_text   

# from datetime import datetime,timedelta
# from .forms import uploadForm
# from .functions.functions import handle_uploaded_file 
from .forms import *
forget_email=""
otp_send=""
current_time=""

def home(request):
    return render(request,'index.html')
#for signup
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(6) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


def signup(request):
    l,u,s,n=0,0,0,0
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        Last_name = request.POST.get('Last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordrepeat = request.POST.get('passwordrepeat')
        if Signup.objects.filter(username=username,email=email).exists():
            return HttpResponse('user/email already exists')
        elif Signup.objects.filter(username=username).exists():
            return HttpResponse('user already exists')
        elif Signup.objects.filter(email=email).exists():
            return HttpResponse('email already exists')
        else:
            if password == passwordrepeat:
                if len(password)>8:
                    for i in password:
                        if (i.islower()):
                            l+=1
                        if (i.isupper()):
                            u+=1
                        if (i.isdigit()):
                            n+=1
                        if(i=='@'or i=='$' or i=='_'):
                            s+=1
                if (l>=1 and u>=1 and s>=1 and n>=1 and l+s+u+n==len(password)):   
                    password=make_password(password)
                    # global hash_pwd 
                    # hash_pwd = password
                    # password=fernet.encrypt(password.encode())
                    signup=Signup(first_name=first_name,Last_name=Last_name,username=username,email=email,password=password,otp='000000')
                    signup.save()
                    # messages.success(request,'Your account has been created successfully')
                    # return HttpResponse('account created successfully')                      
                else:
                    return HttpResponse('password is to weak')
            else:
                return HttpResponse('password doesnt match !!')
    else:
        return render(request,'signup.html')
#till here

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password1=request.POST.get('password')
        sp=Signup.objects.all()
        for st in sp:
            if username==st.username and check_password(password1,st.password) :
                # return HttpResponse('you are already logged')
                request.session['user']=username
                return redirect('logout.html')
            # else:
        return HttpResponse('wrong credentials')
    else:
        return render(request,'signin.html')

# def opt_send(request):
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def forgot_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        global forget_email
        global otp_send
        global current_time
        em=Signup.objects.all()
        for emv in em:
            if email==emv.email:
                otp_send=generateOTP()
                html=render_to_string('otp_temp.html',{'otp':otp_send})
                send_mail('hii','hello','cyphersystem65@gmail.com',[email],html_message=html)
                # current_time=datetime.now().strftime('%H:%M:%S')
                print(otp_send)
                otp_send=make_password(otp_send)
                forget_email=email
                otp_put=Signup.objects.get(email=forget_email)
                otp_put.otp=otp_send
                otp_put.save()
                return render(request,'otp_verification.html')
            # else:
        return HttpResponse('wrong email')   
    else:
        return render(request,'forget_password.html' )

def otp(request):
    if request.method=='POST':
        otp=request.POST.get('otp')
        email_otp=Signup.objects.all()
        # new_current_time=datetime.now().strftime('%H:%M:%S')
        # verification_time=current_time+timedelta(minutes=5)
        for i in email_otp:
            if forget_email==i.email and check_password(otp,i.otp):
                return render(request,'changing_password.html')
            # elif new_current_time==verification_time:
            #     string_otp=id_generator()
            #     string_otp=make_password(string_otp)
            #     string_otp_put=Signup.objects.get(email=forget_email)
            #     string_otp_put.otp=string_otp
            #     string_otp_put.save()

            else:
                string_otp=id_generator()
                string_otp=make_password(string_otp)
                string_otp_put=Signup.objects.get(email=forget_email)
                string_otp_put.otp=string_otp
                string_otp_put.save()
        return HttpResponse('wrong otp')
    else:
        return render(request,'otp_verification.html')
    
def changing_password(request):
    if request.method=='POST':
        new_password=request.POST.get('new_password')
        confirm_new_password=request.POST.get('confirm_new_password')
        if new_password==confirm_new_password:
            change_pwd=Signup.objects.get(email=forget_email)
            new_password=make_password(new_password)
            change_pwd.password=new_password
            change_pwd.save()
            return HttpResponse('pwd_changed')
        else:
            return HttpResponse('passwords are not same')
    else:
        return render(request,'changing_password.html')

def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('signin')
    return render(request,'logout.html')

def hotel_image_view(request):
  
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = HotelForm()
    return render(request, 'fileupload.html', {'form' : form})
  
  
def success(request):
    return HttpResponse('successfully uploaded')

def display_hotel_images(request):
  
    if request.method == 'GET':
  
        # getting all the objects of hotel.
        Hotels = Hotel.objects.all() 
        return render(request, 'displayimages.html',{'hotel_images' : Hotels})
