from frontend import Frontend
import tkinter as tk

def test_creacion_lista_actividades():
    app = Frontend()
    
    # Assert: Check that the list exists and contains expected items
    assert hasattr(app, "listbox")
    assert isinstance(app.listbox, tk.Listbox)