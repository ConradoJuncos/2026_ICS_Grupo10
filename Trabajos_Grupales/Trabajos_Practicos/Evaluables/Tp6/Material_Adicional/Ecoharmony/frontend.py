import tkinter as tk

class Frontend:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(pady=10)
    
if __name__ == "__main__":
    app = Frontend()
    app.root.mainloop()