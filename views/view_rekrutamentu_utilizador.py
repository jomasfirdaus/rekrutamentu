from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
# from population.models import Population,DetailFamily,Family,Religion,Profession,Citizen,Aldeia,Village,User,Migration,Death,Migrationout,Temporary,ChangeFamily
# from population.utils import getnewidp,getnewidf
# from population.forms import Family_form,Family_form,FamilyPosition,Population_form,DetailFamily_form,CustumDetailFamily_form,Death_form,Migration_form,Migrationout_form,Changefamily_form
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
# from custom.utils import getnewid, getjustnewid, hash_md5, getlastid
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import date
from django.http import JsonResponse

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from rekrutamentu.forms import FileUploadForm
from rekrutamentu.models import *

from settingapps.utils import  decrypt_id, encrypt_id
from django.core.paginator import Paginator

from django.utils import translation
from django.utils import timezone
from datetime import datetime


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rekrutamentu.forms import JobPostForm

def listavaga(request):
    
    listavaga = JobPost.objects.filter().order_by("id")
    dadoslistavaga = []
    for dados in listavaga.iterator():
        useraplication=UserApplication.objects.exclude(status='Pending').filter(job_post__id=dados.id).count()

        dadoslistavaga.append({'id' : dados.id,'publish_status' : dados.publish_status, 'title' : dados.title, 'deadline' : dados.deadline,'publish_status' : dados.publish_status , 'created_at' : dados.created_at, 'totalaplikante': useraplication})

    context = {
        "listavaga" : dadoslistavaga ,
        "pajina_rekrutamentu" : "active",
            }
    return render(request, 'rekrutamentu/utilizador/lista_vaga.html',context)






def postvaga(request):
    listavaga = JobPost.objects.filter()
    form = JobPostForm()

    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post created successfully.')  # Success message
            return redirect('rekrutamentu:listavaga')
        else:
            messages.error(request, 'There was an error. Please correct the form.')  # Error message
            return redirect('rekrutamentu:postvaga')


    context = {
        "form" : form,
        "pajina_rekrutamentu" : "active",
        "listavaga" : listavaga ,
            }
    return render(request, 'rekrutamentu/utilizador/post_vaga.html',context)



def editvaga(request, id):
    id = decrypt_id(id)
    vaga = JobPost.objects.get(id=id)
    form = JobPostForm(instance=vaga)

    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES,instance=vaga)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post created successfully.')  # Success message
            return redirect('rekrutamentu:listavaga')
        else:
            messages.error(request, 'There was an error. Please correct the form.')  # Error message
            return redirect('rekrutamentu:editvaga')


    context = {
        "form" : form,
        "pajina_rekrutamentu" : "active",
        "listavaga" : listavaga ,
            }
    return render(request, 'rekrutamentu/utilizador/post_vaga.html',context)




def listaplikantereview(request, id):
    idvaga = decrypt_id(id)
    vaga = JobPost.objects.get(id=idvaga)
    lista_aplikante = UserApplication.objects.filter(job_post__id=idvaga, status="Review")
    context = {
        "pajina_rekrutamentu" : "active",
        "vaga" : vaga,
        "tab_review" : "active",
        "id" : id,
        "lista_aplikante" : lista_aplikante ,
        
            }
    return render(request, 'rekrutamentu/utilizador/lista_aplikante.html',context)



def listaplikanteaccepted(request, id):
    idvaga = decrypt_id(id)
    vaga = JobPost.objects.get(id=idvaga)
    lista_aplikante = UserApplication.objects.filter(job_post__id=idvaga,  status="Accepted")
    context = {
        "pajina_rekrutamentu" : "active",
        "tab_accepted" : "active",
        "vaga" : vaga,
        "id" : id,
        "lista_aplikante" : lista_aplikante ,
            }
    return render(request, 'rekrutamentu/utilizador/lista_aplikante.html',context)



def aplikanteaccepted(request, id):
    id = decrypt_id(id)
    lista_aplikante = UserApplication.objects.get(id=id)
    lista_aplikante.status="Accepted"
    lista_aplikante.save()
    return redirect('rekrutamentu:listaplikantereview', id=encrypt_id(lista_aplikante.job_post.id))




def listaplikanterejected(request, id):
    idvaga = decrypt_id(id)
    vaga = JobPost.objects.get(id=idvaga)
    lista_aplikante = UserApplication.objects.filter(job_post__id=idvaga, status="Rejected")
    context = {
        "pajina_rekrutamentu" : "active",
        "tab_rejected" : "active",
        "vaga" : vaga,
        "id" : id,
        "lista_aplikante" : lista_aplikante ,
            }
    return render(request, 'rekrutamentu/utilizador/lista_aplikante.html',context)



def aplikanterejected(request, id):
    id = decrypt_id(id)
    lista_aplikante = UserApplication.objects.get(id=id)
    lista_aplikante.status="Rejected"
    lista_aplikante.save()
    return redirect('rekrutamentu:listaplikantereview', id=encrypt_id(lista_aplikante.job_post.id))





def listadokumentuaplikante(request, id):
    idaplikante = decrypt_id(id)
    dokumentu = UserAttachment.objects.filter(application__id = idaplikante)
    aplikante = UserAttachment.objects.get(application__id = idaplikante)
    print("dados aplikante")
    print(dokumentu)
    context = {
        "pajina_rekrutamentu" : "active",
        "dokumentu" : dokumentu,
        "aplikante" : aplikante,
            }
    return render(request, 'rekrutamentu/utilizador/lista_dokumentu_aplikante.html',context)

def publikavaga(request, id):
    id = decrypt_id(id)
    publikavaga = JobPost.objects.get(id=id)
    publikavaga.publish_status = "Published"
    publikavaga.save()
    messages.success(request, 'Vaga Publika ona ho susesu')  # Error message
    return redirect('rekrutamentu:listavaga')

def unpublikavaga(request, id):
    id = decrypt_id(id)
    publikavaga = JobPost.objects.get(id=id)
    publikavaga.publish_status = "Draft"
    publikavaga.save()
    messages.success(request, 'Vaga Publika ona ho susesu')  # Error message
    return redirect('rekrutamentu:listavaga')





