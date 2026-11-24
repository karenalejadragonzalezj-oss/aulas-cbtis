from collections import defaultdict
from datetime import date, datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from openpyxl import Workbook
from openpyxl.styles import Font

from .models import Aula, Bloque, Grupo


def inicio(request):
	grupos = Grupo.objects.order_by("semestre", "nombre")
	aulas = Aula.objects.order_by("nombre")
	bloques = Bloque.objects.select_related("grupo", "aula").order_by(
		"dia", "hora_inicio", "aula__nombre", "grupo__nombre"
	)

	busqueda = request.GET.get("q", "").strip()
	grupo_id = request.GET.get("grupo", "")
	aula_id = request.GET.get("aula", "")
	dia = request.GET.get("dia", "")

	if busqueda:
		bloques = bloques.filter(
			Q(grupo__nombre__icontains=busqueda)
			| Q(aula__nombre__icontains=busqueda)
			| Q(materia__icontains=busqueda)
		)
	if grupo_id.isdigit():
		bloques = bloques.filter(grupo_id=grupo_id)
	else:
		grupo_id = ""
	if aula_id.isdigit():
		bloques = bloques.filter(aula_id=aula_id)
	else:
		aula_id = ""
	if dia in {"0", "1", "2", "3", "4"}:
		bloques = bloques.filter(dia=int(dia))
	else:
		dia = ""

	hoy = timezone.localdate()
	dia_actual = hoy.weekday()
	bloques_hoy = Bloque.objects.select_related("grupo", "aula")
	if dia_actual in range(5):
		bloques_hoy = bloques_hoy.filter(dia=dia_actual)
	else:
		bloques_hoy = bloques_hoy.none()

	ocupaciones = defaultdict(list)
	for bloque in bloques_hoy:
		ocupaciones[(bloque.aula_id, bloque.dia)].append(bloque)

	choques = []
	for lista in ocupaciones.values():
		lista.sort(key=lambda b: (b.hora_inicio, b.hora_fin))
		for indice, primero in enumerate(lista):
			for segundo in lista[indice + 1 :]:
				if segundo.hora_inicio >= primero.hora_fin:
					break
				if primero.hora_inicio < segundo.hora_fin:
					choques.append((primero, segundo))

	# Paginación
	pagina = request.GET.get("page", 1)
	paginator = Paginator(bloques, 25) # 25 bloques por página
	bloques_pagina = paginator.get_page(pagina)

	return render(
		request,
		"horarios/inicio.html",
		{
			"grupos": grupos,
			"aulas": aulas,
			"bloques": bloques_pagina,
			"page_obj": bloques_pagina,
			"bloques_count": bloques.count(),
			"aulas_count": aulas.count(),
			"grupos_count": grupos.count(),
			"choques": choques[:12],
			"choques_count": len(choques),
			"hoy": hoy,
			"busqueda": busqueda,
			"grupo_seleccionado": grupo_id,
			"aula_seleccionada": aula_id,
			"dia_seleccionado": dia,
			"dias": Bloque.DIAS,
		},
	)


