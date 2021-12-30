from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages
from account.models import AppUsers
import csv
import os
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

# Create your views here.
def index(request):
    passData = {}
    if(request.session.has_key('user_id')):
        if(request.session['role_id'] == 2):
            passData['fullname'] = request.session['fullname']
            passData['userid'] = request.session['user_id']
        else:
            raise PermissionDenied()
    else:
        return redirect('/')
    return render(request, 'farmer/index.html', passData)