# Entorno de desarrollo del TP6

Ejecutar los comandos siguientes desde esta carpeta (`Material_Adicional`).
El entorno verificado usa **CPython 3.14.8 en macOS ARM64**. CodeStyle menciona
Python 3.15: esa diferencia sigue pendiente de acuerdo del grupo. No se ha
verificado esta instalacion en Python 3.15 ni en otros sistemas operativos.

## Instalacion

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip check
```

`requirements.txt` contiene Django, Segno y las dependencias transitivas de
ejecucion. `requirements-dev.txt` incluye ese archivo y agrega pytest,
pytest-django, Black, Ruff y mypy con sus dependencias. Para instalar solamente
lo necesario para ejecutar la aplicacion, usar `-r requirements.txt`.
No se necesita instalar paquetes globales ni usar `--break-system-packages`.

Las versiones estan fijadas para el entorno indicado. Al actualizarlas, comprobar
la instalacion en un entorno nuevo, ejecutar las verificaciones y actualizar
tambien las dependencias transitivas. No reemplazar estos archivos con un
`pip freeze` de un entorno que contenga paquetes de otros proyectos.

## Verificaciones

```bash
python -m pytest -q --migrations
python manage.py check
python manage.py makemigrations --check --dry-run
python -m black --check .
python -m ruff check .
```

Las pruebas usan la base de test de Django; no requieren migrar la SQLite de
desarrollo ni iniciar un servidor SMTP. `--migrations` explicita que se verifica
el esquema instalado desde migraciones.

Hay incumplimientos de estilo previos: instalar las herramientas no los corrige
ni significa que los controles globales ya pasan. La configuracion y el alcance
global de mypy siguen pendientes de acuerdo. Como comprobacion limitada de los
archivos de la correccion de unicidad se puede ejecutar:

```bash
python -m mypy --follow-imports=silent --ignore-missing-imports core/tests/test_migraciones_actividad.py core/migrations/0002_alter_actividad_nombre.py
```

Ese comando omite el analisis de imports y los errores por librerias sin tipos;
no certifica el tipado de Django ni el del proyecto completo.

## Arranque local

Antes de migrar una base existente, revisar nombres de actividades duplicados:
la migracion de unicidad los rechaza y no los elimina automaticamente. Para una
base nueva o una base revisada:

```bash
python manage.py migrate
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/>. El catalogo y la pantalla de inscripcion son
visuales; todavia no registran reservas reales.

El adaptador de correo usa un servidor SMTP externo en `localhost:1025`.
Estos requirements no instalan ni inician ese servidor. Su configuracion de
demostracion y la entrega real quedan fuera de la preparacion de dependencias.
