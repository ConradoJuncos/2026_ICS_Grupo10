"""Comprueba las restricciones del esquema generado por las migraciones."""

import pytest
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor


@pytest.mark.django_db
def test_esquema_migrado_rechaza_actividades_con_nombre_repetido() -> None:
    """Impide duplicar una actividad al instalar la base desde migraciones."""
    executor = MigrationExecutor(connection)
    estado = executor.loader.project_state()
    modelo_actividad = estado.apps.get_model("core", "Actividad")
    modelo_actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)

    with pytest.raises(IntegrityError), transaction.atomic():
        modelo_actividad.objects.create(nombre="TIROLESA", cupo_maximo=10)
