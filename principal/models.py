
from django.db import models
from django.contrib.auth.models import User

class resultado(models.Model):
	desres = models.CharField(blank=False, max_length=50)
	class Meta:
	    verbose_name = 'Resultado'
	    verbose_name_plural = 'Resultados'
	def __unicode__(self):
		return self.desres

class torneo(models.Model):
	nametorneo = models.CharField(blank=False, max_length=50)
	fkusr = models.ForeignKey(User)
	destorneo = models.CharField(blank=True, max_length=140)
	estado = models.BooleanField(blank=False, default=False)
	class Meta:
	    verbose_name = 'Torneo'
	    verbose_name_plural = 'Torneos'
	def __unicode__(self):
		return self.nametorneo

class equipo(models.Model):
	desequipo = models.CharField(blank=False, max_length=50)
	puntos = models.IntegerField(blank=True, default="0")
	gf = models.IntegerField(blank=False, default="0")
	gc = models.IntegerField(blank=False, default="0")
	pj = models.IntegerField(blank=False, default="0")
	pg = models.IntegerField(blank=False, default="0")
	pe = models.IntegerField(blank=False, default="0")
	pp = models.IntegerField(blank=False, default="0")
	fktorneo = models.ForeignKey(torneo)
	class Meta:
	    verbose_name = 'Equipo'
	    verbose_name_plural = 'Equipos'
	def __unicode__(self):
		return '%s - %s' %(self.desequipo,self.fktorneo)
		
class jugador(models.Model):
	desjugador = models.CharField(blank=False, max_length=50)
	goles = models.IntegerField(blank=False, default="0")
	fkequipo = models.ForeignKey(equipo)
	cedula = models.IntegerField(blank=False)
	representante = models.BooleanField(blank=False, default=False)
	subrepresentante = models.BooleanField(blank=False, default=False)
	capitan = models.BooleanField(blank=False, default=False)
	class Meta:
	    verbose_name = 'Jugador'
	    verbose_name_plural = 'Jugadores'
	def __unicode__(self):
		return "%s - %s" %(self.desjugador, self.fkequipo)
		
class fecha(models.Model):
	desfecha = models.CharField(blank=False, max_length=50)
	class Meta:
	    verbose_name = 'Fecha'
	    verbose_name_plural = 'Fechas'
	def __unicode__(self):
		return self.desfecha

class juego(models.Model):
	fklocal = models.ForeignKey(equipo, related_name='+')
	fkvisita = models.ForeignKey(equipo, related_name='+')
	fkres = models.ForeignKey(resultado)
	fkfecha = models.ForeignKey(fecha)
	goleslocal = models.IntegerField(blank=False, default="0")
	golesvisita = models.IntegerField(blank=False, default="0")
	class Meta:
	    verbose_name = 'Juego'
	    verbose_name_plural = 'Juegos'
	def __unicode__(self):
		return '%s - %s vs %s' %(self.fkfecha, self.fklocal, self.fkvisita)
		
class tarjeta(models.Model):
	destarjeta = models.CharField(blank=False, max_length=50)
	tarjetas = models.ManyToManyField(jugador, through='juegotarjeta')
	class Meta:
	    verbose_name = 'Tarjeta'
	    verbose_name_plural = 'Tarjetas'
	def __unicode__(self):
		return self.destarjeta

class juegotarjeta(models.Model):
	fktarjeta = models.ForeignKey(tarjeta)
	fkjuego = models.ForeignKey(juego)
	fkjugador = models.ForeignKey(jugador)
	class Meta:
	    verbose_name = 'JuegoTarjeta'
	    verbose_name_plural = 'JuegosTarjetas'
	def __unicode__(self):
		return '%s %s %s' %(self.fktarjeta, self.fkjuego, self.fkjugador)

