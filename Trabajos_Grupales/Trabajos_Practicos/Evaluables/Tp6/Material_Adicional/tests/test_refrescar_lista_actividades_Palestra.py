import tkinter as tk
from frontend import Frontend

def test_refrescar_lista_actividades_Palestra():
    # Arrange: Inicializar la app
    app = Frontend()
    
    # Act: Cambiar la cantidad de cupos de palestra y refrescar la lista
    app.items_data["Palestra"] = 6
    app.refrescar_lista()
    
    # Assert: Verificar que la lista despliegue el nuevo cupo de palestra
    visualizacion_items = app.listbox.get(0, tk.END)
    assert "Palestra  (6)" in visualizacion_items