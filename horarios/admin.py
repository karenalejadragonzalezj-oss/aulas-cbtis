from django.contrib import admin
from .models import Aula, Grupo, Bloque


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
	list_display = ("nombre", "tipo")


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
	list_display = ("nombre", "semestre", "especialidad", "turno", "aula_fija")
	list_filter = ("semestre", "turno")


@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
	list_display = ("grupo", "aula", "dia", "hora_inicio", "hora_fin", "materia")
	list_filter = ("dia", "aula", "grupo__turno")
