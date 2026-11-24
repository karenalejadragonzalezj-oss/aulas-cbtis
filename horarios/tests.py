from datetime import date, time
from unittest.mock import patch

from django.test import TestCase

from .models import Aula, Bloque, Grupo


class CrucesDelDiaTests(TestCase):
	def setUp(self):
		self.aula = Aula.objects.create(nombre="A-1")
		self.grupo_uno = Grupo.objects.create(
			nombre="1A", semestre=1, especialidad="Programación",
			turno="Matutino", aula_fija=self.aula,
		)
		self.grupo_dos = Grupo.objects.create(
			nombre="1B", semestre=1, especialidad="Programación",
			turno="Matutino", aula_fija=self.aula,
		)

	def crear_bloques_que_se_cruzan(self, dia):
		for grupo in (self.grupo_uno, self.grupo_dos):
			Bloque.objects.create(
				grupo=grupo, aula=self.aula, dia=dia,
				hora_inicio=time(8, 0), hora_fin=time(9, 0), materia="Matemáticas",
			)

	@patch("horarios.views.timezone.localdate", return_value=date(2026, 11, 19))
	def test_muestra_solo_los_cruces_del_dia_actual(self, _localdate):
		self.crear_bloques_que_se_cruzan(3)  # Jueves
		self.crear_bloques_que_se_cruzan(4)  # Viernes

		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["choques_count"], 1)
		self.assertEqual(response.context["choques"][0][0].dia, 3)

	@patch("horarios.views.timezone.localdate", return_value=date(2026, 11, 21))
	def test_no_muestra_cruces_en_fin_de_semana(self, _localdate):
		self.crear_bloques_que_se_cruzan(4)  # Viernes

		response = self.client.get("/")

		self.assertEqual(response.context["choques_count"], 0)
