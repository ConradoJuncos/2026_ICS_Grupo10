import tkinter as tk
from frontend import Frontend

def test_refrescar_lista_actividades_safari():
    # Arrange: Inicializar la app
    app = Frontend()
    
    # Act: Cambiar la cantidad de cupos de safari y refrescar la lista
    app.items_data["Safari"] = 9
    app.refrescar_lista()
    
    # Assert: Verificar que la lista despliegue el nuevo cupo de safari
    visualizacion_items = app.listbox.get(0, tk.END)
    assert "Safari  (9)" in visualizacion_items