from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from location.models import States, Districts, Tehsils, Towns

# Create your views here.
def regions(request):
    if(request.session.has_key('user_id')):
        if(request.session['role_id'] == 1):
            passData = {}
            passData['fullname'] = request.session['fullname']
            passData['userid'] = request.session['user_id']
            passData['stateslist'] = States.objects.all()
            passData['districtslist'] = Districts.objects.all()
            passData['tehsilslist'] = Tehsils.objects.all()
            passData['townslist'] = Towns.objects.all()
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request,'admin/regions.html',passData)

def states(request):
    if(request.method == 'POST'):
        statename = request.POST['txtstatename']
        state = States()
        state.name = statename.title()
        state.save()
        messages.success(request, f'{statename.title()} added to state list')
        return redirect('regions')