import pytest
from frontend import Frontend # Este archivo no existe todavia

def test_ventana_inicial():
    #Definir la aplicación
    app = Frontend()
    
    # Assert - checking if the UI text starts at 0
    assert app.get_label_text() == "Count: 0"