import tkinter as tk
from frontend import Frontend

def test_selecting_main_item_updates_sub_listbox():
    # Inicializar app
    app = Frontend()
    
    # Act: Seleccionar el primer item, index 0, tirolesa, y llamar al metodo que actualiza la segunda caja
    app.listbox.selection_set(0)
    app.actualizar_sublista()
    
    # Assert: Revisar que la sublista contenga información nueva para tirolesa
    sub_items = app.sub_listbox.get(0, tk.END)
    assert len(sub_items) > 0
    assert "18:00" in sub_items