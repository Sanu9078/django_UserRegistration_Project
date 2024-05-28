from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpRequest
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout,update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from random import randint


# Create your views here.
def register(request):
    EUFO=UserForm()
    EPFO=ProfileForm()
    d={'EUFO':EUFO,'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        UFDO=UserForm(request.POST)
        PFDO=ProfileForm(request.POST,request.FILES)
        if UFDO.is_valid():
            pw=UFDO.cleaned_data.get('password')
            MUFDO=UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            message=f"Hello{UFDO.cleaned_data.get('first_name')} Your Registration sucessfully \n\n Thenk You & Regarding Team"
            email=UFDO.cleaned_data.get('email')
            send_mail(
               'Registration Successfull',
                message,
                'sahoorupak271@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponse ("Registration sucessful")
        return HttpResponse("Invalid Data")        
    return render(request,'register.html',d)

def user_login(request: HttpRequest) -> HttpResponse:
    
    if request.method=='POST':
        username=request.POST.get('un')
        password=request.POST.get('pw')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            return render(request,'home.html',{'user':user})
        else:
            return HttpResponse("Invalid Credantials")
    return render(request,'user_login.html')

@login_required
def user_profile(request):
    try:
        un=request.session['username']
        UO=User.objects.get(username=un)
        d={'UO':UO}
        request.session.modified=True
        return render(request,'user_profile.html',d)
    except:
        return render(request,'user_login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request,'home.html')


def change_password(request):
    if request.method =='POST':
        pw=request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            otp=randint(100000,999999)
            request.session['pw']=pw
            request.session['otp']=otp
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            email=UO.email
            send_mail(
                "OTP for change Password",
                f"OTP of Change Password : {otp}",
                'sahoorupak271@gmail.com',
                [email],
                fail_silently=False
            )
            return render(request,'otp.html')
        return HttpResponse("Password does'n match")
    return render(request,'change_password.html')

def forget_password_username(request):
    if request.method=='POST':
        un=request.POST.get('un')
        request.session['un']=un
        UO=User.objects.get(username=un)
        if UO:
            otp=randint(100000,999999)
            request.session['otp']=otp
            request.session['username']=un
            # un=request.session.get('username')
            # UO=User.objects.get(username=un)
            email=UO.email
            # request.session['email']=email
            send_mail(
            "OTP for Forget Password",
            f"OTP of Forget Password : {otp}",
            'sahoorupak271@gmail.com',
            [email],
            fail_silently=False
            )
            return render(request,'forget_otp.html')
        return HttpResponse("Invalid Username")
    return render(request,'forget_password_username.html')
    

def forget_otp(request):
    if request.method=='POST':
        UOTP=request.POST.get('otp')
        GOTP=request.session.get('otp')
        if UOTP==str(GOTP):
            # pw=request.POST.get('pw')
            # cpw=request.POST.get('cpw')
            # un=request.session.get('username')
            # UO=User.objects.get(username=un)
            # if pw==cpw:
            #     UO.set_password(pw)
            #     UO.save() 
            #     return HttpResponse("Password Change Sucessful")
            # return HttpResponse("") 
            return render(request,'forget_password.html') 
        return HttpResponse("Invalid OTP")       
    return render(request,'forget_otp.html')

def forget_password(request):
    if request.method=='POST':
        pw=request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return render(request,'user_login.html')
        return HttpResponse("Password does't match")    
    return render(request,'forget_password.html')



def otp(request):
    if request.method=='POST':
        UOTP=request.POST.get('otp')
        GOTP=request.session.get('otp')
        if UOTP==str(GOTP):
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            pw=request.session.get('pw')
            UO.set_password(pw)
            UO.save()
            return HttpResponse("Password Change Sucessful")
        return HttpRequest('Invalid OTP')
    return render(request,'otp.html')

def home(request):
    return render(request,'home.html')
        