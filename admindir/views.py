from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages
import os


# Create your views here.
def index(request):
    passData = {}
    if(request.session.has_key('user_id')):
        if(request.session['role_id'] == 1):
            passData['fullname'] = request.session['fullname']
            passData['userid'] = request.session['user_id']
        else:
            raise PermissionDenied()
    else:
        return redirect('/')
    return render(request, 'admin/index.html', passData)