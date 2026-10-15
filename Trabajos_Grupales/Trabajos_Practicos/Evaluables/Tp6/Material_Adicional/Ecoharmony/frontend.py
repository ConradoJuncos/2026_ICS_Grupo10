import tkinter as tk

class Frontend:
    def __init__(self):
        #Definir la ventana principal
        self.root = tk.Tk()
        #Definir los cupos asociados a cada actividad
        self.items_data = {
            "Tirolesa": 8,
            "Safari": 10,
            "Palestra": 5,
            "Jardineria": 3,
        }
        
        self.sub_data = {
            "Tirolesa": ["18:00", "17:00", "16:00"],
            "Safari": ["10:00", "11:00", "12:00"],
            "Palestra": ["14:00", "15:00", "16:00"],
            "Jardineria": ["09:00", "10:00", "11:00"]
        }
        
        #Llamar al metodo para inicializar la interfaz de usuario
        self.setup_ui()

    def setup_ui(self):
        # Crear un Listbox para mostrar los items y sus cantidades
        self.listbox = tk.Listbox(
            self.root,
            font=("Arial", 10),
            selectbackground="#3b82f6", 
            selectforeground="#ffffff", 
            bd=1,
            relief="solid",
            width=25,
            height=4
        )
        self.listbox.pack(padx=10, pady=10)
        
        #crear nueva listbox para la seleccion de horarios
        self.sub_listbox = tk.Listbox(
          self.root,
          font=("Arial", 10),
          bd=1,
          relief="solid",
          width=25,
          height=4
        )
        self.sub_listbox.pack(padx=10, pady=5)
        
        # Inserta numeros con visualizacion para el cliente, estos estan separados en la logica de la aplicacion.
        for name, qty in self.items_data.items():
            self.listbox.insert(tk.END, f"{name}  ({qty})")
        
        # Vincular el evento de seleccion a la actuaiizacion de la lista de horarios. Magia de python no la entiendo.
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.actualizar_sublista())
            
    def actualizar_sublista(self):
        # Revisar qué item esta selecciona en la lista de actividades
        seleccionado = self.listbox.curselection()
        if seleccionado:
            index = seleccionado[0]
            nombre_actividad = list(self.items_data.keys())[index]
            
            # Borrar cualquier otro contenido previo en la sub-lista
            self.sub_listbox.delete(0, tk.END)
            
            # Insertar los horarios asociados a la actividad seleccionada
            sub_items = self.sub_data.get(nombre_actividad, [])
            for item in sub_items:
                self.sub_listbox.insert(tk.END, item)
            
    #Metodo para refrescar la lista
    def refrescar_lista(self):
            # Limpia la lista desactualizada
            self.listbox.delete(0, tk.END)
            #Inserta de vuelta los items para actualizarla
            for name, qty in self.items_data.items():
                self.listbox.insert(tk.END, f"{name}  ({qty})")
    
    #Metodo para obtener la lista de items
    def obtener_lista_items(self):
        # Retorna solo los nombres de los items
        return list(self.items_data.keys())
    
if __name__ == "__main__":
    app = Frontend()
    app.root.mainloop()