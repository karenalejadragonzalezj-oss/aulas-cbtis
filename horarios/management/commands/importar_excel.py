from django.core.management.base import BaseCommand
from openpyxl import load_workbook
from horarios.models import Aula, Grupo, Bloque

DIAS = {"Lunes": 0, "Martes": 1, "Miércoles": 2, "Jueves": 3, "Viernes": 4}
ESPECIALES = {"Lab C1", "Taller de dibujo", "Cómputo"}
FUERA = "Fuera de aula (Act. física)"


class Command(BaseCommand):
    help = "Importa grupos y bloques desde el Excel de horarios (borra lo anterior)."

    def add_arguments(self, parser):
        parser.add_argument("archivo")

    def handle(self, *args, **opts):
        wb = load_workbook(opts["archivo"], data_only=True, read_only=True)

        Bloque.objects.all().delete()
        Grupo.objects.all().delete()
        Aula.objects.all().delete()

        aulas = {}

        def get_aula(nombre):
            nombre = str(nombre).strip()
            if nombre not in aulas:
                tipo = "FUERA" if nombre == FUERA else "ESPECIAL" if nombre in ESPECIALES else "AULA"
                aulas[nombre] = Aula.objects.create(nombre=nombre, tipo=tipo)
            return aulas[nombre]

        grupos = {}
        for nombre, sem, esp, turno, aula, *_ in wb["Grupos"].iter_rows(min_row=2, values_only=True):
            if not nombre:
                continue
            grupos[nombre] = Grupo.objects.create(
                nombre=nombre, semestre=sem, especialidad=esp, turno=turno, aula_fija=get_aula(aula)
            )

        bloques = []
        for sem, grupo, esp, turno, aula, dia, ini, fin, materia, *_ in wb["Horarios"].iter_rows(min_row=2, values_only=True):
            if not grupo:
                continue
            bloques.append(Bloque(
                grupo=grupos[grupo], aula=get_aula(aula), dia=DIAS[dia],
                hora_inicio=ini, hora_fin=fin, materia=materia,
            ))
        Bloque.objects.bulk_create(bloques)

        self.stdout.write(self.style.SUCCESS(
            f"Importados: {len(grupos)} grupos, {len(aulas)} aulas/espacios, {len(bloques)} bloques."
        ))
