from django.urls import path 

from rekrutamentu import views


app_name = "rekrutamentu"





urlpatterns = [
	path('', views.index, name='index'),
	path('logout/gmail', views.logoutgmail, name='logoutgmail'),
	path('detallu/<str:id>', views.detallu, name='detallu'),
    path('upload/dokumentu', views.ajax_uploaddokumentu, name='ajax_uploaddokumentu'),
    path('attachments/<str:file_url>', views.attachments, name='attachments'),

	
    path('lista/vaga', views.listavaga, name='listavaga'),
    path('postvaga', views.postvaga, name='postvaga'),
    path('publika/vaga/<str:id>', views.publikavaga, name='publikavaga'),
    path('unpublika/vaga/<str:id>', views.unpublikavaga, name='unpublikavaga'),
    path('edit/vaga/<str:id>', views.editvaga, name='editvaga'),


    path('list/aplikante/review/<str:id>', views.listaplikantereview, name='listaplikantereview'),
    path('list/aplikante/accepted/<str:id>', views.listaplikanteaccepted, name='listaplikanteaccepted'),
    path('list/aplikante/rejected/<str:id>', views.listaplikanterejected, name='listaplikanterejected'),

    path('apply/vaga/<str:id>', views.apllyavaga, name='apllyavaga'),

    path('lista/dokumentu/aplikante/<str:id>', views.listadokumentuaplikante, name='listadokumentuaplikante'),

    path('aplikante/accepted/<str:id>', views.aplikanteaccepted, name='aplikanteaccepted'),
    path('aplikante/rejected/<str:id>', views.aplikanterejected, name='aplikanterejected')

	
	
]

