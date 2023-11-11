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

from settingapps.utils import  decrypt_id
from django.core.paginator import Paginator

from django.utils import translation
from django.utils import timezone
from datetime import datetime


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    vaga = JobPost.objects.filter(publish_status='Published', deadline__gte=datetime.now())
    apply = UserApplication.objects.filter(user = request.user.id)


    context = {
        "vaga" : vaga ,
        'totalapply' : apply.count(),
            }
    return render(request, 'rekrutamentu/vizitor/index.html',context)


def logoutgmail(request):
    logout(request)
    return redirect('rekrutamentu:index')

def detallu(request, id):
    encrypted_job_post_id = id
    id = decrypt_id(id)
    print(str(id))
    
    vaga = JobPost.objects.get(id = int(id))
    print(vaga)
    dadosaplly = "mamuk"
    useraplication = "mamuk" 
    form = FileUploadForm()


    context = {
        'form': form, 
        "vaga" : vaga,
        'dadosaplly' : dadosaplly,
    }

    if request.user.is_authenticated:

        useraplication = UserApplication.objects.filter(job_post=int(id), user = request.user.id).last()
        dadosaplly = UserApplication.objects.filter(job_post=int(id), user = request.user.id).last()
        if dadosaplly : 
            dadosaplly = UserAttachment.objects.filter(application = dadosaplly)
            if dadosaplly.count()  == 0  :
                dadosaplly ="mamuk"
                
        


       
        context = {
            'encrypted_job_post_id' : encrypted_job_post_id,
            'dadosaplly' : dadosaplly ,
            'useraplication' : useraplication,
            'form': form, 
            "vaga" : vaga,
        }

    return render(request, 'rekrutamentu/vizitor/detallu.html',context)



@csrf_exempt
def ajax_uploaddokumentu(request):
    response_data = {}

    # Get the encrypted job_post ID from the POST data
    encrypted_job_post_id = request.POST.get("job_post")

    # Decrypt the job_post ID
    job_post_id = decrypt_id(encrypted_job_post_id)

    # Find the corresponding JobPost object
    job_post = get_object_or_404(JobPost, id=int(job_post_id))
    user = get_object_or_404(User, id=request.user.id)

    # Check if a UserApplication already exists for the given user and job_post
    user_application = UserApplication.objects.filter(job_post=job_post, user=user).first()

    if user_application:
        useraplication = user_application
        # If a UserApplication already exists, use it
        user_application.status = "Pending"
        user_application.save()
        user_attachment = UserAttachment(application=user_application, upload_file=request.FILES['upload_file'])
        user_attachment.save()
    else:
        # If a UserApplication does not exist, create a new one
        user_application = UserApplication(job_post=job_post, user=user, status="Pending")
        user_application.save()
        user_attachment = UserAttachment(application=user_application, upload_file=request.FILES['upload_file'])
        user_attachment.save()
        print(user_attachment.id)

    # After saving UserAttachment, generate an HTML response
    user_attachments = UserAttachment.objects.filter(application=user_application)

    # Generate HTML content using a template


    context = {
        'encrypted_job_post_id' : encrypted_job_post_id,
        'dadosaplly': user_attachments, 
        'useraplication' : useraplication,
    }
    return render(request, 'rekrutamentu/vizitor/lista_dokumentuupload.html',context)

def apllyavaga(request,id):
    idvaga = decrypt_id(id)
    applyvaga = UserApplication.objects.get(job_post__id=idvaga,user__id = request.user.id)
    applyvaga.status = "Review"
    applyvaga.save()
    messages.success(request, 'Vaga aplly ona ho susesu')  # Error message
    return redirect('rekrutamentu:detallu',id=id)


    # Retrieve the uploaded file from the request
    # uploaded_file = request.FILES.get('upload_file')

    # if uploaded_file:
    #     # Assuming you have a UserApplication ID as 'application_id'
    #     application_id = request.POST.get('application_id')

    #     # Create a new UserAttachment
    #     user_attachment = UserAttachment(
    #         application_id=application_id,
    #         upload_file=uploaded_file
    #     )
    #     user_attachment.save()

    #     return JsonResponse({'success': True, 'attachment_id': user_attachment.id})
    # else:
    #     return JsonResponse({'success': False, 'message': 'No file was provided.'})


def attachments(request, file_url):
  
    return HttpResponseRedirect(decrypt_id(file_url))