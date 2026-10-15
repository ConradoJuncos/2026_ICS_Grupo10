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