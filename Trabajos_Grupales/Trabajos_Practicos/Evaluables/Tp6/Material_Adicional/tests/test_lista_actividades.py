from frontend import Frontend

def test_window_contains_eco_list_items():
    app = Frontend()
    
    items = app.obtener_lista_actividades()
    
    # Assert: Check that the list exists and contains expected items
    assert isinstance(items, list)
    assert "Tirolesa" in items
    assert "Safari" in items
    assert "Palestra" in items
    assert "Jardineria" in items