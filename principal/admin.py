from django.contrib import admin
from principal.models import *

class EquipoAdmin(admin.ModelAdmin):
    list_display = ('id','desequipo','puntos','fktorneo')
    list_filter = ('fktorneo',)

class FechaAdmin(admin.ModelAdmin):
    list_display = ('id','desfecha')

class JuegoAdmin(admin.ModelAdmin):
    list_display = ('id','fklocal','fkvisita','fkres','fkfecha','goleslocal','golesvisita')
    list_filter = ('fkfecha',)
    
class JuegoTarjetaAdmin(admin.ModelAdmin):
    list_display = ('id','fktarjeta','fkjuego','fkjugador')
    list_filter = ('fktarjeta','fkjuego','fkjugador')
    
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('id','desjugador','goles','fkequipo')
    list_filter = ('fkequipo',)

class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id','desres')

class TorneoAdmin(admin.ModelAdmin):
    list_display = ('id','destorneo','fkusr')

class TarjetaAdmin(admin.ModelAdmin):
    list_display = ('id','destarjeta')

admin.site.register(juego, JuegoAdmin)
admin.site.register(fecha, FechaAdmin)
admin.site.register(equipo, EquipoAdmin)
admin.site.register(tarjeta, TarjetaAdmin)
admin.site.register(juegotarjeta, JuegoTarjetaAdmin)
admin.site.register(resultado, ResultadoAdmin)
admin.site.register(torneo, TorneoAdmin)
admin.site.register(jugador, JugadorAdmin)
