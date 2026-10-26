# Entorno de desarrollo del TP6

Ejecutar los comandos siguientes desde esta carpeta (`Programa`).
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
python -m mypy .
```

Las pruebas usan la base de test de Django; no requieren migrar la SQLite de
desarrollo ni iniciar un servidor SMTP. `--migrations` explicita que se verifica
el esquema instalado desde migraciones.

`mypy.ini` ignora los imports sin tipos (Django y Segno no los publican) y
excluye las migraciones generadas, por lo que mypy no verifica el tipado
interno de Django.

## Arranque local

Antes de migrar una base existente, revisar nombres de actividades duplicados:
la migracion de unicidad los rechaza y no los elimina automaticamente. Para una
base nueva o una base revisada:

```bash
python manage.py migrate
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/>. Al finalizar una inscripcion, la aplicacion la
registra, muestra la confirmacion y envia el correo con el resumen y el codigo QR.

El correo se envia a un servidor SMTP en `localhost:1025`, configurable con
`CORREO_SMTP_HOST` y `CORREO_SMTP_PUERTO` en `config/settings.py`. Estos
requirements no instalan ni inician ese servidor. Sin servidor, la inscripcion se registra igual
y el error de envio aparece en la terminal de `runserver`. Para ver los correos
durante una demostracion se puede iniciar un servidor SMTP local de pruebas en
ese puerto, por ejemplo Mailpit (interfaz web en <http://127.0.0.1:8025/>).
