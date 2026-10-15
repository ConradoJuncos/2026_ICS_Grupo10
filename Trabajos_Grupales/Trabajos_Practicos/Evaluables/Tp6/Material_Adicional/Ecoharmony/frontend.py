import tkinter as tk

class Frontend:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        #Crear lista de actividades
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(pady=10)
        
        #Añadir items a la lista de actividades
        initial_items = ["Tirolesa", "Safari", "Palestra"]
        for item in initial_items:
            self.listbox.insert(tk.END, item)
    
    def obtener_lista_items(self):
        # Obtener items de la lista de actividades
        return list(self.listbox.get(0, tk.END))
    
if __name__ == "__main__":
    app = Frontend()
    app.root.mainloop()