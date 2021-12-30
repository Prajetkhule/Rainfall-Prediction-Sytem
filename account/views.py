from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from account.models import AppUsers, Roles
from location.models import Towns

# Create your views here.
def login(request):
    passdata = {}
    if(request.method == 'POST'):
        mobile = request.POST['txtmobile']
        password = request.POST['txtpassword']
        # loginuser = AppUsers.objects.filter(mobile = mobile) & AppUsers.objects.filter(password = password)
        loginuser = AppUsers.objects.filter(Q(mobile = mobile) & Q(password = password))
        # print(str(loginuser.query))
        # print(loginuser.count())
        if(loginuser.count() == 1):
            for user_details in loginuser :
                # print(str(user_details.fullname))
                request.session['fullname'] = user_details.fullname
                request.session['user_id'] = user_details.id
                request.session['role_id'] = user_details.role_id
            # print(type(request.session['role_id']))
            if(request.session["role_id"] == 1):
                return redirect('/admin/')            
            else:
                return redirect('/farmer/')
        else:
            messages.error(request, "Invalid credentials")
    else:
        roles_count = Roles.objects.count()
        if(roles_count < 1):
            roles = Roles()
            roles.name = 'Admin'
            roles.save()
            roles = Roles()
            roles.name = 'Farmer'
            roles.save()

        user_count = AppUsers.objects.count()
        if(user_count < 1):
            appuser = AppUsers()
            appuser.fullname = 'Neha and Pooja'
            appuser.mobile = '9373320550'
            appuser.password = 'pooja@123'
            appuser.role = Roles.objects.get(pk=1)
            appuser.save()
    return render(request, 'accounts/login.html', passdata)

def signup(request):
    if(request.method == 'POST'):
        fullname = request.POST['txtfullname']
        mobile = request.POST['txtrmobile']
        password = request.POST['txtrpassword']
        role = int(request.POST['txtrole'])
        appuser = AppUsers()
        appuser.fullname = fullname.title()
        appuser.mobile = mobile
        appuser.password = password
        appuser.role = Roles.objects.get(pk = role)
        appuser.save()
        messages.success(request, "Signed up successfully. You can login now.")
        return redirect('/')

def logout(request):
    del request.session['fullname']
    del request.session['user_id']
    del request.session['role_id']
    return redirect('/')
