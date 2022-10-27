from django.shortcuts import render,HttpResponse,redirect
from home.models import Signup
from django.contrib.auth.hashers import make_password,check_password
import random,string
import math,random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import *

forget_email=""
otp_send=""
current_time=""
islogin=False
isforgetcheck=False
service_islogin=False
service_isforgetcheck=False


#------------------common-------------function-----------used---------in--------both--------------------
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(6) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

def token():
    import secrets
    return secrets.token_urlsafe(16)

def home(request):
    return render(request,'index.html')

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#------------------customer--------------------------function--------------------

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
                        if(i=='@'or i=='$' or i=='_' or i=="'" or i=='%' or i=='!' or i=='&' or i=='*'):
                            s+=1
                if (l>=1 and u>=1 and s>=1 and n>=1 and l+s+u+n==len(password)):   
                    password=make_password(password)
                    # global hash_pwd 
                    # hash_pwd = password
                    # password=fernet.encrypt(password.encode())
                    signup=Signup(first_name=first_name,Last_name=Last_name,username=username,email=email,password=password,otp='000000',token='ab')
                    signup.save()
                    # messages.success(request,'Your account has been created successfully')
                    # return HttpResponse('account created successfully')                      
                    return redirect('signin.html')
                    
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
        # global islogin
        global name
        global islogin
        global create_token
        islogin=False
        sp=Signup.objects.all() # use filter instead of all
        for st in sp:
            if username==st.username and check_password(password1,st.password) :
                # return HttpResponse('you are already logged')
                request.session['user']=username
                create_token=token()
                token_put=Signup.objects.get(username=username)
                token_put.token=create_token
                token_put.save()
                islogin=True
                name=username
                return redirect('bargin.html')
        return HttpResponse('wrong credentials')
    else:
        return render(request,'signin.html')

#this is used for bargin
                                                                # print(request.user.id)

                        



def forgot_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        global forget_email
        global otp_send
        global current_time
        global isforgetcheck
        global forget_token

        if Signup.objects.filter(email=email).exists():
            otp_send=generateOTP()
            # html=render_to_string('otp_temp.html',{'otp':otp_send})
            # send_mail('hii','hello','cyphersystem65@gmail.com',[email],html_message=html)
            # current_time=datetime.now().strftime('%H:%M:%S')
            print(otp_send)
            otp_send=make_password(otp_send)
            forget_token=token()
            forget_email=email
            otp_put=Signup.objects.get(email=forget_email)
            otp_put.otp=otp_send
            otp_put.token=forget_token
            isforgetcheck=True
            otp_put.save()
            return render(request,'otp_verification.html')
            # else:
        return HttpResponse('wrong email')   
    else:
        return render(request,'forget_password.html' )

def otp(request):
    if isforgetcheck and Signup.objects.filter(email=forget_email,token=forget_token).exists():
        if request.method=='POST':
            otp=request.POST.get('otp')
            email_otp=Signup.objects.all()
            for i in email_otp:
                if forget_email==i.email and check_password(otp,i.otp):
                    return render(request,'changing_password.html')

                else:
                    string_otp=id_generator()
                    string_otp=make_password(string_otp)
                    string_otp_put=Signup.objects.get(email=forget_email)
                    string_otp_put.otp=string_otp
                    string_otp_put.save()
            return HttpResponse('wrong otp')
        else:
            return render(request,'otp_verification.html')
    return render(request,'forget_password.html')
    
def changing_password(request):
    if isforgetcheck and Signup.objects.filter(email=forget_email,token=forget_token).exists():
        if request.method=='POST':
            new_password=request.POST.get('new_password')
            confirm_new_password=request.POST.get('confirm_new_password')
            if new_password==confirm_new_password:
                change_pwd=Signup.objects.get(email=forget_email)
                new_password=make_password(new_password)
                change_pwd.password=new_password
                change_pwd.save()
                return HttpResponse('signin.html')
            else:
                return HttpResponse('passwords are not same')
        else:
            return render(request,'changing_password.html')
    return render(request,'forgot_password.html')

def logout(request):
    global islogin
    try:
        del request.session['user']
    except:
        token_puting=Signup.objects.get(username=name)
        creating_token=token()
        token_puting.token=creating_token
        token_puting.save()
        islogin=False
        return redirect('signin.html')
    return render (request,'logout.html',{'name':name})

