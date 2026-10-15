from frontend import Frontend

def test_insercion_item_Tirolesa_lista_actividades():
    app = Frontend()
    
    # Obtener items de la lista de actividades
    items = app.get_list_items()
    
    # Assert: Revisar que exista el item Tirolesa en la lista de actividades
    assert isinstance(items, list)
    assert "Tirolesa" in items