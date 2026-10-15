import tkinter as tk

class Frontend:
    def __init__(self):
        self.root = tk.Tk()
        self.count = 0
        self.label = tk.Label(self.root, text=f"Count: {self.count}")
        self.setup_ui()

    def setup_ui(self):
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(pady=10)

    def get_label_text(self):
        return self.label.cget("text")
    
if __name__ == "__main__":
    app = Frontend()
    app.root.mainloop()