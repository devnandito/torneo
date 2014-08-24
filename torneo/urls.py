from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.index', name='index'),
    url(r'^fixture/$', 'principal.views.viewfixture', name='viewfixture'),
    url(r'^jugadores/$', 'principal.views.viewjugadores', name='viewjugadores'),
    url(r'^amonestados/$', 'principal.views.amonestados', name='amonestados'),
    url(r'^equipos/$', 'principal.views.viewequipos', name='viewequipos'),
    url(r'^ingresar/$', 'principal.views.ingresar', name='ingresar'),
    url(r'^planilla/$', 'principal.views.planilla', name='planilla'),
    url(r'^goleadores/$', 'principal.views.goleadores', name='goleadores'),
    url(r'^jugador/$', 'principal.views.cargarGoles', name='cargarGoles'),
    url(r'^tarjeta/$', 'principal.views.cargarTarjeta', name='cargarTarjeta'),
    url(r'^tarjeta/add$', 'principal.views.addtarjeta', name='addtarjeta'),
    # url(r'^listjugador/$', 'principal.views.jugadorlist', name='jugadorlist'),
    # url(r'^listj/$', 'principal.views.jugadorl', name='jugadorl'),
    url(r'^cerrar/$', 'principal.views.cerrar', name='cerrar'),
    url(r'^contactenos/$', 'principal.views.contactenos', name='contactenos'),
    url(r'^planilla/juego/(?P<id_juego>\d+)/$','principal.views.printplanilla', name='printplanilla'),
    url(r'^jugadordetalle/jugador/(?P<id_jugador>\d+)/$','principal.views.detjugador', name='detjugador'),
    url(r'^equipodetalle/juego/(?P<id_juego>\d+)/local/(?P<id_local>\d+)/visita/(?P<id_visita>\d+)/$','principal.views.detequipo', name='detequipo'),
    # url(r'^app1/', include('app1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
