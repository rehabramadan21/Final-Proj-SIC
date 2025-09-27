# main.py
import tkinter as tk
from categories import categories  # الكلاس اللي فيه كل حاجة

def main():
    root = tk.Tk()
    nav_stack = []
    app = categories(root)
    # ربط الـ root بالكلاس
    root.mainloop()

if __name__ == "__main__":
    main()
