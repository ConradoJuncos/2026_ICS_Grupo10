import tkinter as tk
from frontend import Frontend

def test_refrescar_lista_actividades_tirolesa():
    # Arrange: Inicializar la app
    app = Frontend()
    
    # Act: Cambiar la cantidad de cupos de tirolesa y refrescar la lista
    app.items_data["Tirolesa"] = 7
    app.refrescar_lista()
    
    # Assert: Verificar que la lista despliegue el nuevo cupo de tirolesa
    visualizacion_items = app.listbox.get(0, tk.END)
    assert "Tirolesa  (7)" in visualizacion_items