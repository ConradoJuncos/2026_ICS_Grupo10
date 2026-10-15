import tkinter as tk
from frontend import Frontend

def test_seleccion_de_horarios_listbox_creacion():
    # Levantar app
    app = Frontend()
    
    # Assert: Comprueba si existe una segunda Listbox en la interfaz para la seleccion de horarios
    assert hasattr(app, "sub_listbox")
    assert isinstance(app.sub_listbox, tk.Listbox)