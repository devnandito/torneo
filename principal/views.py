from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from datetime import datetime
from principal.forms import *
from django.template.context import RequestContext
from principal.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core import serializers
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.sessions.middleware import SessionMiddleware

#Vista tabla de posiciones
def index(request):	
    #equipos = equipo.objects.values('desequipo','puntos','gf','gc').order_by('-puntos','-gf','gc')
    torneos = torneo.objects.filter(estado=True)
    equipos = equipo.objects.filter(fktorneo__estado__exact=True).order_by('-puntos','-gf','gc')
    return render_to_response('viewtablas.html', context_instance=RequestContext(request,{'equipos':equipos, 'torneos':torneos}))
    
#Vista fixture
def viewfixture(request):
	torneos = torneo.objects.filter(estado=True)
	#fixture = juego.objects.all().order_by('fkfecha')
	fixture = juego.objects.filter(fklocal__fktorneo__estado__exact=True).order_by('fkfecha')
	return render_to_response('fixture.html', context_instance=RequestContext(request,{'fixture':fixture, 'torneos':torneos}))
	
#Vista de los jugadores
def viewjugadores(request):
	jugadores = jugador.objects.exclude(goles=0).order_by('-goles','fkequipo','desjugador').filter(fkequipo__fktorneo__estado__exact=True)
	torneos = torneo.objects.filter(estado=True)
	return render_to_response('viewjugadores.html', context_instance=RequestContext(request,{'jugadores':jugadores, 'torneos': torneos}))

#Vista de los goleadores
def goleadores(request):
	jugadores = jugador.objects.exclude(goles=0).order_by('-goles','fkequipo','desjugador').filter(fkequipo__fktorneo__estado__exact=True)
	torneos = torneo.objects.filter(estado=True)
	return render_to_response('printgoleadores.html', context_instance=RequestContext(request,{'jugadores':jugadores, 'torneos': torneos}))

#Vista de los equipos
@login_required(login_url='/ingresar')
def viewequipos(request):
	juego_list = juego.objects.filter(fklocal__fktorneo__estado__exact=True).order_by('fkfecha')
	torneos = torneo.objects.filter(estado=True)
	usuario = request.user
	#juego_list = juego.objects.values().order_by('id')
	return render_to_response('viewequipos.html', context_instance=RequestContext(request,{'juego_list':juego_list, 'usuario':usuario, 'torneos':torneos}))

#Vista amonestados
def amonestados(request):
	#b = juego.objects.exclude(id=0)
	#tarjetas = b.juegotarjeta_set.all()
	torneos = torneo.objects.filter(estado=True)
	tarjetas = juegotarjeta.objects.filter(fkjugador__fkequipo__fktorneo__estado__exact=True).order_by('-fkjuego')
	return render_to_response('viewamonestados.html', context_instance=RequestContext(request,{'tarjetas':tarjetas, 'torneos':torneos}))

#Vista contactenos
def contactenos(request):
	torneos = torneo.objects.filter(estado=True)
	if request.method=='POST':
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mesaje del Torneo SSEE'
			contenido = formulario.cleaned_data['mensaje']+"\n"
			contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['fhersa@gmail.com'])
			correo.send()
			return HttpResponseRedirect('/')
	else:
		formulario = ContactoForm()
	return render_to_response('contactenos.html',{'formulario':formulario, 'torneos':torneos}, context_instance=RequestContext(request))

#def contactenos(request):
#	contactenos = 'fhersa@gmail.com'
#	return render_to_response('contactenos.html', context_instance=RequestContext(request, {'contactenos':contactenos}))

