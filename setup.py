import os
import sys
from tkinter import messagebox as _msgbox
from tkinter import filedialog
import tkinter as tk
from utils import center_window, get_current_date, show
from tkinter import ttk
from backends import BaseManager
from constants import *
from datetime import datetime
from db import PostgresConnect

def database_setup():
    index_view_window = tk.Tk()
    index_view_window.withdraw()
    create_user_window = tk.Toplevel(master=index_view_window)
    create_user_window.wm_withdraw()
    create_user_window.title(DATABASE_SETUP_WINDOW_TITLE)
    # create_user_window.iconbitmap(WINDOW_ICON_BITMAP_PATH)

    container = tk.Canvas(master=create_user_window, bg=DEFAULT_BACKGROUND_COLOR)

    database_name = tk.StringVar()
    user_full_name = tk.StringVar()
    user_name = tk.StringVar()
    user_password = tk.StringVar()
    security_question = tk.StringVar()
    security_answer = tk.StringVar()
    admin_status = tk.BooleanVar()
    __show = tk.BooleanVar()

    # # label and input box
    main_heading_label = tk.Label(container, text='SET UP DATABASE', bg=DEFAULT_BACKGROUND_COLOR, font=HEADER_FONT_2)
    main_heading_label.place(relx=.2525, relwidth=.55, rely=.03, relheight=.085)

    database_name_label = tk.Label(
                                    container, anchor="e", text='Database name', font=('Comic Scan Ms', 10, 'bold'),
                                    bg=DEFAULT_BACKGROUND_COLOR
                            )
    database_name_label.place(relx=.1, relwidth=.22, rely=.2, relheight=.05)
    database_name_entry = tk.Entry(container, textvariable=database_name, font=DEFAULT_FONT)
    database_name_entry.place(relx=.35, relwidth=.45, rely=.2, relheight=.05)
    database_name_entry.focus_set()

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
                                        command=lambda: create_user(create_user_window, database_name=database_name.get(), user_name=user_name.get(),
                                        user_full_name=user_full_name.get(), user_password=user_password.get(),admin_status=admin_status.get(),
                                        security_question=security_question.get(), security_answer=security_answer.get()
                                    )
                                )
    create_user_button.place(relx=.35, relwidth=.15, rely=.8, relheight=.07)         

    container.place(relheight=1, relwidth=1)
    center_window(create_user_window, height=400, width=480)
    create_user_window.wm_deiconify()
    index_view_window.mainloop()

database_setup()