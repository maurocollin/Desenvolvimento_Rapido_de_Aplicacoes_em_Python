import tkinter as tk
from core.database import create_tables
from ui.main_window import MainWindow

def main():
    create_tables()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()