import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# COLORS and FONTS
COLORS = {
    "background": "#F8F8F8",
    "surface": "#FFFFFF",
    "title": "#3C467B",
    "button": "#3C467B",
    "text_primary": "#000000"
}

FONTS = {
    "title": ("Arial", 20, "bold"),
    "heading": ("Arial", 16, "bold"),
    "body": ("Arial", 12),
    "button": ("Arial", 12, "bold")
}

class style_one_category(tk.Toplevel):
    """Base class for event pages, handles UI layout and display"""
    def __init__(self, parent, category_name, events, nav_stack=None):
        super().__init__(parent)
        self.title(category_name)
        self.nav_stack = nav_stack
        self.configure(bg=COLORS['background'])
        self.state("zoomed")
        self.events = events

        top_frame = tk.Frame(self, bg=COLORS['background'])
        top_frame.pack(fill="x", padx=20, pady=10)

        back_btn = tk.Button(top_frame, text="← Back", font=FONTS['button'],
                             bg=COLORS['button'], fg='white',
                             command=self.go_back)
        back_btn.pack(side="left")

        # هنا بقية display_events والـ canvas كما عندك..

        # Header
        tk.Label(top_frame, text=f"{category_name} Events", font=FONTS['title'],
                 fg=COLORS['title'], bg=COLORS['background']).pack(padx=20)

        # Scrollable canvas
        container = tk.Frame(self, bg=COLORS['background'])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        canvas = tk.Canvas(container, bg=COLORS['background'])
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.main_frame = scrollable_frame
        self.display_events()


    def go_back(self):
        if self.nav_stack:
            self.withdraw()  # نشيل الصفحة الحالية من stack
            previous_page = self.nav_stack[-1]
            previous_page.deiconify()# نرجع الصفحة السابقة

    def open_category_page(parent, category_name, events, nav_stack):
        # اخفاء الصفحة الحالية بدل تدميرها
        if nav_stack:
            nav_stack[-1].withdraw()
        page = style_one_category(parent, category_name, events, nav_stack)
        nav_stack.append(page)



    def display_events(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.images = []  # To prevent garbage collection of images

        for idx, event in enumerate(self.events):
            row = idx // 3
            col = idx % 3

            frame = tk.Frame(self.main_frame, bg=COLORS['surface'], padx=10, pady=10,
                             relief="raised", bd=2, width=300, height=350)
            frame.grid(row=row, column=col, padx=100, pady=10, sticky="nsew")
            frame.grid_propagate(False)

            # Load image
            try:
                img = Image.open(event["image"]).resize((280, 150))
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)
                tk.Label(frame, image=photo, bg=COLORS['surface']).pack(pady=5)
            except:
                tk.Label(frame, text="No Image", bg=COLORS['surface']).pack(pady=5)

            tk.Label(frame, text=event["name"], font=FONTS['heading'], fg=COLORS['title'],
                     bg=COLORS['surface']).pack(pady=5)
            tk.Label(frame, text=f"{event['date']} | {event['location']}", fg=COLORS['text_primary'],
                     bg=COLORS['surface']).pack(pady=2)
            tk.Label(frame, text=f"Price: ${event['price']}", fg=COLORS['text_primary'],
                     bg=COLORS['surface']).pack(pady=2)
            tk.Label(frame, text=f"Rating: {event['rating']} ⭐", fg=COLORS['text_primary'],
                     bg=COLORS['surface']).pack(pady=2)
            tk.Label(frame, text=f"Available Seats: {event['capacity'] - event['booked']}", fg=COLORS['text_primary'],
                     bg=COLORS['surface']).pack(pady=2)

            tk.Button(frame, text="Book Your Seat", bg=COLORS['button'], fg='white', font=FONTS['button']).pack(pady=5)
            tk.Button(frame, text="More Details", bg=COLORS['button'], fg='white', font=FONTS['button']).pack(pady=5)

        # Make columns expand equally
        for i in range(3):
            self.main_frame.columnconfigure(i, weight=1)
        for i in range((len(self.events)+2)//3):
            self.main_frame.rowconfigure(i, weight=1)