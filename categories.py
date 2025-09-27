import tkinter as tk
from tech_page import tech_page
from art_page import art_page
from sports_page import sports_page
from social_page import social_page

class categories:
    def __init__(self, master):
        self.master = master
        self.nav_stack = []
        self.master.title("Event Categories")
        self.master.configure(bg='#F0F0F0')
        self.master.state("zoomed")

        # اسم الشركة
        self.company_label = tk.Label(master, text="A7GEZLAK",
                                      font=('Arial', 28, 'bold'),
                                      fg='#3C467B', bg='#F0F0F0')
        self.company_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # عنوان الصفحة
        self.title_label = tk.Label(master, text="Explore Our Event Categories",
                                    font=('Arial', 20, 'bold'),
                                    fg='#333333', bg='#F0F0F0')
        self.title_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Main Frame للأزرار
        self.main_frame = tk.Frame(master, bg='#FFFFFF')
        self.main_frame.grid(row=2, column=0, columnspan=2, padx=50, pady=20, sticky='nsew')

        # تعريف الأعمدة والصفوف في main_frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # إنشاء الأزرار
        self.create_buttons()

        # توزيع الصفوف والأعمدة الرئيسية في root عشان تتوسع
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)

    def create_buttons(self):
        # زر 1
        # إنشاء الأزرار
        self.button_Tech = tk.Button(self.main_frame, text="Tech & IT Events",
                                     font=('Arial', 16, 'bold'),
                                     fg='#FFFFFF', bg='#3C467B',
                                     relief='flat', cursor='hand2',
                                     activebackground='#2E3A5F',
                                     width=25, height=6,
                                     command=lambda: self.open_category(tech_page))
        self.button_Tech.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

        self.button_Arts = tk.Button(self.main_frame, text="Creative & Arts Events",
                                     font=('Arial', 16, 'bold'),
                                     fg='#FFFFFF', bg='#3C467B',
                                     relief='flat', cursor='hand2',
                                     activebackground='#2E3A5F',
                                     width=25, height=6,
                                     command=lambda: self.open_category(art_page))
        self.button_Arts.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

        self.button_Sports = tk.Button(self.main_frame, text="Sports & Health Events",
                                       font=('Arial', 16, 'bold'),
                                       fg='#FFFFFF', bg='#3C467B',
                                       relief='flat', cursor='hand2',
                                       activebackground='#2E3A5F',
                                       width=25, height=6,
                                       command=lambda: self.open_category(sports_page))
        self.button_Sports.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

        self.button_Lifestyle = tk.Button(self.main_frame, text="Lifestyle & Social Events",
                                          font=('Arial', 16, 'bold'),
                                          fg='#FFFFFF', bg='#3C467B',
                                          relief='flat', cursor='hand2',
                                          activebackground='#2E3A5F',
                                          width=25, height=6,
                                          command=lambda: self.open_category(social_page))
        self.button_Lifestyle.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')

    def open_category(self, page_class):
        existing_page = None
        if self.nav_stack:
            self.nav_stack[-1].withdraw()  # اخفي الصفحة الحالية فقط
        page = page_class(self.master, self.nav_stack)
        self.nav_stack.append(page)
        page.protocol("WM_DELETE_WINDOW", lambda: self.close_category(page))

    def close_category(self, page):
        if page in self.nav_stack:
            self.nav_stack.remove(page)
            page.withdraw()  # بدل destroy

        if not self.nav_stack:
            self.master.deiconify()
        else:
            self.nav_stack[-1].deiconify()  # إظهار الصفحة السابقة