def bargin(request):

    if islogin and Signup.objects.filter(username=name,token=create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            a=0
            service_name=[]
            amt=[]
            tr=[]
            global service
            global amount
            amount=request.POST.get('bargin')
            service=request.POST.get('service')
            bg=Signup_service.objects.all()
            amount=int(amount)
            for mj in bg:
                if service==mj.service and amount>=mj.amount:
                    service_name.append(mj.username)
                    amt.append(mj.amount)
                    a+=1
            mylist=zip(service_name,amt)
            cont={'mylist':mylist,}
            # print(mylist.service_name)
            if a ==0:
                return HttpResponse('increase the price') 
            return render(request,'sending_request.html', cont)
        return render(request,'bargin.html')
    return render(request,'signin.html')

def sending_request(request):
    if islogin and Signup.objects.filter(username=name,token=create_token).exists():
        if request.method=='POST':
            mi=0
            serv_name=[]
            amt=[]
            service_usr=request.POST.get('service_usr')
            bargin_amt=request.POST.get('bargin_amt')
            if Signup_service.objects.filter(username=service_usr).exists():
                if perfect_service.objects.filter(service_usr=service_usr,customer_usr=name).exists():
                    updating_amt=perfect_service.objects.get(service_usr=service_usr,customer_usr=name)
                    updating_amt.amt_offered=bargin_amt
                    # updating_amt.service=service

                    updating_amt.save()
                else:
                    servic=perfect_service(amt_offered=bargin_amt,customer_usr=name,service_usr=service_usr,service_boolean='0',customer_boolean='0',service=service)
                    servic.save()
                bg=Signup_service.objects.all()
                for mj in bg:
                    if service==mj.service and amount>=mj.amount:
                        serv_name.append(mj.username)
                        amt.append(mj.amount)
                        mi+=1
                mylist=zip(serv_name,amt)
                cont={'mylist':mylist,}
            return render(request,'sending_request.html', cont)
        else:
            mi=0
            serv_name=[]
            amt=[]
            bg=Signup_service.objects.all()
            for mj in bg:
                if service==mj.service and amount>=mj.amount:
                    serv_name.append(mj.username)
                    amt.append(mj.amount)
                    mi+=1
            mylist=zip(serv_name,amt)
            cont={'mylist':mylist,}
            return render(request,'sending_request.html', cont)

    return render(request,'signin.html')


def pending_request(request):
    if islogin and Signup.objects.filter(username=name,token=create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            pass
        else:
            service_name=[]
            amt=[]
            ser_amt=[]
            serv_get=[]
            y=0
            data=perfect_service.objects.all()
            for k in data:
                if k.customer_usr==name and k.service_boolean=='0':
                    service_name.append(k.service_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    serv_get.append(k.service)
                    # serv_get.append(k.service_recieved)
                    y+=1
            
            if y==0:                
                return HttpResponse('no request is pending')
            mylist=zip(service_name,amt,ser_amt,serv_get)
            cont={'mylist':mylist,}
            return render(request,'pending_request.html',cont)#dashboard or profile
    return render(request,'signin.html')
          
def delete_request(request):
    if islogin and Signup.objects.filter(username=name,token=create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            serv_get=[]
            service_usr=request.POST.get('service_usr')
            if perfect_service.objects.filter(service_usr=service_usr,customer_usr=name).exists():
                perfect_service.objects.filter(service_usr=service_usr,customer_usr=name).delete()
                data=perfect_service.objects.all()
                for k in data:
                    if k.customer_usr==name and k.service_boolean=='0':
                        serv_name.append(k.service_usr)
                        amt.append(k.amt_offered)
                        ser_amt.append(k.ser_amt_offered)
                        serv_get.append(k.service)
                        z+=1
                if z==0:                
                    return HttpResponse('no request is pending')
                mylist=zip(serv_name,amt,ser_amt,serv_get)
                cont={'mylist':mylist,}
            return render(request,'pending_request.html',cont)
                # return render(request,'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
            # return render(request, 'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt,'service':serv_get}) #with a message that please enter right datat
        else:
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            serv_get=[]
            data=perfect_service.objects.all()
            for k in data:
                if k.customer_usr==name and k.service_boolean=='0':
                    serv_name.append(k.service_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    serv_get.append(k.service)
                    z+=1
            if z==0:                
                return HttpResponse('no request is pending')
            mylist=zip(serv_name,amt,ser_amt,serv_get)
            cont={'mylist':mylist,}
            return render(request,'pending_request.html',cont)
            # return render(request, 'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt,'service':serv_get}) #with a message that please enter right datat   #dashboard   #dashboard
    return render(request, 'signin.html')

def accept_request(request):
    if islogin and Signup.objects.filter(username=name,token=create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            serv_get=[]
            service_usr=request.POST.get('service_usr')
            bargin_amt=request.POST.get('bargin_amt')
            if perfect_service.objects.filter(service_usr=service_usr,ser_amt_offered=bargin_amt,customer_usr=name).exists():
                accept=perfect_service.objects.get(service_usr=service_usr,ser_amt_offered=bargin_amt,customer_usr=name)
                accept.service_boolean='1'
                accept.customer_boolean='1'
                accept.final=bargin_amt
                accept.save()
                data=perfect_service.objects.all()
                for k in data:
                    if k.customer_usr==name and k.service_boolean=='0':
                        serv_name.append(k.service_usr)
                        amt.append(k.amt_offered)
                        ser_amt.append(k.ser_amt_offered)
                        serv_get.append(k.service)
                        z+=1
                if z==0:                
                    return HttpResponse('no request is pending')
                mylist=zip(serv_name,amt,ser_amt,serv_get)
                cont={'mylist':mylist,}
            return render(request,'pending_request.html',cont)
                # return render(request,'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
            # return render(request, 'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt,'service':serv_get,'service':serv_get}) #with a message that please enter right datat
        else:
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            serv_get=[]
            data=perfect_service.objects.all()
            for k in data:
                if k.customer_usr==name and k.service_boolean=='0':
                    serv_name.append(k.service_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    serv_get.append(k.service)
                    z+=1
            if z==0:                
                return HttpResponse('no request is pending')
            mylist=zip(serv_name,amt,ser_amt,serv_get)
            cont={'mylist':mylist,}
            return render(request,'pending_request.html',cont)
            # return render(request, 'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt,'service':serv_get}) #with a message that please enter right datat   #dashboard
    return render(request, 'signin.html')


def bargin_request(request):
    if islogin and Signup.objects.filter(username=name,token=create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            serv_get=[]
            servic_usr=request.POST.get('service_usr')
            bargin_amt=request.POST.get('bargin_amt')
            if perfect_service.objects.filter(service_usr=servic_usr,service_boolean='0',customer_usr=name).exists():
                accept=perfect_service.objects.get(service_usr=servic_usr,service_boolean='0',customer_usr=name)
                accept.amt_offered=bargin_amt
                accept.save()
                data=perfect_service.objects.all()
                for k in data:
                    if k.customer_usr==name and k.service_boolean=='0':
                        serv_name.append(k.service_usr)
                        amt.append(k.amt_offered)
                        ser_amt.append(k.ser_amt_offered)
                        serv_get.append(k.service)
                        z+=1
                if z==0:                
                    return HttpResponse('no request is pending')    
                mylist=zip(serv_name,amt,ser_amt,serv_get)
                cont={'mylist':mylist,}
            return render(request,'pending_request.html',cont)
                # return render(request,'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
            # return render(request, 'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt,'service':serv_get}) #with a message that please enter right datat
        else:
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            serv_get=[]
            data=perfect_service.objects.all()
            for k in data:
                if k.customer_usr==name and k.service_boolean=='0':
                    serv_name.append(k.service_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    serv_get.append(k.service)
                    z+=1
            if z==0:                
                return HttpResponse('no request is pending')
                
            mylist=zip(serv_name,amt,ser_amt,serv_get)
            cont={'mylist':mylist,}
            return render(request,'pending_request.html',cont)
                # return render(request,'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
            # return render(request, 'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt,'service':serv_get}) #with a message that please enter right datat
    return render(request, 'signin.html')



def accepted(request): #to check the accepted request
    if islogin and Signup.objects.filter(username=name,token=create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            pass
        else:
            m=0
            serv_name=[]
            amt=[]
            serv_get=[]
            accept=perfect_service.objects.all()
            for i in accept:
                if i.service_boolean=='1'and i.customer_usr==name:
                    serv_name.append(i.service_usr)
                    amt.append(i.final)
                    serv_get.append(i.service)
                    m+=1
            if m==0:
                return HttpResponse('no request accepted')
                
            mylist=zip(serv_name,amt,serv_get)
            cont={'mylist':mylist,}
            return render(request,'accept_request.html',cont)
            # return render(request,'accept_request.html',{'service_name':serv_name,'amt':amt,'y':range(m),'service':serv_get})
    return render(request, 'signin.html')
                    




#------------------file-----------------------------------------------uploading--------------------------code-----------------------------

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


#------------------------------code -------------------for--------------service------------------provider---------------------------------
    

def signup_service(request):
    l,u,s,n=0,0,0,0
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        Last_name = request.POST.get('Last_name')
        username = request.POST.get('username')
        amount = request.POST.get('amount')
        service= request.POST.get('service')
        email = request.POST.get('email')
        password = request.POST.get('password')
        passwordrepeat = request.POST.get('passwordrepeat')
        if Signup_service.objects.filter(username=username,email=email).exists():
            return HttpResponse('user/email already exists')
        elif Signup_service.objects.filter(username=username).exists():
            return HttpResponse('user already exists')
        elif Signup_service.objects.filter(email=email).exists():
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
                        if(i=='@'or i=='$' or i=='_' or i=="'" or i=='%' or i=='!' or i=='&' or i=='*'):
                            s+=1
                if (l>=1 and u>=1 and s>=1 and n>=1 and l+s+u+n==len(password)):   
                    password=make_password(password)
                    # global hash_pwd 
                    # hash_pwd = password
                    # password=fernet.encrypt(password.encode())
                    Signup=Signup_service(first_name=first_name,Last_name=Last_name,username=username,email=email,password=password,otp='000000',token='ab',amount=amount,service=service)
                    Signup.save()
                    # messages.success(request,'Your account has been created successfully')
                    # return HttpResponse('account created successfully')                      
                    return redirect('service_signin.html')
                    
                else:
                    return HttpResponse('password is to weak')
            else:
                return HttpResponse('password doesnt match !!')
    else:
        return render(request,'signup_service.html')
#till here



def sign_service(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password1=request.POST.get('password')
        # global islogin
        global service_name
        global service_islogin
        global service_create_token
        service_islogin=False
        sp=Signup_service.objects.all() # use filter instead of all
        for st in sp:
            if username==st.username and check_password(password1,st.password) :
                # return HttpResponse('you are already logged')
                request.session['user']=username
                service_create_token=token()
                token_put=Signup_service.objects.get(username=username)
                token_put.token=service_create_token
                token_put.save()
                service_islogin=True
                service_name=username
                return render(request,'service_logout.html')
        return HttpResponse('wrong credentials')
    else:
        return render(request,'service_signin.html')


def service_forgot_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        global service_forget_email
        global service_otp_send
        global service_current_time
        global service_isforgetcheck
        global service_forget_token

        if Signup_service.objects.filter(email=email).exists():
            service_otp_send=generateOTP()
            # html=render_to_string('otp_temp.html',{'otp':otp_send})
            # send_mail('hii','hello','cyphersystem65@gmail.com',[email],html_message=html)
            # current_time=datetime.now().strftime('%H:%M:%S')
            print(service_otp_send)
            service_otp_send=make_password(service_otp_send)
            service_forget_token=token()
            service_forget_email=email
            otp_put=Signup_service.objects.get(email=service_forget_email)
            otp_put.otp=service_otp_send
            otp_put.token=service_forget_token
            service_isforgetcheck=True
            otp_put.save()
            return render(request,'service_otp.html')
            # else:
        return HttpResponse('wrong email')   
    else:
        return render(request,'service_forget_ped.html' )

def service_otp(request):
    if service_isforgetcheck and Signup_service.objects.filter(email=service_forget_email,token=service_forget_token).exists():
        if request.method=='POST':
            otp=request.POST.get('otp')
            email_otp=Signup_service.objects.all()
            for i in email_otp:
                if service_forget_email==i.email and check_password(otp,i.otp):
                    return render(request,'service_changing_pwd.html')

                else:
                    string_otp=id_generator()
                    string_otp=make_password(string_otp)
                    string_otp_put=Signup_service.objects.get(email=service_forget_email)
                    string_otp_put.otp=string_otp
                    string_otp_put.save()
            return HttpResponse('wrong otp')
        else:
            return render(request,'service_otp.html')
    return render(request,'service_forget_ped.html')
    
def service_changing_password(request):
    if service_isforgetcheck and Signup_service.objects.filter(email=service_forget_email,token=service_forget_token).exists():
        if request.method=='POST':
            new_password=request.POST.get('new_password')
            confirm_new_password=request.POST.get('confirm_new_password')
            if new_password==confirm_new_password:
                change_pwd=Signup_service.objects.get(email=service_forget_email)
                new_password=make_password(new_password)
                change_pwd.password=new_password
                # service_create_token=token()
                # change_pwd.token=service_create_token
                change_pwd.save()
                # return HttpResponse('pwd_changed')
                return render(request,'service_signin.html')
            else:
                return HttpResponse('passwords are not same')
        else:
            service_create_token=token()
            return render(request,'service_signin.html')
    return render(request,'service_forget_ped.html')

def service_logout(request):
    global service_islogin
    try:
        del request.session['user']
    except:
        token_puting=Signup_service.objects.get(username=service_name)
        creating_token=token()
        token_puting.token=creating_token
        token_puting.save()
        service_islogin=False
        return redirect('service_signin.html')
    return render (request,'service_logout.html',{'name':service_name})

def service_recieve_request(request):
    if service_islogin and Signup_service.objects.filter(username=service_name,token=service_create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            pass
        else:
            cust_name=[]
            amt=[]
            ser_amt=[]
            y=0
            data=perfect_service.objects.all()
            for k in data:
                if k.service_usr==service_name and k.service_boolean=='0':
                
                    cust_name.append(k.customer_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    y+=1
            if y==0:                
                return HttpResponse('no request is pending')
                
            mylist=zip(cust_name,amt,ser_amt)
            cont={'mylist':mylist,}
            return render(request,'ser_receive_request.html',cont)
            # return render(request,'ser_receive_request.html',{'service_name':cust_name,'amt':amt,'y':range(y),'ser_amt':ser_amt})#dashboard or profile
    return render(request,'service_signin.html')

def service_delete_request(request):
    if service_islogin and Signup_service.objects.filter(username=service_name,token=service_create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            cust_usr=request.POST.get('service_usr')
            if perfect_service.objects.filter(customer_usr=cust_usr,service_usr=service_name).exists():
                perfect_service.objects.filter(customer_usr=cust_usr,service_usr=service_name).delete()
                data=perfect_service.objects.all()
                for k in data:
                    if k.service_usr==service_name and k.service_boolean=='0':
                        serv_name.append(k.customer_usr)
                        amt.append(k.amt_offered)
                        ser_amt.append(k.ser_amt_offered)
                        z+=1
                if z==0:                
                    return HttpResponse('no request is pending')
                mylist=zip(serv_name,amt,ser_amt)
                cont={'mylist':mylist,}
            return render(request,'ser_receive_request.html',cont)
                # return render(request,'ser_receive_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
            # return render(request, 'ser_receive_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
        else:
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            data=perfect_service.objects.all()
            for k in data:
                if k.service_usr==service_name and k.service_boolean=='0':
                    serv_name.append(k.customer_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    z+=1
            if z==0:                
                return HttpResponse('no request is pending')
                
            mylist=zip(serv_name,amt,ser_amt)
            cont={'mylist':mylist,}
            return render(request,'ser_receive_request.html',cont) #with a message that please enter right datat
        # return HttpResponse('login again')   #dashboard
    return render(request, 'service_signin.html')

def service_accept_request(request):
    if service_islogin and Signup_service.objects.filter(username=service_name,token=service_create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            cust_usr=request.POST.get('service_usr')
            amt_ready=request.POST.get('bargin_amt')
            if perfect_service.objects.filter(customer_usr=cust_usr,amt_offered=amt_ready,service_usr=service_name).exists():
                accept=perfect_service.objects.get(customer_usr=cust_usr,amt_offered=amt_ready,service_usr=service_name)
                accept.service_boolean='1'
                accept.customer_boolean='1'
                accept.final=amt_ready
                accept.save()
                data=perfect_service.objects.all()
                for k in data:
                    if k.service_usr==service_name and k.service_boolean=='0':
                        serv_name.append(k.customer_usr)
                        amt.append(k.amt_offered)
                        ser_amt.append(k.ser_amt_offered)
                        z+=1
                if z==0:                
                    return HttpResponse('no request is pending')
                    
                mylist=zip(serv_name,amt,ser_amt)
                cont={'mylist':mylist,}
            return render(request,'ser_receive_request.html',cont)
                # return render(request,'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
            # return render(request, 'pending_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
        else:
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            data=perfect_service.objects.all()
            for k in data:
                if k.service_usr==service_name and k.service_boolean=='0':
                    serv_name.append(k.customer_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    z+=1
            if z==0:                
                return HttpResponse('no request is pending')
                
            mylist=zip(serv_name,amt,ser_amt)
            cont={'mylist':mylist,}
            return render(request,'ser_receive_request.html',cont) #with a message that please enter right datat
        # return render(request, 'service_logout.html')   #dashboard
    return render(request, 'service_signin.html')


def service_bargin_request(request):
    if service_islogin and Signup_service.objects.filter(username=service_name,token=service_create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            servic_usr=request.POST.get('service_usr')
            bargin_amt=request.POST.get('bargin_amt')
            if perfect_service.objects.filter(customer_usr=servic_usr,service_boolean='0',service_usr=service_name).exists():
                accept=perfect_service.objects.get(customer_usr=servic_usr,service_boolean='0',service_usr=service_name)
                accept.ser_amt_offered=bargin_amt
                accept.save()
                data=perfect_service.objects.all()
                for k in data:
                    if k.service_usr==service_name and k.service_boolean=='0':
                        serv_name.append(k.customer_usr)
                        amt.append(k.amt_offered)
                        ser_amt.append(k.ser_amt_offered)
                        z+=1
                if z==0:                
                    return HttpResponse('no request is pending')
                
                mylist=zip(serv_name,amt,ser_amt)
                cont={'mylist':mylist,}
            return render(request,'ser_receive_request.html',cont)
                # return render(request,'ser_receive_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt})
            # return render(request, 'ser_receive_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt}) #with a message that please enter right datat
        else:
            z=0
            serv_name=[]
            amt=[]
            ser_amt=[]
            data=perfect_service.objects.all()
            for k in data:
                if k.service_usr==service_name and k.service_boolean=='0':
                    serv_name.append(k.customer_usr)
                    amt.append(k.amt_offered)
                    ser_amt.append(k.ser_amt_offered)
                    z+=1
            if z==0:                
                return HttpResponse('no request is pending')
            
            mylist=zip(serv_name,amt,ser_amt)
            cont={'mylist':mylist,}
            return render(request,'ser_receive_request.html',cont)
               #dashboard
            # return render(request, 'ser_receive_request.html',{'service_name':serv_name,'amt':amt,'y':range(z),'ser_amt':ser_amt}) #with a message that please enter right datat
    return render(request, 'service_signin.html')


def service_accepted(request): #to check the accepted request
    if service_islogin and Signup_service.objects.filter(username=service_name,token=service_create_token).exists():#use this feature in all the pages which are view after login to check authnetication
        if request.method=='POST':
            pass
        else:
            m=0
            serv_name=[]
            amt=[]
            accept=perfect_service.objects.all()
            for i in accept:
                if i.service_boolean=='1' and i.service_usr==service_name:
                    serv_name.append(i.customer_usr)
                    amt.append(i.final)
                    m+=1
            if m==0:
                return HttpResponse('no request accepted')
                
            mylist=zip(serv_name,amt)
            cont={'mylist':mylist,}
            return render(request,'ser_accept_request.html',cont)
            # return render(request,'ser_accept_request.html',{'service_name':serv_name,'amt':amt,'y':range(m)})
    return render(request, 'service_signin.html')


