# Planteamiento del problema: choques de turnos y asignación de aulas

**CBTis 234, Nuevo Laredo, Tamaulipas**  
**Periodo:** agosto de 2026 – enero de 2027  
**Proyecto:** aplicación web para consultar horarios y apoyar la asignación de aulas  
**Documento:** planteamiento, descripción de la página y código principal

> **Nota sobre los datos:** las cifras de grupos, aulas y choques de las secciones siguientes corresponden al análisis proporcionado para este documento. Conviene anexar o citar el archivo de horarios y confirmar los resultados con la dirección antes de presentar el informe como medición oficial.

## 1. Contexto

El plantel opera con dos turnos. El turno matutino imparte clases de 7:00 a 14:10 horas y el turno vespertino de 12:30 a 19:40 horas. Entre ambos turnos existe un **empalme de 1 hora con 40 minutos**, de 12:30 a 14:10, durante el cual grupos de ambos turnos pueden tener clase al mismo tiempo.

De acuerdo con los horarios publicados para este periodo, el plantel atiende **40 grupos** de primero, tercero y quinto semestre: 23 en el turno matutino y 17 en el vespertino. Se reportan **24 aulas**, además de espacios especiales como el laboratorio C1, el taller de dibujo y la sala de cómputo. Las especialidades son Administración de Recursos Humanos, Programación, Ciberseguridad (solo matutino), Construcción y Electrónica.

## 2. Descripción del problema

Cada grupo tiene un aula asignada. En el turno vespertino, 15 de los 17 grupos utilizan el aula de un grupo matutino. Durante el empalme, el grupo vespertino puede llegar cuando el grupo matutino todavía ocupa ese salón y quedarse sin espacio disponible.

Los horarios se encuentran en documentos separados, uno por grupo, y no existe una vista general que permita consultar la ocupación de todas las aulas por día y bloque. Por esta razón, los posibles choques pueden detectarse hasta que ya ocurrieron.

## 3. Datos que respaldan el problema

Se consolidaron los horarios de los 40 grupos en una base de datos y se revisó la ocupación de aulas entre las 11:40 y las 14:10 horas. Según el análisis proporcionado, los resultados son:

- **No faltan aulas en total.** En el momento de mayor demanda hay 21 grupos que necesitan salón al mismo tiempo y existen 24 aulas. Al contar también laboratorios y talleres como espacios utilizables, el máximo reportado es 23. El análisis concluye que quedan al menos 3 espacios libres.
- **Sí hay choques por la asignación fija.** Se reportaron 9 casos durante la semana en los que un grupo vespertino y uno matutino tienen clase a la vez en la misma aula. El caso más repetido es 5A de Construcción vespertino con 3BM de Recursos Humanos en el aula 5L, con coincidencias cinco veces por semana, una de ellas desde las 11:40.
- **Los casos reportados podrían resolverse reasignando espacios.** En cada uno de los 9 casos se encontraron al menos 4 aulas libres en ese horario, según el análisis proporcionado.
- **Hay ajustes manuales parciales.** En primer semestre vespertino, 4 de los 7 grupos no tienen clase antes de las 14:10, lo cual podría indicar que se intenta reducir el empalme manualmente. Esta interpretación debe confirmarse con el personal responsable.

## 4. Causas identificadas

- Asignación de aula fija por grupo, sin comprobar la disponibilidad del salón en cada bloque.
- Horarios dispersos en archivos separados, sin una vista general de ocupación.
- Bloques de distintas duraciones y huecos diferentes entre grupos, lo que dificulta revisar los conflictos manualmente.
- Falta de un mecanismo de aviso para detectar un choque antes de que ocurra.

## 5. Consecuencias

Según observaciones del alumnado, algunos grupos vespertinos llegan y no encuentran disponible el salón asignado. Esto puede ocasionar pérdida de tiempo de clase mientras se busca otro espacio, interrupciones a grupos matutinos que todavía están en clase y desorden en el uso de las instalaciones.

*Estas consecuencias provienen de observaciones directas del alumnado y están pendientes de medirse de manera sistemática.*

## 6. Planteamiento del problema

**¿Cómo puede el plantel saber, en cada bloque de clase, qué aulas están libres y asignarlas sin que se empalmen los grupos de ambos turnos?**

## 7. Propuesta de solución

Desarrollar una **aplicación web de gestión y consulta de aulas** que registre cada clase como un bloque con grupo, aula, día y hora. La propuesta contempla:

- Consultar horarios por grupo, aula, materia y día.
- Consultar la ocupación de aulas en un día seleccionado.
- Detectar posibles cruces cuando dos bloques coinciden en la misma aula, día y horario.
- En una etapa posterior, sugerir aulas libres y generar reportes para apoyar las decisiones de la dirección.

