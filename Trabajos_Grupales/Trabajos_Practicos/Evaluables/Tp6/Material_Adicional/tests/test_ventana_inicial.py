import pytest
from frontend import Frontend # Este archivo no existe todavia
import tkinter as tk

def test_ventana_inicial():
    #Definir la aplicación
    app = Frontend()
    
    #smoke test, comprueba que solo la ventana esté abierta
    assert app.root is not None
    assert isinstance(app.root, tk.Tk)