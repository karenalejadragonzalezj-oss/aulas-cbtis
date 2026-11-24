from django.db import models

class Aula(models.Model):
	TIPOS = [
		("AULA", "Aula"),
		("ESPECIAL", "Laboratorio / taller / cómputo"),
		("FUERA", "Fuera de aula"),
	]
	nombre = models.CharField(max_length=40, unique=True)
	tipo = models.CharField(max_length=10, choices=TIPOS, default="AULA")

	def __str__(self):
		return self.nombre


class Grupo(models.Model):
	nombre = models.CharField(max_length=40, unique=True)
	semestre = models.PositiveSmallIntegerField()
	especialidad = models.CharField(max_length=80)
	turno = models.CharField(max_length=12)
	aula_fija = models.ForeignKey(
		Aula, null=True, on_delete=models.PROTECT, related_name="grupos"
	)

	def __str__(self):
		return self.nombre


class Bloque(models.Model):
	DIAS = [
		(0, "Lunes"),
		(1, "Martes"),
		(2, "Miércoles"),
		(3, "Jueves"),
		(4, "Viernes"),
	]
	grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="bloques")
	aula = models.ForeignKey(Aula, on_delete=models.PROTECT, related_name="bloques")
	dia = models.PositiveSmallIntegerField(choices=DIAS)
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	materia = models.CharField(max_length=200)

	class Meta:
		ordering = ["grupo", "dia", "hora_inicio"]
		indexes = [models.Index(fields=["aula", "dia", "hora_inicio"])]

	def __str__(self):
		return (
			f"{self.grupo} · {self.get_dia_display()} "
			f"{self.hora_inicio:%H:%M} · {self.aula}"
		)
