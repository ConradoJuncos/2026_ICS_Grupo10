from frontend import Frontend

def test_item_numbers_are_correct():
    # Iniciar aplicacion
    app = Frontend()
    
    # Assert: Revisar que cada item tenga su numero inicial
    assert app.items_data["Tirolesa"] == 8
    assert app.items_data["Safari"] == 10
    assert app.items_data["Palestra"] == 5
    assert app.items_data["Jardineria"] == 3