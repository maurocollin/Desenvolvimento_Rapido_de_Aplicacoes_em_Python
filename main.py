import tkinter as tk
from core.database import create_tables
from ui.main_window import MainWindow

def main():
    # Inicializa o banco de dados antes da interface
    create_tables()

    # Configura a janela principal do Tkinter
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()