La aplicación actual muestra los horarios y detecta cruces del día actual al cargar la página. **Todavía no reasigna grupos ni recomienda automáticamente un aula alternativa.** Esa función se plantea como una mejora futura.

Los usuarios previstos son personal administrador (dirección o prefectura), docentes y alumnos. Se estima inicialmente una carga baja, de decenas de usuarios simultáneos; esta estimación debe validarse antes de definir el servidor definitivo.

## 8. Objetivos

### Objetivo general

Diseñar una aplicación web que permita consultar la asignación de aulas por bloque de clase y apoyar la prevención de choques entre los turnos matutino y vespertino.

### Objetivos específicos

- Consolidar los horarios de los 40 grupos en una base de datos única.
- Identificar automáticamente los empalmes de aula entre grupos.
- Mostrar la ocupación de las aulas por día y franja horaria.
- Sentar las bases para proponer reasignaciones que eliminen los choques detectados.

## 9. Alcance y limitaciones

La aplicación no modifica los horarios oficiales de entrada y salida de los turnos, porque esa decisión corresponde a la dirección. El sistema organiza y presenta los datos disponibles para ayudar a identificar conflictos y aprovechar mejor los espacios.

Los datos pueden cambiar durante el semestre; por ello, los horarios importados deben mantenerse actualizados. Según los supuestos del análisis inicial, el laboratorio C1, el taller de dibujo, la sala de cómputo y la activación física no se contaron como aulas ordinarias. La disponibilidad real y las restricciones de uso de cada espacio deben confirmarse con el plantel.

La vista de cruces se actualiza al consultar o recargar la página, utilizando el día local del servidor. No es una actualización instantánea mediante notificaciones automáticas. De lunes a viernes filtra los bloques del día correspondiente; durante sábado y domingo no presenta cruces de la semana.

## 10. Observaciones sobre los datos

- El aula 10 aparece asignada a dos grupos vespertinos (5B de Recursos Humanos y 5A de Programación), y también a 5AM de Programación en la mañana. Es probable que exista un error de captura; debe verificarse con la dirección antes de corregir los registros.
- Antes de tomar decisiones, se recomienda contrastar los resultados con el archivo fuente y validar las aulas especiales que pueden utilizarse como espacios alternativos.

## 11. Descripción de la página web

La página principal funciona como un panel de consulta. La interfaz incluye:

1. **Barra superior:** identificación del CBTis 234 y accesos a Administración y Ocupación.
2. **Encabezado:** nombre de la aplicación y periodo escolar.
3. **Tarjetas de resumen:** cantidad de grupos, aulas/espacios y posibles cruces detectados para hoy.
4. **Tabla de bloques:** presenta día, horario, grupo, aula y materia. Incluye filtros por texto, grupo, aula y día, además de paginación.
5. **Panel “Posibles cruces”:** indica el día actual y enumera los bloques que se traslapan en una misma aula. Si no encuentra conflictos para hoy, lo informa.
6. **Descarga de Excel:** permite exportar los horarios registrados.

La página también ofrece una vista de ocupación por día y una página de detalle por grupo. El diseño se adapta a pantallas pequeñas y grandes.

**Rutas principales:**

| Dirección | Función |
|---|---|
| `/` | Panel principal, filtros y cruces del día actual |
| `/ocupacion/` | Vista de ocupación de aulas por día y filtros |
| `/grupo/<id>/` | Horario detallado de un grupo |
| `/exportar-excel/` | Descarga del horario en formato Excel |
| `/admin/` | Administración de aulas, grupos y bloques |

## 12. Código principal de la aplicación

El proyecto está desarrollado con Django y organiza la información en tres entidades: aulas, grupos y bloques de horario. El modelo de bloque guarda el día como número de lunes a viernes, junto con sus horas de inicio y fin.

### 12.1 Modelo de datos

Fragmento representativo de `horarios/models.py`:

```python
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
```

### 12.2 Detección de cruces del día actual

La vista principal obtiene la fecha local configurada en Django. `weekday()` devuelve 0 para lunes y 4 para viernes; si es fin de semana, la consulta de bloques queda vacía. Después agrupa los bloques por aula y día, los ordena por hora y compara sus intervalos.

Fragmento representativo de `horarios/views.py`:

```python
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
    lista.sort(key=lambda bloque: (bloque.hora_inicio, bloque.hora_fin))
    for indice, primero in enumerate(lista):
        for segundo in lista[indice + 1:]:
            if segundo.hora_inicio >= primero.hora_fin:
                break
            if primero.hora_inicio < segundo.hora_fin:
                choques.append((primero, segundo))
```

