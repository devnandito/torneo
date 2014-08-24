from django.forms import ModelForm
from django import forms
from principal.models import *

class JuegoForm(ModelForm):
	class Meta:
		model = juego
		fields = ('goleslocal','golesvisita','fkres')

class golesForm(ModelForm):
	class Meta:
		model = jugador
		fields = ('desjugador','goles')

class ContactoForm(forms.Form):
	correo = forms.EmailField(label='Tu correo electronico')
	mensaje = forms.CharField(widget=forms.Textarea)

class JuegoTarjetaForm(ModelForm):
	class Meta:
		model = juegotarjeta
	
#class equipoForm(ModelForm):
#	class Meta:
#		model = equipo
#		field = ('gf','gc')

#class JuegoForm(forms.Form):
#	pkjuego = forms.CharField(max_length=255)
#	goleslocal = forms.CharField(max_length=255)
#	golesvisita = forms.CharField(max_length=255)
