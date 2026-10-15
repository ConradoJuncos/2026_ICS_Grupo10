import tkinter as tk
from frontend import Frontend

def test_seleccion_lista_safari_mostrar_horarios():
    # Inicializar app
    app = Frontend()
    
    # Act: Seleccionar el primer item, index 1, safari, y llamar al metodo que actualiza la segunda caja
    app.listbox.selection_set(1)
    app.actualizar_sublista()
    
    # Assert: Revisar que la sublista contenga información nueva para safari
    sub_items = app.sub_listbox.get(0, tk.END)
    assert len(sub_items) > 0
    assert "10:00" in sub_items