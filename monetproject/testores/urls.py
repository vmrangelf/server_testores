from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^ajax/obtenerMatriz/$', views.obtenerMatriz, name='obtenerMatriz'),
	url(r'^ajax/operacionPhi/$', views.operacionPhi, name='operacionPhi'),
	url(r'^ajax/calcularMB/$', views.calcularMB, name='calcularMB'),
	url(r'^ajax/obtenerHipergrafoCatalogo/$', views.obtenerHipergrafoCatalogo, name='obtenerHipergrafoCatalogo'),
	url(r'^ajax/obtenerHipergrafoResultante/$', views.obtenerHipergrafoResultante, name='obtenerHipergrafoResultante'),
	# ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
]