def detalle_grupo(request, grupo_id):
	grupo = get_object_or_404(Grupo, id=grupo_id)
	bloques = list(Bloque.objects.filter(grupo=grupo).select_related("aula").order_by(
		"dia", "hora_inicio"
	))
	dias = []
	for numero, nombre in Bloque.DIAS:
		dias.append(
			{
				"nombre": nombre,
				"bloques": [bloque for bloque in bloques if bloque.dia == numero],
			}
		)

	vista = request.GET.get("vista", "lista")
	if vista not in {"lista", "tabla"}:
		vista = "lista"

	horario_grid = []
	if bloques:
		marcas = sorted({hora for bloque in bloques for hora in (bloque.hora_inicio, bloque.hora_fin)})
		intervalos = list(zip(marcas, marcas[1:]))
		por_dia = {
			numero: [bloque for bloque in bloques if bloque.dia == numero]
			for numero, _ in Bloque.DIAS
		}
		celdas_por_dia = {}
		for numero, _ in Bloque.DIAS:
			celdas = [{"tipo": "libre", "rowspan": 1} for _ in intervalos]
			for bloque in por_dia[numero]:
				inicio = marcas.index(bloque.hora_inicio)
				fin = marcas.index(bloque.hora_fin)
				celdas[inicio] = {"tipo": "clase", "bloque": bloque, "rowspan": fin - inicio}
				for indice in range(inicio + 1, fin):
					celdas[indice] = None
			celdas_por_dia[numero] = celdas

		for indice, (inicio, fin) in enumerate(intervalos):
			ocupado = any(
				bloque.hora_inicio <= inicio and bloque.hora_fin >= fin
				for bloque in bloques
			)
			minutos = int((datetime.combine(date.min, fin) - datetime.combine(date.min, inicio)).total_seconds() // 60)
			descanso = not ocupado and minutos >= 20
			horario_grid.append({
				"inicio": inicio,
				"fin": fin,
				"descanso": descanso,
				"celdas": [celdas_por_dia[numero][indice] for numero, _ in Bloque.DIAS],
			})

	return render(
		request,
		"horarios/grupo.html",
		{
			"grupo": grupo,
			"dias": dias,
			"dias_semana": Bloque.DIAS,
			"bloques_count": len(bloques),
			"vista": vista,
			"horario_grid": horario_grid,
		},
	)


def exportar_excel(request):
	bloques = Bloque.objects.select_related("grupo", "aula").order_by(
		"grupo__nombre", "dia", "hora_inicio"
	)

	workbook = Workbook()
	hoja = workbook.active
	hoja.title = "Horarios"
	hoja.append(
		[
			"Grupo",
			"Semestre",
			"Especialidad",
			"Turno",
			"Aula",
			"Día",
			"Hora inicio",
			"Hora fin",
			"Materia",
		]
	)

	for bloque in bloques:
		hoja.append(
			[
				bloque.grupo.nombre,
				bloque.grupo.semestre,
				bloque.grupo.especialidad,
				bloque.grupo.turno,
				bloque.aula.nombre,
				bloque.get_dia_display(),
				bloque.hora_inicio.strftime("%H:%M"),
				bloque.hora_fin.strftime("%H:%M"),
				bloque.materia,
			]
		)

	for columna in hoja.columns:
		columna[0].font = Font(bold=True)
	hoja.freeze_panes = "A2"
	hoja.auto_filter.ref = hoja.dimensions

	respuesta = HttpResponse(
		content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
	)
	respuesta["Content-Disposition"] = 'attachment; filename="horarios_cbtis234.xlsx"'
	workbook.save(respuesta)
	return respuesta


def ocupacion(request):
	try:
		dia = int(request.GET.get("dia", 0))
	except (TypeError, ValueError):
		dia = 0
	if dia not in range(5):
		dia = 0

	turno = request.GET.get("turno", "Matutino")
	if turno not in {"Matutino", "Vespertino"}:
		turno = "Matutino"

	semestre = request.GET.get("semestre", "")
	especialidad = request.GET.get("especialidad", "")

	bloques_dia = Bloque.objects.filter(dia=dia).select_related("grupo", "aula").order_by("hora_inicio")
	if turno:
		bloques_dia = bloques_dia.filter(grupo__turno=turno)
	if semestre.isdigit():
		bloques_dia = bloques_dia.filter(grupo__semestre=int(semestre))
	else:
		semestre = ""
	if especialidad:
		bloques_dia = bloques_dia.filter(grupo__especialidad=especialidad)

	tipo_aula = request.GET.get("tipo_aula", "")
	if tipo_aula not in {"AULA", "ESPECIAL", "FUERA"}:
		tipo_aula = ""

	salones_solicitados = {
		identificador
		for valor in request.GET.getlist("salones")
		for identificador in valor.split(",")
		if identificador.isdigit()
	}
	salones_seleccionados = set(
		Aula.objects.filter(id__in=salones_solicitados).values_list("id", flat=True)
	)
	if salones_seleccionados:
		bloques_dia = bloques_dia.filter(aula_id__in=salones_seleccionados)

	aulas_comparacion = list(Aula.objects.order_by("nombre"))
	for aula in aulas_comparacion:
		aula.seleccionada = aula.id in salones_seleccionados

	intervalos = sorted(set((b.hora_inicio, b.hora_fin) for b in bloques_dia))

	secciones = []
	for tipo, titulo in Aula.TIPOS:
		aulas_tipo = Aula.objects.filter(tipo=tipo).order_by("nombre")
		if salones_seleccionados:
			aulas_tipo = aulas_tipo.filter(id__in=salones_seleccionados)
		if tipo_aula and tipo != tipo_aula:
			continue
		filas_tipo = []
		for aula in aulas_tipo:
			celdas = []
			for inicio, fin in intervalos:
				ocupantes = [
					b for b in bloques_dia
					if b.aula_id == aula.id and b.hora_inicio == inicio and b.hora_fin == fin
				]
				celdas.append({"inicio": inicio, "fin": fin, "ocupantes": ocupantes})
			if celdas:
				filas_tipo.append({"aula": aula, "celdas": celdas})
		if filas_tipo:
			secciones.append({"titulo": titulo, "filas": filas_tipo})

	return render(request, "horarios/ocupacion.html", {
		"dia": dia,
		"dias": Bloque.DIAS,
		"turno": turno,
		"intervalos": intervalos,
		"filas": [],
		"bloques_count": bloques_dia.count(),
		"semestre": semestre,
		"especialidad": especialidad,
		"semestres": sorted(set(Grupo.objects.exclude(semestre=None).values_list("semestre", flat=True))),
		"especialidades": Grupo.objects.exclude(especialidad="").values_list("especialidad", flat=True).distinct().order_by("especialidad"),
		"secciones": secciones,
		"tipo_aula": tipo_aula,
		"aulas_comparacion": aulas_comparacion,
		"salones_seleccionados": sorted(str(identificador) for identificador in salones_seleccionados),
	})
