from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages
import csv
import os
from sklearn.linear_model import LinearRegression
import joblib
import pandas as pd
import numpy as np
from rainfall.models import RainfallDataset
from location.models import States
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
def rain_dataset(request):
    passData = {}
    if(request.session.has_key('user_id')):
        if(request.session['role_id'] == 1):
            passData['fullname'] = request.session['fullname']
            passData['userid'] = request.session['user_id']
            passData['states'] = States.objects.all().order_by('name')
            passData['dataset'] = RainfallDataset.objects.all().order_by('state', 'year')
            now = datetime.now()
            pre_year = now.year - 1
            passData['maxyear'] = pre_year
            if(request.method == 'POST'):
                rain = RainfallDataset()
                rain.state = States.objects.get(pk = int(request.POST['txtstate']))
                rain.annual = float(request.POST['txtannual'])
                rain.year = float(request.POST['txtyear'])
                rain.jf = float(request.POST['txtjf'])
                rain.mam = float(request.POST['txtmam'])
                rain.jjas = float(request.POST['txtjjas'])
                rain.ond = float(request.POST['txtond'])
                rain.save()
                messages.success(request,'Record added in database.')
                return redirect('/rainfall/rain_dataset')
        else:
            raise PermissionDenied()
    else:
        return redirect('/')
    return render(request, 'admin/rainfall.html', passData)

def rain_export_to_csv(request):
    if(request.method == 'POST'):
        dataset = RainfallDataset.objects.all().order_by('state', 'year')
        with open(os.path.join(BASE_DIR,'datasets/rainfall_dataset.csv'), 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['state', 'year', 'annual', 'jf', 'mam', 'jjas', 'ond'])
            for data in dataset:
                csv_writer.writerow([data.state_id, data.year, data.annual, data.jf, data.mam, data.jjas, data.ond])

        # Read csv file
        df=pd.read_csv(os.path.join(BASE_DIR,'datasets/rainfall_dataset.csv'))
        reg = LinearRegression()
        # Annual model
        reg.fit(df[['state', 'year']], df.annual)
        joblib.dump(reg,os.path.join(BASE_DIR,'datasets/rainfall_model_annual.pkl'))
        # JF model
        reg.fit(df[['state', 'year']], df.jf)
        joblib.dump(reg,os.path.join(BASE_DIR,'datasets/rainfall_model_jf.pkl'))
        # MAM model
        reg.fit(df[['state', 'year']], df.mam)
        joblib.dump(reg,os.path.join(BASE_DIR,'datasets/rainfall_model_mam.pkl'))
        # JJAS model
        reg.fit(df[['state', 'year']], df.jjas)
        joblib.dump(reg,os.path.join(BASE_DIR,'datasets/rainfall_model_jjas.pkl'))
        # OND model
        reg.fit(df[['state', 'year']], df.ond)
        joblib.dump(reg,os.path.join(BASE_DIR,'datasets/rainfall_model_ond.pkl'))
        messages.success(request, 'Rainfall Dataset CSV modified.')
    return redirect('/rainfall/rain_dataset')

def rain_predict(request):
    passData = {}
    if(request.session.has_key('user_id')):
        if(request.session['role_id'] == 2):
            passData['fullname'] = request.session['fullname']
            passData['userid'] = request.session['user_id']
            passData['states'] = States.objects.all().order_by('name')
            if(request.method == 'POST'):
                state = int(request.POST['txtstate'])
                return redirect('rainfall_data', pk = state)
        else:
            raise PermissionDenied()
    else:
        return redirect('/')
    return render(request, 'farmer/rainfall.html', passData)

def rainfall_data(request, pk):
    passData = {}
    if(request.session.has_key('user_id')):
        if(request.session['role_id'] == 2):
            passData['fullname'] = request.session['fullname']
            passData['userid'] = request.session['user_id']
            passData['states'] = States.objects.all().order_by('name')
            state = pk

            statename = States.objects.get(id = state)
            passData['statename'] = statename.name

            now = datetime.now()
            current_year = now.year
            # Predict annual rainfall for current year
            joblib_annual = joblib.load(os.path.join(BASE_DIR,'datasets/rainfall_model_annual.pkl'))
            pred_annual = joblib_annual.predict([[state, current_year]])

            # Predict jf rainfall for current year
            joblib_jf = joblib.load(os.path.join(BASE_DIR,'datasets/rainfall_model_jf.pkl'))
            pred_jf = joblib_jf.predict([[state, current_year]])

            # Predict mam rainfall for current year
            joblib_mam = joblib.load(os.path.join(BASE_DIR,'datasets/rainfall_model_mam.pkl'))
            pred_mam = joblib_mam.predict([[state, current_year]])

            # Predict jjas rainfall for current year
            joblib_jjas = joblib.load(os.path.join(BASE_DIR,'datasets/rainfall_model_jjas.pkl'))
            pred_jjas = joblib_jjas.predict([[state, current_year]])

            # Predict ond rainfall for current year
            joblib_ond = joblib.load(os.path.join(BASE_DIR,'datasets/rainfall_model_ond.pkl'))
            pred_ond = joblib_ond.predict([[state, current_year]])

            passData['annual'] = f'Predicted annual rainfall for <strong>{current_year}</strong> will be <strong>{pred_annual}</strong>.'
            passData['JF'] = f'Predicted JF rainfall for <strong>{current_year}</strong> will be <strong>{pred_jf}</strong>.'
            passData['MAM'] = f'Predicted MAM rainfall for <strong>{current_year}</strong> will be <strong>{pred_mam}</strong>.'
            passData['JJAS'] = f'Predicted JJAS rainfall for <strong>{current_year}</strong> will be <strong>{pred_jjas}</strong>.'
            passData['OND'] = f'Predicted OND rainfall for <strong>{current_year}</strong> will be <strong>{pred_ond}</strong>.'
        else:
            raise PermissionDenied()
    else:
        return redirect('/')
    return render(request, 'farmer/p_rainfall.html', passData)