Dos bloques se consideran en conflicto cuando corresponden a la misma aula y día y sus intervalos de tiempo se traslapan. El resultado se limita a los 12 primeros elementos para presentarlo en el panel.

### 12.3 Presentación de los cruces

Fragmento de `horarios/templates/horarios/inicio.html`:

```django
<h2>Posibles cruces · {{ hoy|date:"l"|capfirst }}</h2>
<p>Dos grupos programados hoy en la misma aula y horario</p>

{% if choques %}
  {% for primero, segundo in choques %}
    <div>
      {{ primero.get_dia_display }} ·
      {{ primero.hora_inicio|time:"H:i" }}–{{ primero.hora_fin|time:"H:i" }}
      Aula {{ primero.aula.nombre }}
      {{ primero.grupo.nombre }} · {{ primero.materia }}
      {{ segundo.grupo.nombre }} · {{ segundo.materia }}
    </div>
  {% endfor %}
{% else %}
  <p>No se detectaron cruces de aula para hoy.</p>
{% endif %}
```

### 12.4 Rutas y administración

Las direcciones de la página se conectan con las vistas desde `config/urls.py`. El sitio también utiliza el panel administrativo de Django para registrar y revisar aulas, grupos y bloques de horario. La importación inicial de datos se realiza desde un archivo Excel mediante el comando de administración del proyecto.

## 13. Requisitos de software

### Desarrollo y ejecución actual

- Sistema operativo compatible con Python y Django, como Windows o Linux.
- Python 3.14.7 en el entorno de desarrollo actual.
- Django 6.1.3.
- SQLite para la base de datos del proyecto actual.
- openpyxl 3.1.5 para leer y generar archivos Excel.
- Navegador web actualizado para consultar la aplicación.
- Visual Studio Code es recomendable para editar el proyecto, pero no es requisito para los usuarios finales.

### Recomendaciones para publicación

Para una prueba dentro del plantel puede usarse un servidor conectado a la red local. Antes de publicar el servicio para uso real se recomienda configurar `DEBUG = False`, definir hosts permitidos, proteger credenciales, realizar copias de seguridad y habilitar HTTPS si se accede desde una red externa. Si aumenta el número de usuarios o se necesita operación multiusuario más robusta, se debe evaluar sustituir SQLite por una base de datos como PostgreSQL.

## 14. Requisitos de hardware estimados

Los siguientes valores son una **estimación inicial para una carga baja** y no sustituyen una prueba de rendimiento ni una cotización del equipo:

| Componente | Requisito inicial sugerido |
|---|---|
| Servidor para prueba local | Procesador de 2 núcleos, 4 GB de RAM y al menos 10 GB libres para sistema, aplicación, base de datos y respaldos iniciales |
| Equipo de desarrollo | Procesador de 2 núcleos, 8 GB de RAM recomendados y espacio para Python, editor y archivos del proyecto |
| Dispositivo cliente | Computadora, tableta o teléfono con navegador actualizado y conexión a la red |
| Red del plantel | Red local Wi-Fi o cableada con cobertura suficiente en las áreas donde se consultarán los horarios |
| Respaldo | Medio de almacenamiento separado para copias periódicas de la base de datos y del archivo fuente de horarios |

El dimensionamiento final debe considerar cuántos usuarios consultarán el sistema simultáneamente, si habrá acceso desde fuera del plantel, la frecuencia de actualización de los horarios y la política institucional de respaldo.

## 15. Pruebas realizadas

Se añadieron pruebas automatizadas para comprobar que la vista principal muestra únicamente los cruces del día actual y que no muestra cruces en fin de semana. En la ejecución de validación del proyecto, las dos pruebas de la aplicación pasaron correctamente.

## 16. Conclusión

El problema descrito no parece deberse únicamente a una falta total de aulas, sino a la asignación fija y a la falta de una herramienta común para revisar su disponibilidad por bloque. La aplicación ya centraliza los horarios y permite consultar la ocupación, además de señalar posibles cruces del día. Como siguientes pasos se propone validar las cifras con la dirección, corregir posibles errores de captura, medir la demanda real y desarrollar la recomendación automática de aulas alternativas.

## Referencias al código del proyecto

- Modelos de datos: [horarios/models.py](horarios/models.py)
- Vista principal y detección de cruces: [horarios/views.py](horarios/views.py)
- Página principal: [horarios/templates/horarios/inicio.html](horarios/templates/horarios/inicio.html)
- Direcciones web: [config/urls.py](config/urls.py)
- Importación desde Excel: [horarios/management/commands/importar_excel.py](horarios/management/commands/importar_excel.py)
- Pruebas de cruces diarios: [horarios/tests.py](horarios/tests.py)