#Vista parametros para ver un equipo
@login_required(login_url='/ingresar')
def detequipo(request, id_juego, id_local, id_visita):
	usuario = request.user
	torneos = torneo.objects.filter(estado=True)
	if request.method == 'POST':
		a = get_object_or_404(juego, pk=id_juego)
		goleslocal = request.POST['goleslocal']
		golesvisita = request.POST['golesvisita']
		el = equipo.objects.get(pk=id_local)
		el.gf = F('gf') + goleslocal
		el.gc = F('gc') + golesvisita
		ev = equipo.objects.get(pk=id_visita)
		ev.gf = F('gf') + golesvisita
		ev.gc = F('gc') + goleslocal
		el.pj = F('pj') + 1
		ev.pj = F('pj') + 1
		if goleslocal > golesvisita:
			el.puntos = F('puntos') + 3
			el.pg = F('pg') + 1
			ev.pp = F('pp') + 1
		elif golesvisita > goleslocal:
			ev.puntos = F('puntos') + 3
			ev.pg = F('pg') + 1
			el.pp = F('pp') + 1
		else:
			el.puntos = F('puntos') + 1
			ev.puntos = F('puntos') + 1
			el.pe = F('pe') + 1
			ev.pe = F('pe') + 1
		form = JuegoForm(request.POST, instance=a)
		if form.is_valid():
			form.save()
			el.save()
			ev.save()
			return HttpResponseRedirect('/equipos')
	else:
		b = juego.objects.get(pk=id_juego)
		form = JuegoForm(instance=b)
		juegos = juego.objects.get(pk=id_juego)
	return render_to_response('formequipos.html', context_instance=RequestContext(request,{'form':form, 'usuario':usuario, 'juegos':juegos, 'torneos':torneos}))

