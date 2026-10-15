import tkinter as tk
from frontend import Frontend

def test_refrescar_lista_actividades_Jardineria():
    # Arrange: Inicializar la app
    app = Frontend()
    
    # Act: Cambiar la cantidad de cupos de jardineria y refrescar la lista
    app.items_data["Jardineria"] = 2
    app.refrescar_lista()
    
    # Assert: Verificar que la lista despliegue el nuevo cupo de jardineria
    visualizacion_items = app.listbox.get(0, tk.END)
    assert "Jardineria  (2)" in visualizacion_items