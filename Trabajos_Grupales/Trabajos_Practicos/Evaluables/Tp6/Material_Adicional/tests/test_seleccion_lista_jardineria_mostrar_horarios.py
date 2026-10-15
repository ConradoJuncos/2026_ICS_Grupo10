import tkinter as tk
from frontend import Frontend

def test_seleccion_lista_jardineria_mostrar_horarios():
    # Inicializar app
    app = Frontend()
    
    # Act: Seleccionar el primer item, index 3, jardineria, y llamar al metodo que actualiza la segunda caja
    app.listbox.selection_set(3)
    app.actualizar_sublista()
    
    # Assert: Revisar que la sublista contenga información nueva para jardineria
    sub_items = app.sub_listbox.get(0, tk.END)
    assert len(sub_items) > 0
    assert "09:00" in sub_items