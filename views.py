from tkinter import messagebox as _msgbox
from tkinter import filedialog
import tkinter as tk
from utils import center_window, get_current_date, get_current_time, show
from tkinter import ttk
from backends import BaseManager
from constants import *


class BaseView(BaseManager):
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_withdraw()
        super().__init__(root_window=self.root)
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.index_view_window = None
        self.forgot_password_view_window = None
        self.students_information_window = None
        self.books_information_window = None
        self.users_information_window = None
        self.register_student_window = None
        self.add_book_window = None
        self.create_user_window = None
        self.unregister_student_window = None
        self.remove_book_window = None
        self.delete_user_window = None
        self.issue_book_window = None
        self.retrieve_book_window = None

    def log_in_view(self):
        if WIN32:
            self.root.iconbitmap(WINDOW_ICON_BITMAP_PATH)
            self.root.iconphoto(False, tk.PhotoImage(file=WINDOW_ICON_PHOTO_PATH))
        self.root.title(WINDOW_TITLE)
        self.root.attributes("-alpha", .9)
        container = tk.Canvas(self.root, bg=DEFAULT_BACKGROUND_COLOR)
        heading_label = tk.Label(container, anchor="e", font=HEADER_FONT_1, bg=LOGIN_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR)
        heading_label["text"] = "LOGIN TO OGITECH LIBRARY"
        heading_label.place(relx=.1, rely=.1, relheight=.08, relwidth=.8)

        username_label = tk.Label(container, text="Username", font=FONT_1, bg=LOGIN_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR)
        username_label.place(relx=.1, rely=.4, relheight=.08, relwidth=.22)

        username_entry = tk.Entry(container, textvariable=self.username, width=45, font=FONT_1)
        username_entry.place(relx=.32, rely=.4, relheight=.08, relwidth=.5)
        username_entry.focus_set()

        password_label = tk.Label(container, anchor="e", text="Password", font=FONT_1, bg=LOGIN_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR)
        password_label.place(relx=.1, rely=.52, relheight=.08, relwidth=.2)

        password_entry = tk.Entry(container, show='*', textvariable=self.password, width=45, font=FONT_1)
        password_entry.place(relx=.32, rely=.52, relheight=.08, relwidth=.5)
        username_entry.bind("<Return>", lambda event=None: password_entry.focus_set())
        password_entry.bind("<Return>", lambda event=None: self._next())

        login_entries = [username_entry, password_entry]

        login_button = tk.Button(container, text="Log in", bg="#b9d5f0" , font=DEFAULT_BUTTON_FONT, command=self._next)
        login_button["activeforeground"] = "white"
        login_button["activebackground"] = "grey"
        login_button.place(relx=.32, rely=.65, relheight=.06, relwidth=.07)

        forgot_password_button = tk.Button(container, text="Forgot Password?",
                                            relief="flat", font=DEFAULT_BUTTON_FONT,
                                            bg=LOGIN_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR, #"#b9d5f0",
                                            command=lambda: self.forgot_password_view()
                                            )
        forgot_password_button["activeforeground"] = DEFAULT_FOREGROUND_COLOR
        forgot_password_button["activebackground"] = LOGIN_BACKGROUND_COLOR
        forgot_password_button.place(relx=.66, rely=.65, relheight=.06, relwidth=.16)
        container.place(relheight=1, relwidth=1)
            
        center_window(self.root, height=360, width=600)
        self.root.wm_protocol("WM_DELETE_WINDOW", lambda window=self.root: self.clean_exit(window=window, current_window="application"))
        self.root.wm_deiconify()
        self.set_login_entries(login_entries, tk.END)
        self.root.mainloop()

    def _next(self):
        self.login_user(self.root, self.username.get(), self.password.get(), self.index_view)

    def forgot_password_view(self):
        if self.forgot_password_view_window:
            self.forgot_password_view_window.wm_deiconify()
            return
        self.forgot_password_view_window = tk.Toplevel(master=self.root)
        self.forgot_password_view_window.wm_withdraw()
        self.root.withdraw()
        if WIN32:
            self.forgot_password_view_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)
            self.forgot_password_view_window.title(FORGOT_PASSWORD_WINDOW_TITLE)

        container = tk.Canvas(self.forgot_password_view_window, bg=LOGIN_BACKGROUND_COLOR)

        username = tk.StringVar()
        security_question = tk.StringVar()
        security_answer = tk.StringVar()
        password = tk.StringVar()

        heading_label = tk.Label(
                                    container, text="RECOVER USER PASSWORD", font=HEADER_FONT_1,
                                    bg=LOGIN_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR
                                    )
        heading_label.place(relx=.1, rely=.1, relheight=.08, relwidth=.8)

        username_label = tk.Label(
                                    container, anchor="e", text="Username",font=DEFAULT_FONT,
                                    bg=LOGIN_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR
                                )
        username_label.place(relx=.02, rely=.3, relheight=.0588, relwidth=.23)

        username_entry = tk.Entry(container, textvariable=username, width=45, font=DEFAULT_FONT)
        username_entry.place(relx=.3, rely=.3, relheight=.0588, relwidth=.5)
        username_entry.focus_set()

        security_question_label = tk.Label(container, anchor="e", text='Question', font=DEFAULT_FONT,
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        security_question_label.place(relx=.02, relwidth=.23, rely=.42, relheight=.0588)
        security_question.set(SECURITY_QUESTIONS[0])
        security_question = ttk.Combobox(container, textvariable=security_question, values=SECURITY_QUESTIONS, state="readonly", font=DROPDOWN_FONT)
        security_question.place(relx=.3, relwidth=.5, rely=.42, relheight=.0588)        
        
        security_answer_label = tk.Label(
                                        container, anchor="e", text='Answer', font=DEFAULT_FONT,
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        security_answer_label.place(relx=.02, relwidth=.23, rely=.54, relheight=.0588)
        security_answer_entry = tk.Entry(container, textvariable=security_answer, font=DEFAULT_FONT)
        security_answer_entry.place(relx=.3, relwidth=.5, rely=.54, relheight=.0588)  


        password_label = tk.Label(
                                    container, anchor="e", text="New Password", font=DEFAULT_FONT,
                                         bg=LOGIN_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR
                                )
        password_label.place(relx=.02, rely=.68, relheight=.0588, relwidth=.23)

        password_entry = tk.Entry(container, show='*', textvariable=password, font=DEFAULT_FONT)
        password_entry.place(relx=.3, rely=.68, relheight=.0588, relwidth=.5)

        change_password_button = tk.Button(container, text="Update", font=DEFAULT_BUTTON_FONT,
                                            command=lambda: self.update_password(
                                                self.forgot_password_view_window, username.get(), security_question.get(),
                                                security_answer.get(), password.get()
                                            )
                                )

        change_password_button["activeforeground"] = "white"
        change_password_button["activebackground"] = "grey"
        change_password_button.place(relx=.3, rely=.8, relheight=.06, relwidth=.07)

        container.place(relheight=1, relwidth=1)
        
        center_window(self.forgot_password_view_window, height=360, width=600)
        self.forgot_password_view_window.wm_protocol(
                                                    "WM_DELETE_WINDOW",
                                                    lambda: self.clean_exit(
                                                    window=self.forgot_password_view_window,
                                                    master=self.root,
                                                )
                                            )
        self.forgot_password_view_window.wm_deiconify()

    def index_view(self):
        if self.index_view_window:
            self.index_view_window.wm_deiconify()
            return
        self.index_view_window = tk.Toplevel(master=self.root)
        self.index_view_window.wm_withdraw()
        if WIN32:
            self.index_view_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)
            self.index_view_window.iconphoto(False, tk.PhotoImage(file=WINDOW_ICON_PHOTO_PATH))
        self.index_view_window.wm_title(INDEX_WINDOW_TITLE)
        container = tk.Canvas(self.index_view_window, bg=DEFAULT_BACKGROUND_COLOR)
        home_menu = tk.Menu(self.index_view_window)
        book_id = tk.StringVar()
        student_matric_number = tk.StringVar()

        self.date_time_label = ttk.Label(container)
        self.date_time_label.place(relx=.70, rely=.03, relwidth=.27, relheight=.047)
        self.date_time_label.configure(background=DEFAULT_BACKGROUND_COLOR)
        self.date_time_label.configure(foreground=DEFAULT_FOREGROUND_COLOR)
        self.date_time_label.configure(font="-family {Franklin Gothic Medium} -size 20 -weight bold -slant roman -underline 0 -overstrike 0")
        self.date_time_label.configure(borderwidth="2")
        self.date_time_label.configure(relief="ridge")
        self.date_time_label.configure(anchor='center')
        self.date_time_label.configure(justify='center')
        self.date_time_label.configure(compound='center')
        self.date_time_label.configure(text=get_current_time())
        self.date_time_label.after(1000, self.refresh_date_time_label)      

        heading_label = tk.Label(container, text=WINDOW_TITLE, fg='black', bg=DEFAULT_BACKGROUND_COLOR , font=HEADER_FONT)
        heading_label.place(relx=.1, rely=.08, relheight=.1, relwidth=.8)

        information_header = tk.Label(container, text="INFORMATION DETAILS",  font=('Arial', 15, 'underline', 'bold'), bg=DEFAULT_BACKGROUND_COLOR)
        information_header.place(relx=.3, rely=.22, relwidth=.4, relheight=.05)

        listTreestyle = ttk.Style()
        listTree = ttk.Treeview(container, columns=(0, 1, 2, 3, 4), show="headings")
        vsb = ttk.Scrollbar(container, orient="vertical", command=listTree.yview)
        listTree.configure(yscrollcommand=vsb.set)
        listTreestyle.configure('Treeview',  font=FONT_10)
        listTreestyle.configure('Treeview.Heading', font=FONT_10)        
        listTree.heading(0, text='Book ID', anchor ='center')
        listTree.column(0, width=50, minwidth=50, anchor='center')
        listTree.column(1, width=150, minwidth=150, anchor='center')
        listTree.heading(1, text='Matric No')
        listTree.heading(2, text='Student Name')
        listTree.column(2, width=250, minwidth=250, anchor='center')
        listTree.heading(3, text='Book Name')
        listTree.column(3, width=250, minwidth=250, anchor='center')
        listTree.heading(4, text='Date Issued')
        listTree.column(4, width=100, minwidth=100, anchor='center')
        listTree.place(relx=.05, rely=.3, relwidth=.9, relheight=.55)
        vsb.place(relx=.950005, rely=.3, relheight=.55)
        ttk.Style().configure("Treeview",font=('Times new Roman',15))
        self.set_transactions_information_viewer(listTree)
        self.populate_transactions_information_treeview(self.index_view_window)
        listTree.after(1000, self.refresh_information_treeview)

        book_id_label = tk.Label(container, anchor="w", text="BOOK ID", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        book_id_label.place(relx=.05, rely=.8658, relheight=.05, relwidth=.1)
        book_id_entry = tk.Entry(container, textvariable=book_id, font=INDEX_ENTRY_FONT)
        book_id_entry.place(relx=.14, rely=.87, relheight=.04, relwidth=.04)
        book_id_entry.focus_set()

        student_matric_number_label = tk.Label(container, anchor="w", text="MATRIC NUMBER", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        student_matric_number_label.place(relx=.2, rely=.8658, relheight=.05, relwidth=.16)
        student_matric_number_entry = tk.Entry(container, textvariable=student_matric_number, font=INDEX_ENTRY_FONT)
        student_matric_number_entry.place(relx=.37, rely=.87, relheight=.04, relwidth=.1)

        search_transactions_button = tk.Button(
                                        container, font=DEFAULT_FONT,
                                        bg="#518f45", text='SEARCH',
                                        command=lambda: self.search_transactions(self.index_view_window, book_id.get(), student_matric_number.get())
                                        )
        search_transactions_button.place(relx=.49, rely=.87, relheight=.04, relwidth=.06)

        clear_transactions_button = tk.Button(self.index_view_window, font=DEFAULT_FONT,
                                                bg="#d36d6d", text="CLEAR", command=lambda: self.clear_searched_transactions(

                                                    (book_id_entry, student_matric_number_entry),
                                                    (book_id, student_matric_number)
                                                )
                                            )
        clear_transactions_button.place(relx=.57, rely=.87, relheight=.04, relwidth=.06)


        librarian_sub_menu = tk.Menu(self.index_view_window)
        librarian_sub_menu.add_command(label="Issue Book", command=self.issue_book_view)
        librarian_sub_menu.add_command(label="Retrieve Book", command=self.retrieve_book_view)

        information_sub_menu = tk.Menu(self.index_view_window)
        information_sub_menu.add_command(label="View Students", command=self.students_information_view)
        information_sub_menu.add_command(label="View Books", command=self.books_information_view)
        information_sub_menu.add_command(label="View Users", command=self.users_information_view)        

        home_menu.add_cascade(label='Information Tools', menu=information_sub_menu)
        home_menu.add_cascade(label='Librarian Tools', menu=librarian_sub_menu)

        if self.is_admin.get():
            admin_sub_menu = tk.Menu(self.index_view_window)
            admin_sub_menu.add_command(label="Register Student", command=self.register_student_view)
            admin_sub_menu.add_command(label="Add Book", command=self.add_book_view)
            admin_sub_menu.add_command(label="Create User", command=self.create_user_view)
            admin_sub_menu.add_command(label="Unregister Student", command=self.unregister_student_view)
            admin_sub_menu.add_command(label="Remove Book", command=self.remove_book_view)
            admin_sub_menu.add_command(label="Delete User", command=self.delete_user_view)
            home_menu.add_cascade(label='Admin Tools', menu=admin_sub_menu)
        
        self.index_view_window.config(menu=home_menu)
        container.place(relheight=1, relwidth=1)
        
        self.index_view_window.wm_attributes("-zoomed", True)
        self.index_view_window.wm_resizable(False, False)
        self.index_view_window.wm_protocol("WM_DELETE_WINDOW",
                                        lambda: self.clean_exit(
                                                                        window=self.index_view_window,
                                                                        master=self.root,
                                                                        current_window = "home"
                                                                        )
                                                                    )
        self.root.withdraw()
        self.index_view_window.wm_deiconify()

    def refresh_date_time_label(self):
        # display the new time
        self.date_time_label.configure(text=get_current_time())
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.date_time_label.after(1000, self.refresh_date_time_label)

    def refresh_information_treeview(self, event=None):
        if not self.searching_transactions.get():
            self.depopulate_transactions_information_treeview()
            self.populate_transactions_information_treeview(self.index_view_window)
        self.transactions_information_viewer.after(1000, self.refresh_information_treeview)

    def students_information_view(self):
        if self.students_information_window:
            self.students_information_window.wm_deiconify()
            return
        self.students_information_window = tk.Toplevel(master=self.index_view_window)
        self.students_information_window.wm_withdraw()
        self.students_information_window.title(STUDENTS_INFORMATION_WINDOW_TITLE)
        if WIN32:
            self.students_information_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)
        container = tk.Canvas(self.students_information_window, bg=DEFAULT_BACKGROUND_COLOR)
        home_menu = tk.Menu(self.students_information_window)
        student_name = tk.StringVar()
        student_matric_number = tk.StringVar()

        students_information_header = tk.Label(container, text="REGISTERED STUDENTS",  font=HEADER_FONT, bg=DEFAULT_BACKGROUND_COLOR)
        students_information_header.place(relx=.1, rely=.05, relwidth=.8, relheight=.1)

        students_list_treestyle = ttk.Style()
        students_list_tree = ttk.Treeview(container, columns=(0, 1, 2, 3, 4), show="headings")
        vsb = ttk.Scrollbar(container, orient="vertical", command=students_list_tree.yview)
        students_list_tree.configure(yscrollcommand=vsb.set)
        students_list_treestyle.configure('Treeview',  font=FONT_10)
        students_list_treestyle.configure('Treeview.Heading', font=FONT_10)        
        students_list_tree.heading(0, text='Matric No', anchor ='center')
        students_list_tree.column(0, width=60, minwidth=60, anchor='center')
        students_list_tree.heading(1, text='Student Name')
        students_list_tree.column(1, width=250, minwidth=150, anchor='center')
        students_list_tree.heading(2, text='Department')
        students_list_tree.column(2, width=250, minwidth=250, anchor='center')
        students_list_tree.heading(3, text='Date Registered')
        students_list_tree.column(3, width=100, minwidth=100, anchor='center')
        students_list_tree.heading(4, text='Registrar')
        students_list_tree.column(4, width=100, minwidth=100, anchor='center')
        students_list_tree.place(relx=.05, rely=.2, relwidth=.9, relheight=.65)
        vsb.place(relx=.950005, rely=.2, relheight=.65)
        ttk.Style().configure("Treeview",font=('Times new Roman',15))
        self.set_students_information_viewer(students_list_tree)
        self.populate_students_information_treeview(self.students_information_window)

        student_name_label = tk.Label(container, anchor="w", text="STUDENT NAME", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        student_name_label.place(relx=.05, rely=.8658, relheight=.05, relwidth=.15)
        student_name_entry = tk.Entry(container, textvariable=student_name, font=INDEX_ENTRY_FONT)
        student_name_entry.place(relx=.205, rely=.87, relheight=.04, relwidth=.2)
        student_name_entry.focus_set()

        student_matric_number_label = tk.Label(container, anchor="w", text="MATRIC NUMBER", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        student_matric_number_label.place(relx=.42, rely=.8658, relheight=.05, relwidth=.16)
        student_matric_number_entry = tk.Entry(container, textvariable=student_matric_number, font=INDEX_ENTRY_FONT)
        student_matric_number_entry.place(relx=.59, rely=.87, relheight=.04, relwidth=.1)

        search_students_information_button = tk.Button(container, font=DEFAULT_FONT,
                                        bg="#518f45", text='SEARCH',
                                        command=lambda: self.search_students(
                                            self.students_information_window,
                                            student_matric_number,
                                            student_name,
                                        )
                                    )
        search_students_information_button.place(relx=.71, rely=.87, relheight=.04, relwidth=.06)

        clear_students_information_button = tk.Button(self.students_information_window,
                                font=DEFAULT_FONT, bg="#d36d6d", text="CLEAR",
                                command=lambda: self.clear_searched_students(
                                    self.students_information_window,
                                    (student_matric_number_entry, student_name_entry),
                                    (student_name, student_matric_number)
                                )
                            )
        clear_students_information_button.place(relx=.785, rely=.87, relheight=.04, relwidth=.06)

        container.place(relheight=1, relwidth=1)
        self.students_information_window.wm_attributes("-zoomed", True)
        self.students_information_window.wm_resizable(False, False)
        self.students_information_window.wm_protocol("WM_DELETE_WINDOW",
                                        lambda: self.clean_exit(
                                                                        window=self.students_information_window,
                                                                        index_window=self.index_view_window,
                                                                        )
                                                                    )
        self.students_information_window.wm_deiconify()
        self.index_view_window.wm_withdraw()

    def books_information_view(self):
        if self.books_information_window:
            self.books_information_window.wm_deiconify()
            return
        self.books_information_window = tk.Toplevel(master=self.index_view_window)
        self.books_information_window.wm_withdraw()
        if WIN32:
            self.books_information_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)
        container = tk.Canvas(self.books_information_window, bg=DEFAULT_BACKGROUND_COLOR)
        home_menu = tk.Menu(self.books_information_window)
        book_id = tk.StringVar()
        book_title = tk.StringVar()

        books_information_header = tk.Label(container, text="BOOKS IN LIBRARY",  font=HEADER_FONT, bg=DEFAULT_BACKGROUND_COLOR)
        books_information_header.place(relx=.1, rely=.05, relwidth=.8, relheight=.1)

        books_list_treestyle = ttk.Style()
        books_list_tree = ttk.Treeview(container, columns=(0, 1, 2, 3, 4), show="headings")
        vsb = ttk.Scrollbar(container, orient="vertical", command=books_list_tree.yview)
        books_list_tree.configure(yscrollcommand=vsb.set)
        books_list_treestyle.configure('Treeview',  font=FONT_10)
        books_list_treestyle.configure('Treeview.Heading', font=FONT_10)        
        books_list_tree.heading(0, text='Book ID', anchor ='center')
        books_list_tree.column(0, width=50, minwidth=50, anchor='center')
        books_list_tree.heading(1, text='Book Name')
        books_list_tree.column(1, width=250, minwidth=250, anchor='center')
        books_list_tree.heading(2, text='Author Name')
        books_list_tree.column(2, width=250, minwidth=250, anchor='center')
        books_list_tree.heading(3, text='Available Books')
        books_list_tree.column(3, width=50, minwidth=50, anchor='center')
        books_list_tree.heading(4, text='Total Books')
        books_list_tree.column(4, width=50, minwidth=50, anchor='center')
        books_list_tree.place(relx=.05, rely=.3, relwidth=.9, relheight=.55)
        vsb.place(relx=.950005, rely=.3, relheight=.55)
        ttk.Style().configure("Treeview",font=('Times new Roman',15), padding=.05)
        self.set_books_information_viewer(books_list_tree)
        self.populate_books_information_treeview(self.books_information_window)

        book_id_label = tk.Label(container, anchor="w", text="BOOK ID", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        book_id_label.place(relx=.05, rely=.8658, relheight=.05, relwidth=.1)
        book_id_entry = tk.Entry(container, textvariable=book_id, font=INDEX_ENTRY_FONT)
        book_id_entry.place(relx=.14, rely=.87, relheight=.04, relwidth=.04)
        book_id_entry.focus_set()

        book_name_label = tk.Label(container, anchor="w", text="BOOK NAME", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        book_name_label.place(relx=.2, rely=.8658, relheight=.05, relwidth=.16)
        book_name_entry = tk.Entry(container, textvariable=book_title, font=INDEX_ENTRY_FONT)
        book_name_entry.place(relx=.32, rely=.87, relheight=.04, relwidth=.2)

        books_information_button = tk.Button(container, font=DEFAULT_FONT, bg="#518f45", text='SEARCH')
        books_information_button.place(relx=.545, rely=.87, relheight=.04, relwidth=.06)

        books_information_button = tk.Button(self.books_information_window, font=DEFAULT_FONT, bg="#d36d6d", text="CLEAR")
        books_information_button.place(relx=.625, rely=.87, relheight=.04, relwidth=.06)

        container.place(relheight=1, relwidth=1)
        
        container.place(relheight=1, relwidth=1)
        self.books_information_window.wm_attributes("-zoomed", True)
        self.books_information_window.wm_resizable(False, False)
        self.books_information_window.wm_protocol("WM_DELETE_WINDOW",
                                        lambda: self.clean_exit(
                                                                        window=self.books_information_window,
                                                                        index_window=self.index_view_window,
                                                                        )
                                                                    )
        self.books_information_window.wm_deiconify()
        self.index_view_window.wm_withdraw()

    def users_information_view(self):
        if self.users_information_window:
            self.users_information_window.wm_deiconify()
            return
        self.users_information_window = tk.Toplevel(master=self.index_view_window)
        self.users_information_window.wm_withdraw()
        if WIN32:
            self.users_information_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)
        container = tk.Canvas(self.users_information_window, bg=DEFAULT_BACKGROUND_COLOR)
        home_menu = tk.Menu(self.users_information_window)
        user_id = tk.StringVar()
        username = tk.StringVar()

        users_information_header = tk.Label(container, text="AUTHENTICATED USERS ",  font=HEADER_FONT, bg=DEFAULT_BACKGROUND_COLOR)
        users_information_header.place(relx=.1, rely=.05, relwidth=.8, relheight=.1)

        users_list_treestyle = ttk.Style()
        users_list_tree = ttk.Treeview(container, columns=(0, 1, 2, 3, 4, 5), show="headings")
        vsb = ttk.Scrollbar(container, orient="vertical", command=users_list_tree.yview)
        users_list_tree.configure(yscrollcommand=vsb.set)
        users_list_treestyle.configure('Treeview',  font=FONT_10)
        users_list_treestyle.configure('Treeview.Heading', font=FONT_10)        
        users_list_tree.heading(0, text='User ID', anchor ='center')
        users_list_tree.column(0, width=50, minwidth=50, anchor='center')
        users_list_tree.heading(1, text='User Name')
        users_list_tree.column(1, width=150, minwidth=150, anchor='center')
        users_list_tree.heading(2, text='User Full Name')
        users_list_tree.column(2, width=250, minwidth=250, anchor='center') 
        users_list_tree.heading(3, text='Admin status')
        users_list_tree.column(3, width=100, minwidth=100, anchor='center')       
        users_list_tree.heading(4, text='Date created')
        users_list_tree.column(4, width=100, minwidth=100, anchor='center')
        users_list_tree.heading(5, text='Creator')
        users_list_tree.column(5, width=100, minwidth=100, anchor='center')    
        users_list_tree.place(relx=.05, rely=.3, relwidth=.9, relheight=.55)
        vsb.place(relx=.950005, rely=.3, relheight=.55)
        ttk.Style().configure("Treeview",font=('Times new Roman',15))
        self.set_users_information_viewer(users_list_tree)
        self.populate_users_information_treeview(self.users_information_window)

        user_id_label = tk.Label(container, anchor="w", text="BOOK ID", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        user_id_label.place(relx=.05, rely=.8658, relheight=.05, relwidth=.1)
        user_id_entry = tk.Entry(container, textvariable=user_id, font=INDEX_ENTRY_FONT)
        user_id_entry.place(relx=.14, rely=.87, relheight=.04, relwidth=.04)
        user_id_entry.focus_set()

        user_name_label = tk.Label(container, anchor="w", text="BOOK NAME", bg=DEFAULT_BACKGROUND_COLOR , font=INDEX_LABEL_FONT)
        user_name_label.place(relx=.2, rely=.8658, relheight=.05, relwidth=.16)
        user_name_entry = tk.Entry(container, textvariable=username, font=INDEX_ENTRY_FONT)
        user_name_entry.place(relx=.37, rely=.87, relheight=.04, relwidth=.1)

        users_information_button = tk.Button(container, font=DEFAULT_FONT, bg="#518f45", text='SEARCH')
        users_information_button.place(relx=.49, rely=.87, relheight=.04, relwidth=.06)

        users_information_button = tk.Button(self.users_information_window, font=DEFAULT_FONT, bg="#d36d6d", text="CLEAR")
        users_information_button.place(relx=.57, rely=.87, relheight=.04, relwidth=.06)

        container.place(relheight=1, relwidth=1)
        
        container.place(relheight=1, relwidth=1)
        self.users_information_window.wm_attributes("-zoomed", True)
        self.users_information_window.wm_resizable(False, False)
        self.users_information_window.wm_protocol("WM_DELETE_WINDOW",
                                        lambda: self.clean_exit(
                                                                        window=self.users_information_window,
                                                                        index_window=self.index_view_window,
                                                                        )
                                                                    )
        self.users_information_window.wm_deiconify()
        self.index_view_window.wm_withdraw()

    def register_student_view(self):
        if self.register_student_window:
            self.register_student_window.wm_deiconify()
            return
        self.register_student_window = tk.Toplevel(master=self.index_view_window)
        self.register_student_window.wm_withdraw()
        self.register_student_window.title(REGISTER_STUDENT_WINDOW_TITLE)
        if WIN32:
            self.register_student_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(master=self.register_student_window, bg=DEFAULT_BACKGROUND_COLOR)
        student_name = tk.StringVar()
        student_matric_number = tk.StringVar()
        department = tk.StringVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='REGISTER STUDENT', bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2)
        main_heading_label.place(relx=.2525, relwidth=.55, rely=.03, relheight=.085)

        student_name_label = tk.Label(
                                        container, anchor="e", text='Student Name', font=DEFAULT_LABEL_FONT,
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        student_name_label.place(relx=.08, relwidth=.22, rely=.2, relheight=.05)
        student_name_entry = tk.Entry(container, textvariable=student_name, font=DEFAULT_FONT)
        student_name_entry.place(relx=.35, relwidth=.45, rely=.2, relheight=.05)
        student_name_entry.focus_set()
        
        student_matric_number_label = tk.Label(
                                        container, anchor="e", text='Matric No.', font=DEFAULT_LABEL_FONT,
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        student_matric_number_label.place(relx=.08, relwidth=.22, rely=.3, relheight=.05)
        student_matric_number_entry = tk.Entry(container, textvariable=student_matric_number, font=DEFAULT_FONT)
        student_matric_number_entry.place(relx=.35, relwidth=.45, rely=.3, relheight=.05)

        department_label = tk.Label(
                                        container, anchor="e", text='Department', font=DEFAULT_LABEL_FONT,
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        department_label.place(relx=.08, relwidth=.22, rely=.4, relheight=.05)
        department.set(DEPARTMENT_CHOICE_LIST[0])
        department_entry = ttk.Combobox(container, textvariable=department, values=DEPARTMENT_CHOICE_LIST, state="readonly", font=DROPDOWN_FONT)
        department_entry.place(relx=.35, relwidth=.45, rely=.4, relheight=.05)  

        register_student_button = tk.Button(container, text="Register", font=DEFAULT_FONT, bg=DEFAULT_BACKGROUND_COLOR,
                                            command=lambda:self.register_student(self.register_student_window, registrar=self.username.get(),
                                            student_name=student_name.get(), student_matric_number=student_matric_number.get(),
                                            department=department.get(), date_registered=get_current_date()
                                        )
                                    )
        register_student_button.place(relx=.35, relwidth=.2, rely=.5, relheight=.07)         

        container.place(relheight=1, relwidth=1)
        center_window(self.register_student_window, height=400, width=480)
        self._next_modal(self.index_view_window, self.register_student_window)
        self.register_student_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.register_student_window, self.index_view_window))
        self.register_student_window.wm_deiconify()

    def add_book_view(self):
        if self.add_book_window:
            self.add_book_window.wm_deiconify()
            return
        self.add_book_window = tk.Toplevel(master=self.index_view_window)
        self.add_book_window.wm_withdraw()
        self.add_book_window.title(ADD_BOOK_WINDOW_TITLE)
        if WIN32:
            self.add_book_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(master=self.add_book_window, bg=DEFAULT_BACKGROUND_COLOR)
        book_id = tk.StringVar()
        book_name = tk.StringVar()
        book_author = tk.StringVar()
        number_of_copies = tk.StringVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='ADD BOOK', bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2)
        main_heading_label.place(relx=.325, relwidth=.5, rely=.03, relheight=.085)

        book_id_label = tk.Label(
                                        container, anchor="e", text='Book ID', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        book_id_label.place(relx=.1, relwidth=.22, rely=.2, relheight=.05)
        book_id_entry = tk.Entry(container, textvariable=book_id, font=DEFAULT_FONT)
        book_id_entry.place(relx=.35, relwidth=.45, rely=.2, relheight=.05)
        book_id_entry.focus_set()

        book_name_label = tk.Label(
                                        container, anchor="e", text='Book Name', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        book_name_label.place(relx=.1, relwidth=.22, rely=.3, relheight=.05)
        book_name_entry = tk.Entry(container, textvariable=book_name, font=DEFAULT_FONT)
        book_name_entry.place(relx=.35, relwidth=.45, rely=.3, relheight=.05)

        book_author_label = tk.Label(
                                        container, anchor="e", text='Author', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        book_author_label.place(relx=.1, relwidth=.22, rely=.4, relheight=.05)
        book_author_entry = tk.Entry(container, textvariable=book_author, font=DEFAULT_FONT)
        book_author_entry.place(relx=.35, relwidth=.45, rely=.4, relheight=.05) 

        number_of_copies.set(1)
        number_of_copies_label = tk.Label(
                                        container, anchor="e", text='No. Of Copies', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        number_of_copies_label.place(relx=.1, relwidth=.22, rely=.5, relheight=.05)
        number_of_copies_entry = tk.Entry(container, textvariable=number_of_copies, font=DEFAULT_FONT)
        number_of_copies_entry.place(relx=.35, relwidth=.45, rely=.5, relheight=.05)  

        add_book = tk.Button(container, text="Add Book", font=DEFAULT_FONT, bg=DEFAULT_BACKGROUND_COLOR,
                                command=lambda: self.add_book(self.add_book_window, book_id=book_id.get(),
                                        book_name=book_name.get(), book_author=book_author.get(), number_of_copies=number_of_copies.get()
                                    )
                                )
        add_book.place(relx=.35, relwidth=.2, rely=.6, relheight=.07)         

        container.place(relheight=1, relwidth=1)
        center_window(self.add_book_window, height=400, width=480)
        self._next_modal(self.index_view_window, self.add_book_window)
        self.add_book_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.add_book_window, self.index_view_window))
        self.add_book_window.wm_deiconify()

    def create_user_view(self):
        if self.create_user_window:
            self.create_user_window.wm_deiconify()
            self.create_user_window.focus_set()
            return
        self.create_user_window = tk.Toplevel(master=self.index_view_window)
        self.create_user_window.wm_withdraw()
        self.create_user_window.title(CREATE_USER_WINDOW_TITLE)
        if WIN32:
            self.create_user_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(master=self.create_user_window, bg=DEFAULT_BACKGROUND_COLOR)

        user_id = tk.StringVar()
        user_full_name = tk.StringVar()
        user_name = tk.StringVar()
        user_password = tk.StringVar()
        security_question = tk.StringVar()
        security_answer = tk.StringVar()
        admin_status = tk.BooleanVar()
        __show = tk.BooleanVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='CREATE USER', bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2)
        main_heading_label.place(relx=.2525, relwidth=.55, rely=.03, relheight=.085)

        user_id_label = tk.Label(
                                        container, anchor="e", text='User ID', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        user_id_label.place(relx=.1, relwidth=.22, rely=.2, relheight=.05)
        user_id_entry = tk.Entry(container, textvariable=user_id, font=DEFAULT_FONT)
        user_id_entry.place(relx=.35, relwidth=.45, rely=.2, relheight=.05)
        user_id_entry.focus_set()

        user_full_name_label = tk.Label(
                                        container, anchor="e", text='Full Name', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        user_full_name_label.place(relx=.1, relwidth=.22, rely=.3, relheight=.05)
        user_full_name_entry = tk.Entry(container, textvariable=user_full_name, font=DEFAULT_FONT)
        user_full_name_entry.place(relx=.35, relwidth=.45, rely=.3, relheight=.05)

        user_name_label = tk.Label(
                                        container, anchor="e", text='Username', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        user_name_label.place(relx=.1, relwidth=.22, rely=.4, relheight=.05)
        user_name_entry = tk.Entry(container, textvariable=user_name, font=DEFAULT_FONT)
        user_name_entry.place(relx=.35, relwidth=.45, rely=.4, relheight=.05)

        user_password_label = tk.Label(
                                        container, anchor="e", text='Password', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        user_password_label.place(relx=.1, relwidth=.22, rely=.5, relheight=.05)
        user_password_entry = tk.Entry(container, show="*", textvariable=user_password, font=DEFAULT_FONT)
        user_password_entry.place(relx=.35, relwidth=.45, rely=.5, relheight=.05)

        # show_status_checkbox = tk.Checkbutton(
        #                                         container, variable=__show, onvalue=True, offvalue=False,
        #                                         fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR,
        #                                         command=lambda: show(user_password_entry, __show),
        #                                         activebackground=DEFAULT_BACKGROUND_COLOR, activeforeground=DEFAULT_FOREGROUND_COLOR)
        # show_status_checkbox.place(relx=.77, rely=.5, relwidth=.05, relheight=.05)        

        security_question_label = tk.Label(container, anchor="e", text='Question', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        security_question_label.place(relx=.1, relwidth=.22, rely=.6, relheight=.05)
        security_question.set(SECURITY_QUESTIONS[0])
        security_question = ttk.Combobox(container, textvariable=security_question, values=SECURITY_QUESTIONS, state="readonly")
        security_question.place(relx=.35, relwidth=.45, rely=.6, relheight=.05)        
        
        security_answer_label = tk.Label(
                                        container, anchor="e", text='Answer', font=('Comic Scan Ms', 10, 'bold'),
                                        bg=DEFAULT_BACKGROUND_COLOR
                                )
        security_answer_label.place(relx=.1, relwidth=.22, rely=.7, relheight=.05)
        security_answer_entry = tk.Entry(container, textvariable=security_answer, font=DEFAULT_FONT)
        security_answer_entry.place(relx=.35, relwidth=.45, rely=.7, relheight=.05)

        admin_status_text = tk.Label(container, text="Grant admin rights?", bg=DEFAULT_BACKGROUND_COLOR, fg=DEFAULT_FOREGROUND_COLOR)
        admin_status_text.place(relx=.54, rely=.8, relwidth=.23)

        admin_status_checkbox = tk.Checkbutton(
                                                container, variable=admin_status, onvalue=True, offvalue=False,
                                                fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR,
                                                activebackground=DEFAULT_BACKGROUND_COLOR, activeforeground=DEFAULT_FOREGROUND_COLOR)
        admin_status_checkbox.place(relx=.77, rely=.8, relwidth=.05, relheight=.05)

        create_user_button = tk.Button(
                                            container, text="Register", font=DEFAULT_FONT, bg=DEFAULT_BACKGROUND_COLOR,
                                            command=lambda: self.create_user(self.create_user_window, user_id=user_id.get(), user_name=user_name.get(),
                                            user_full_name=user_full_name.get(), user_password=user_password.get(),admin_status=admin_status.get(),
                                            security_question=security_question.get(), security_answer=security_answer.get()
                                        )
                                    )
        create_user_button.place(relx=.35, relwidth=.15, rely=.8, relheight=.07)         

        container.place(relheight=1, relwidth=1)
        center_window(self.create_user_window, height=400, width=480)
        self._next_modal(self.index_view_window, self.create_user_window)
        self.create_user_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.create_user_window, self.index_view_window))        
        self.create_user_window.wm_deiconify()

    def unregister_student_view(self):
        if self.unregister_student_window:
            self.unregister_student_window.wm_deiconify()
            return
        self.unregister_student_window = tk.Toplevel(master=self.root)
        self.unregister_student_window.wm_withdraw()
        self.unregister_student_window.title(UNREGISTER_STUDENT_WINDOW_TITLE)
        if WIN32:
            self.unregister_student_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(self.unregister_student_window, bg=DEFAULT_BACKGROUND_COLOR)
        student_matric_number = tk.StringVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='UNREGISTER STUDENT', fg=DEFAULT_FOREGROUND_COLOR,
                                        bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2
                                )
        main_heading_label.place(relx=.1, relwidth=.8, rely=.07, relheight=.2)

        student_matric_number_label = tk.Label(
                                        container, anchor="e", text='Matric No.', font=DEFAULT_LABEL_FONT,
                                        fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR
                                )
        student_matric_number_label.place(relx=.05, relwidth=.2, rely=.35, relheight=.1)
        student_matric_number_entry = tk.Entry(container, textvariable=student_matric_number, font=DEFAULT_FONT)
        student_matric_number_entry.place(relx=.3, relwidth=.5, rely=.35, relheight=.1)
        student_matric_number_entry.focus_set()

        unregister_student = tk.Button(container, text="Unregister", font=DEFAULT_FONT,
                                    fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR,
                                    command=lambda: self.unregister_student(self.unregister_student_window,
                                    student_matric_number=student_matric_number.get())
                                    )
        unregister_student.place(relx=.3, relwidth=.17, rely=.5, relheight=.1)         

        container.place(relheight=1, relwidth=1)
        center_window(self.unregister_student_window, height=200, width=480)
        self._next_modal(self.index_view_window, self.unregister_student_window)
        self.unregister_student_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.unregister_student_window, self.index_view_window))
        self.unregister_student_window.wm_deiconify()       

    def remove_book_view(self):
        if self.remove_book_window:
            self.remove_book_window.wm_deiconify()
            return
        self.remove_book_window = tk.Toplevel(master=self.root)
        self.remove_book_window.wm_withdraw()
        self.remove_book_window.title(REMOVE_BOOK_WINDOW_TITLE)
        if WIN32:
            self.remove_book_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(master=self.remove_book_window, bg=DEFAULT_BACKGROUND_COLOR)
        book_id = tk.StringVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='REMOVE BOOK', fg=DEFAULT_FOREGROUND_COLOR,
                                        bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2
                                )
        main_heading_label.place(relx=.25, relwidth=.6, rely=.07, relheight=.2)

        book_id_label = tk.Label(
                                        container, anchor="e", text='Book ID', font=DEFAULT_LABEL_FONT,
                                        fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR
                                )
        book_id_label.place(relx=.05, relwidth=.2, rely=.35, relheight=.1)
        book_id_entry = tk.Entry(container, textvariable=book_id, font=DEFAULT_FONT)
        book_id_entry.place(relx=.3, relwidth=.5, rely=.35, relheight=.1)
        book_id_entry.focus_set()

        remove_book = tk.Button(container, text="Remove", font=DEFAULT_FONT,
                                    fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR,
                                    command=lambda: self.remove_book(self.remove_book_window, book_id.get())
                                    )
        remove_book.place(relx=.3, relwidth=.15, rely=.5, relheight=.1)         

        container.place(relheight=1, relwidth=1)
        center_window(self.remove_book_window, height=200, width=480)
        self._next_modal(self.index_view_window, self.remove_book_window)
        self.remove_book_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.remove_book_window, self.index_view_window))
        self.remove_book_window.wm_deiconify()

    def delete_user_view(self):
        if self.delete_user_window:
            self.delete_user_window.wm_deiconify()
            return
        self.delete_user_window = tk.Toplevel(master=self.root)
        self.delete_user_window.wm_withdraw()
        self.delete_user_window.title(DELETE_USER_WINDOW_TITLE)
        if WIN32:
            self.delete_user_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(self.delete_user_window, bg=DEFAULT_BACKGROUND_COLOR)
        user_id = tk.StringVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='DELETE USER', fg=DEFAULT_FOREGROUND_COLOR,
                                        bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2
                                )
        main_heading_label.place(relx=.25, relwidth=.6, rely=.07, relheight=.2)

        user_id_label = tk.Label(
                                        container, anchor="e", text='User ID', font=DEFAULT_LABEL_FONT,
                                        fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR
                                )
        user_id_label.place(relx=.05, relwidth=.2, rely=.35, relheight=.1)
        user_id_entry = tk.Entry(container, textvariable=user_id, font=DEFAULT_FONT)
        user_id_entry.place(relx=.3, relwidth=.5, rely=.35, relheight=.1)
        user_id_entry.focus_set()

        delete_user_button = tk.Button(container, text="Delete", font=DEFAULT_FONT,
                                    fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR,
                                    command=lambda: self.delete_user(self.delete_user_window, user_id.get())
                                    )
        delete_user_button.place(relx=.3, relwidth=.15, rely=.5, relheight=.1)   
              
        container.place(relheight=1, relwidth=1)
        center_window(self.delete_user_window, height=200, width=480)
        self._next_modal(self.index_view_window, self.delete_user_window)
        self.delete_user_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.delete_user_window, self.index_view_window))
        self.delete_user_window.wm_deiconify()

    def issue_book_view(self):
        if self.issue_book_window:
            self.issue_book_window.wm_deiconify()
            return
        self.issue_book_window = tk.Toplevel(master=self.index_view_window)
        self.issue_book_window.wm_withdraw()
        self.issue_book_window.title(ISSUE_BOOK_WINDOW_TITLE)
        if WIN32:
            self.issue_book_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(master=self.issue_book_window, bg=DEFAULT_BACKGROUND_COLOR)
        book_id = tk.StringVar()
        student_matric_number = tk.StringVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='ISSUE BOOK', fg=DEFAULT_FOREGROUND_COLOR,
                                        bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2
                                )
        main_heading_label.place(relx=.25, relwidth=.6, rely=.07, relheight=.2)

        book_id_label = tk.Label(
                                        container, anchor="e", text='Book ID', font=DEFAULT_LABEL_FONT,
                                        fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR
                                )
        book_id_label.place(relx=.05, relwidth=.2, rely=.35, relheight=.1)
        book_id_entry = tk.Entry(container, textvariable=book_id, font=DEFAULT_FONT)
        book_id_entry.place(relx=.3, relwidth=.5, rely=.35, relheight=.1)
        book_id_entry.focus_set()

        student_matric_number_label = tk.Label(
                                                container, anchor="e", text='Matric No.', font=DEFAULT_LABEL_FONT,
                                                fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR
                                        )
        student_matric_number_label.place(relx=.05, relwidth=.2, rely=.5, relheight=.1)
        student_matric_number_entry = tk.Entry(container, textvariable=student_matric_number, font=DEFAULT_FONT)
        student_matric_number_entry.place(relx=.3, relwidth=.5, rely=.5, relheight=.1)


        issue_book_button = tk.Button(container, text="Issue Book", font=DEFAULT_FONT,
                                    fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR,
                                    command=lambda: self.issue_book(self.issue_book_window, book_id=book_id.get(), 
                                    student_matric_number=student_matric_number.get(), current_date=get_current_date)
                                    )
        issue_book_button.place(relx=.3, relwidth=.2, rely=.65, relheight=.1)         

        container.place(relheight=1, relwidth=1)
        center_window(self.issue_book_window, height=200, width=480)  
        self._next_modal(self.index_view_window, self.issue_book_window)
        self.issue_book_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.issue_book_window, self.index_view_window))
        self.issue_book_window.wm_deiconify()

    def retrieve_book_view(self):
        if self.retrieve_book_window:
            self.retrieve_book_window.wm_deiconify()
            return
        self.retrieve_book_window = tk.Toplevel(master=self.index_view_window)
        self.retrieve_book_window.wm_withdraw()
        self.retrieve_book_window.title(ISSUE_BOOK_WINDOW_TITLE)
        if win32:
            self.retrieve_book_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

        container = tk.Canvas(master=self.retrieve_book_window, bg=DEFAULT_BACKGROUND_COLOR)
        book_id = tk.StringVar()
        student_matric_number = tk.StringVar()

        # # label and input box
        main_heading_label = tk.Label(container, text='RETRIEVE BOOK', fg=DEFAULT_FOREGROUND_COLOR,
                                        bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2
                                )
        main_heading_label.place(relx=.25, relwidth=.6, rely=.07, relheight=.2)

        book_id_label = tk.Label(
                                        container, anchor="e", text='Book ID', font=DEFAULT_LABEL_FONT,
                                        fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR
                                )
        book_id_label.place(relx=.05, relwidth=.2, rely=.35, relheight=.1)
        book_id_entry = tk.Entry(container, textvariable=book_id, font=DEFAULT_FONT)
        book_id_entry.place(relx=.3, relwidth=.5, rely=.35, relheight=.1)
        book_id_entry.focus_set()

        student_matric_number_label = tk.Label(
                                        container, anchor="e", text='Matric No.', font=DEFAULT_LABEL_FONT,
                                        fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR
                                )
        student_matric_number_label.place(relx=.05, relwidth=.2, rely=.5, relheight=.1)
        issue_name_entry = tk.Entry(container, textvariable=student_matric_number, font=DEFAULT_FONT)
        issue_name_entry.place(relx=.3, relwidth=.5, rely=.5, relheight=.1)


        retrieve_book_button = tk.Button(container, text="Retrieve Book", font=DEFAULT_FONT,
                                    fg=DEFAULT_FOREGROUND_COLOR, bg=DEFAULT_BACKGROUND_COLOR,
                                    command=lambda: self.retrieve_book(self.retrieve_book_window, book_id=book_id.get(), 
                                    student_matric_number=student_matric_number.get())
                                    )
        retrieve_book_button.place(relx=.3, relwidth=.2, rely=.65, relheight=.1)         

        container.place(relheight=1, relwidth=1)
        center_window(self.retrieve_book_window, height=200, width=480)
        self.retrieve_book_window.wm_protocol("WM_DELETE_WINDOW", lambda: self._release_modal(self.retrieve_book_window, self.index_view_window))
        self._next_modal(self.index_view_window, self.retrieve_book_window)
        self.retrieve_book_window.wm_deiconify()

    @staticmethod
    def fileDialog(registrar):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select A File",filetype = (("jpeg","*.jpg"),("png","*.png"),("All Files","*.*")))
        registrar.set(filename)
