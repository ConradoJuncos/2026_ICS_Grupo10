import tkinter as tk
from frontend import Frontend

def test_seleccion_lista_palestra_mostrar_horarios():
    # Inicializar app
    app = Frontend()
    
    # Act: Seleccionar el primer item, index 2, palestra, y llamar al metodo que actualiza la segunda caja
    app.listbox.selection_set(2)
    app.actualizar_sublista()
    
    # Assert: Revisar que la sublista contenga información nueva para palestra
    sub_items = app.sub_listbox.get(0, tk.END)
    assert len(sub_items) > 0
    assert "14:00" in sub_items