#Vista para login_required
def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/equipos')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			pwd = request.POST['password']
			acceso = authenticate(username=usuario, password=pwd)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/equipos')
				else:
					#return render_to_response('noactivo.html', context_instance=RequestContext(request))
					return render_to_response('noactivo.html', {'error':True, 'formulario':formulario}, context_instance=RequestContext(request))
			else:
				#return render_to_response('nousuario.html', context_instance=RequestContext(request))
				return render_to_response('nousuario.html', {'error':True, 'formulario':formulario}, context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

#Vista cerra session
@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/ingresar')

#Vista carga de goles
@login_required(login_url='/ingresar')
def cargarGoles(request):
    jugador_list = jugador.objects.filter(fkequipo__fktorneo__estado__exact=True).order_by('-goles','fkequipo','desjugador')
    torneos = torneo.objects.filter(estado=True)
    paginator = Paginator(jugador_list,20)
    usuario = request.user
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        jugadores = paginator.page(page)
    except (EmptyPage, InvalidPage):
        jugadores = paginator.page(paginator.num_pages)
    return render_to_response('viewjugador.html', context_instance=RequestContext(request,{'jugadores':jugadores, 'usuario':usuario, 'torneos':torneos}))

#Vista carga de goles
@login_required(login_url='/ingresar')
def cargarTarjeta(request):
    tarjeta_list = juegotarjeta.objects.filter(fkjugador__fkequipo__fktorneo__estado__exact=True).order_by('-fkjuego')
    torneos = torneo.objects.filter(estado=True)
    paginator = Paginator(tarjeta_list,20)
    usuario = request.user
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        tarjetas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tarjetas = paginator.page(paginator.num_pages)
    return render_to_response('viewtarjeta.html', context_instance=RequestContext(request,{'tarjetas':tarjetas, 'usuario':usuario, 'torneos':torneos}))
    
#Vista form tarjetas
@login_required(login_url='/ingresar')
def addtarjeta(request):
	torneos = torneo.objects.filter(estado=True)
	usuario = request.user
	if request.method=='POST':
		form = JuegoTarjetaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/tarjeta')
	else:
		form = JuegoTarjetaForm()
	return render_to_response('formtarjeta.html',{'usuario':usuario, 'form':form, 'torneos':torneos}, context_instance=RequestContext(request))

#vista detalle jugador
@login_required(login_url='/ingresar')
def detjugador(request, id_jugador):
	torneos = torneo.objects.filter(estado=True)
	usuario = request.user
	if request.method == 'POST':
		a = get_object_or_404(jugador, pk=id_jugador)
		formjugador = golesForm(request.POST, instance=a)
		if formjugador.is_valid():
			formjugador.save()
			return HttpResponseRedirect('/jugador')
	else:
		#b = jugador.objects.filter(pk=id_jugador, fkequipo__fktorneo__estado__exact=True)
		b = jugador.objects.get(pk=id_jugador)
		formjugador = golesForm(instance=b)
	return render_to_response('formgoles.html', context_instance=RequestContext(request, {'formjugador':formjugador, 'usuario':usuario, 'torneos':torneos}))

#Vista para generar la planilla
@login_required(login_url='/ingresar')
def planilla(request):
	usuario = request.user
	torneos = torneo.objects.filter(estado=True)
	juegos = juego.objects.filter(fklocal__fktorneo__estado__exact=True).order_by('fkfecha')
	return render_to_response('planilla.html',{'juegos':juegos,'usuario':usuario, 'torneos':torneos}, context_instance=RequestContext(request))

#Vista para imprimir la planilla
@login_required(login_url='/ingresar')    
def printplanilla(request, id_juego):
	usuario = request.user
	torneos = torneo.objects.filter(estado=True)
	planilla = juego.objects.get(id=id_juego)
	jugadorlocal = jugador.objects.filter(fkequipo=planilla.fklocal)
	rl = jugador.objects.filter(fkequipo=planilla.fklocal, representante=True)
	srl = jugador.objects.filter(fkequipo=planilla.fklocal, subrepresentante=True)
	jugadorvisita = jugador.objects.filter(fkequipo=planilla.fkvisita)
	rv = jugador.objects.filter(fkequipo=planilla.fkvisita, representante=True)
	srv = jugador.objects.filter(fkequipo=planilla.fkvisita, subrepresentante=True)
	return render_to_response('printplanilla.html',{'planilla':planilla, 'jugadorlocal':jugadorlocal, 'jugadorvisita':jugadorvisita,'rl':rl,'srl':srl,'rv':rv,'srv':srv,'usuario':usuario, 'torneos': torneos}, context_instance=RequestContext(request))

#Vista para paginar con un templatag
# def jugadorlist(request):
# 	if request.POST:
# 		desjugador = request.POST['desjugador']
# 		request.session['desjugador'] = desjugador
# 	else:
# 		name_jugador = request.session['desjugador']
# 		queryset = jugador.objects.filter(desjugador__icontains=desjugador).order_by('desjugador')
# 	return object_list(request, queryset, tamplate_name='jugadorlist.html', paginate_by=35, allow_empty=True)

# def jugadorl(request):
# 	page_obj = jugador.objects.all().order_by('desjugador')
# 	paginator = 3
# 	return render_to_response('listj.html', {'page_obj':page_obj, 'paginator':paginator})


#LIST_HEADERS 
#(
#	('PK','id') ('Judador','desjugador'),('Goles','goles')
#)
#def sorting(request):
#	sort_headers = SortHeaders(reques, LIST_HEADERS)
#	jugadores = jugador.objects.all().order_by(sort_headers.get_order_by())






	
#Vista pagina admin
#@login_required(login_url='/ingresar')
#def privado(request):
#	usuario = request.user
#	return render_to_response('privado.html',{'usuario':usuario}, context_instance=RequestContext(request))

#Vista formulario actualizacion de equipos
#def updateJuego(request):
#	if request.method == 'POST':
#		a = juego.objects.get(pk=1)
#		form = JuegoForm(request.POST, instance=a)
#		if form.is_valid():
#			form.save()
#			return HttpResponseRedirect('/fixture')
#	else:
#		form = JuegoForm()
#	return render_to_response('formequipos.html', context_instance=RequestContext(request,{'form':form}))

#def index(request):	
#    equipo_list = equipo.objects.all().order_by('-puntos')
#    paginator = Paginator(equipo_list,6)
#    try:
#        page = int(request.GET.get('page','1'))
#    except ValueError:
#        page = 1
#    try:
#        equipos = paginator.page(page)
#    except (EmptyPage, InvalidPage):
#        juegos = paginator.page(paginator.num_pages)
#    return render_to_response('viewequipos.html', context_instance=RequestContext(request,{'equipos':equipos}))
