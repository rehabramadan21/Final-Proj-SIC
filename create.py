import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font
import json
from datetime import datetime
import os
import uuid

class EventCreationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Creation Form")
        self.root.geometry("900x800")
        self.root.configure(bg='#2a2a2a')
        
        # Configure style for dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_dark_theme()
        
        # Variables
        self.event_name_var = tk.StringVar()
        self.event_description_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.tickets_var = tk.StringVar()
        self.image_path = ""
        
        # Tag variables
        self.tag_vars = {}
        self.tags = [
            'Art', 'Business', 'Charity', 'Community',
            'Concert', 'Conference', 'Craft', 'Culinary',
            'Cultural', 'Dance', 'DIY', 'Education',
            'Entertainment', 'Exhibition', 'Fashion', 'Festival',
            'Film', 'Fitness', 'Food', 'Gaming',
            'Health', 'Literature', 'Music', 'Networking',
            'Outdoor', 'Party', 'Photography', 'Poetry',
            'Religious', 'Science', 'Seminar', 'Sports',
            'Technology', 'Theater', 'Travel', 'Workshops'
        ]
        
        for tag in self.tags:
            self.tag_vars[tag] = tk.BooleanVar()
        
        self.create_widgets()
    
    def configure_dark_theme(self):
        # Configure ttk styles for dark theme
        self.style.configure('TLabel', background='#2a2a2a', foreground='white')
        self.style.configure('TFrame', background='#2a2a2a')
        self.style.configure('TEntry', fieldbackground='#404040', foreground='white', borderwidth=1)
        self.style.configure('TCombobox', fieldbackground='#404040', foreground='white', borderwidth=1)
        self.style.configure('TCheckbutton', background='#2a2a2a', foreground='white')
        self.style.configure('TButton', background='#404040', foreground='white', borderwidth=1)
        self.style.map('TButton',
                      background=[('active', '#505050')],
                      foreground=[('active', 'white')])
    
    def create_widgets(self):
        # Main frame with scrollbar
        main_frame = tk.Frame(self.root, bg='#2a2a2a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_frame, bg='#2a2a2a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a2a2a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Event Name
        self.create_label(scrollable_frame, "Event Name", 0)
        event_name_entry = self.create_entry(scrollable_frame, self.event_name_var, 1)
        
        # Event Description
        self.create_label(scrollable_frame, "Event Description", 2)
        desc_frame = tk.Frame(scrollable_frame, bg='#2a2a2a')
        desc_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        desc_frame.columnconfigure(0, weight=1)
        
        self.desc_text = tk.Text(desc_frame, height=5, bg='#404040', fg='white', 
                                border=1, relief='solid')
        self.desc_text.pack(fill='x', expand=True)
        
        char_count_label = tk.Label(desc_frame, text="0/500 characters", 
                                   bg='#2a2a2a', fg='gray', font=('Arial', 8))
        char_count_label.pack(anchor='w')
        
        def update_char_count(*args):
            content = self.desc_text.get(1.0, tk.END).strip()
            char_count = len(content)
            char_count_label.config(text=f"{char_count}/500 characters")
            if char_count > 500:
                char_count_label.config(fg='red')
            else:
                char_count_label.config(fg='gray')
        
        self.desc_text.bind('<KeyRelease>', update_char_count)
        
        # Date fields
        date_frame = tk.Frame(scrollable_frame, bg='#2a2a2a')
        date_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 10))
        date_frame.columnconfigure(0, weight=1)
        date_frame.columnconfigure(1, weight=1)
        
        # Start Date
        start_label = tk.Label(date_frame, text="Start Date", bg='#2a2a2a', fg='white')
        start_label.grid(row=0, column=0, sticky="w")
        start_entry = ttk.Entry(date_frame, textvariable=self.start_date_var)
        start_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        start_entry.insert(0, "mm/dd/yyyy --:-- --")
        
        # End Date
        end_label = tk.Label(date_frame, text="End Date", bg='#2a2a2a', fg='white')
        end_label.grid(row=0, column=1, sticky="w")
        end_entry = ttk.Entry(date_frame, textvariable=self.end_date_var)
        end_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0))
        end_entry.insert(0, "mm/dd/yyyy --:-- --")
        
        # Event Image
        self.create_label(scrollable_frame, "Event Image", 5)
        image_frame = tk.Frame(scrollable_frame, bg='#2a2a2a')
        image_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        image_frame.columnconfigure(0, weight=1)
        
        self.image_button = tk.Button(image_frame, text="Choose File    No file chosen", 
                                     bg='#404040', fg='white', border=1, relief='solid',
                                     command=self.choose_image)
        self.image_button.pack(fill='x')
        
        image_info_label = tk.Label(image_frame, text="Upload an image for your event (JPEG, PNG, JPG, GIF - max 2MB)", 
                                   bg='#2a2a2a', fg='gray', font=('Arial', 8))
        image_info_label.pack(anchor='w')
        
        # Location fields
        location_frame = tk.Frame(scrollable_frame, bg='#2a2a2a')
        location_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 10))
        location_frame.columnconfigure(0, weight=1)
        location_frame.columnconfigure(1, weight=1)
        
        # Country
        country_label = tk.Label(location_frame, text="Country", bg='#2a2a2a', fg='white')
        country_label.grid(row=0, column=0, sticky="w")
        
        countries = ['Select a country', 'United States', 'Canada', 'United Kingdom', 
                    'Germany', 'France', 'Japan', 'Australia', 'Egypt', 'Other']
        self.country_combo = ttk.Combobox(location_frame, textvariable=self.country_var, values=countries, state="readonly")
        self.country_combo.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        self.country_combo.current(0)
        
        # City
        city_label = tk.Label(location_frame, text="City", bg='#2a2a2a', fg='white')
        city_label.grid(row=0, column=1, sticky="w")
        city_entry = ttk.Entry(location_frame, textvariable=self.city_var)
        city_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0))
        city_entry.insert(0, "Enter City Name")
        
        # Number of Available Tickets
        self.create_label(scrollable_frame, "Number of Available Tickets", 8)
        tickets_entry = self.create_entry(scrollable_frame, self.tickets_var, 9)
        tickets_entry.insert(0, "Enter the number of available tickets")
        
        tickets_info_label = tk.Label(scrollable_frame, text="Enter the total number of tickets available for this event.", 
                                     bg='#2a2a2a', fg='gray', font=('Arial', 8))
        tickets_info_label.grid(row=10, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Tags
        self.create_label(scrollable_frame, "Tags", 11)
        tags_info_label = tk.Label(scrollable_frame, text="Select relevant tags to make your event more discoverable", 
                                  bg='#2a2a2a', fg='gray', font=('Arial', 8))
        tags_info_label.grid(row=12, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Tags grid
        tags_frame = tk.Frame(scrollable_frame, bg='#2a2a2a')
        tags_frame.grid(row=13, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Create tags in 4 columns
        row = 0
        col = 0
        for i, tag in enumerate(self.tags):
            tag_check = ttk.Checkbutton(tags_frame, text=tag, variable=self.tag_vars[tag])
            tag_check.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=2)
            
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        # Buttons
        button_frame = tk.Frame(scrollable_frame, bg='#2a2a2a')
        button_frame.grid(row=14, column=0, columnspan=2, pady=20)
        
        cancel_button = tk.Button(button_frame, text="CANCEL", bg='#606060', fg='white', 
                                 border=1, relief='solid', padx=20, pady=10, command=self.cancel_event)
        cancel_button.pack(side='left', padx=(0, 10))
        
        create_button = tk.Button(button_frame, text="CREATE EVENT", bg='#0066cc', fg='white', 
                                 border=1, relief='solid', padx=20, pady=10, command=self.create_event)
        create_button.pack(side='left')
        
        # Configure grid weights
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_label(self, parent, text, row):
        label = tk.Label(parent, text=text, bg='#2a2a2a', fg='white', font=('Arial', 10, 'bold'))
        label.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 5))
        return label
    
    def create_entry(self, parent, textvariable, row):
        entry = ttk.Entry(parent, textvariable=textvariable)
        entry.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        return entry
    
    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose Event Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            self.image_path = file_path
            filename = os.path.basename(file_path)
            self.image_button.config(text=f"Choose File    {filename}")
    
    def generate_event_id(self):
        """Generate a unique event ID"""
        # Option 1: UUID (Universally Unique Identifier)
        return str(uuid.uuid4())
        
        # Option 2: If you prefer shorter IDs, use timestamp + random
        # import random
        # timestamp = int(datetime.now().timestamp())
        # random_num = random.randint(1000, 9999)
        # return f"EVENT_{timestamp}_{random_num}"
    
    def collect_data(self):
        # Get selected tags
        selected_tags = [tag for tag, var in self.tag_vars.items() if var.get()]
        
        # Get description text
        description = self.desc_text.get(1.0, tk.END).strip()
        
        # Generate unique ID for the event
        event_id = self.generate_event_id()
        
        event_data = {
            "id": event_id,
            "event_name": self.event_name_var.get(),
            "event_description": description,
            "start_date": self.start_date_var.get(),
            "end_date": self.end_date_var.get(),
            "event_image": self.image_path,
            "country": self.country_var.get(),
            "city": self.city_var.get(),
            "available_tickets": self.tickets_var.get(),
            "tags": selected_tags,
            "created_at": datetime.now().isoformat()
        }
        return event_data
    
    def create_event(self):
        event_data = self.collect_data()
        
        # Basic validation
        if not event_data["event_name"]:
            messagebox.showerror("Error", "Please enter an event name")
            return
        
        if not event_data["event_description"]:
            messagebox.showerror("Error", "Please enter an event description")
            return
        
        # Save to JSON file
        try:
            # Load existing events if file exists
            events = []
            if os.path.exists("events.json"):
                with open("events.json", "r", encoding="utf-8") as f:
                    events = json.load(f)
            
            # Add new event
            events.append(event_data)
            
            # Save updated events
            with open("events.json", "w", encoding="utf-8") as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Event created successfully!\nEvent ID: {event_data['id']}")
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save event: {str(e)}")
    
    def cancel_event(self):
        result = messagebox.askyesno("Cancel", "Are you sure you want to cancel? All unsaved data will be lost.")
        if result:
            self.clear_form()
    
    def clear_form(self):
        self.event_name_var.set("")
        self.desc_text.delete(1.0, tk.END)
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.end_date_var.set("")
        self.country_var.set("")
        self.city_var.set("")
        self.tickets_var.set("")
        self.image_path = ""
        self.image_button.config(text="Choose File    No file chosen")
        
        # Clear all tag checkboxes
        for var in self.tag_vars.values():
            var.set(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = EventCreationForm(root)
    root.mainloop()