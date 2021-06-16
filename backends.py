from tkinter import messagebox as _msgbox
from validator import Validator
from db import PostgresConnect
import tkinter as tk
from hashlib import md5
from utils import (
                    log_errors,
                    _clear_search,
                    get_current_date
                )
from constants import (
                        DEPARTMENT_CHOICE_LIST,
                        ABBRV_DEPARTMENT_MATRIC,
                        WIN32
                    )


class BaseManager:
    def __init__(self, root_window):
        self.root_window = root_window
        self.db_manager = PostgresConnect(root_window=self.root_window)
        self.validator = Validator()
        self.is_admin = tk.BooleanVar(value=False)
        self.searching_transactions = tk.BooleanVar(value=False)
        self.searching_students = tk.BooleanVar(value=False)
        self.managed_login_widgets = None
        self.end = None
        self.transactions_information = []
        self.students_information = []
        self.users_information = []
        self.books_information = []
        self.found_transactions = []
        self.students_information_viewer = None
        self.books_information_viewer = None
        self.users_information_viewer = None
        self.transactions_information_viewer = None

    def login_user(self, prev_window, username, password, next_window):
        if not (username and password):
            _msgbox.showwarning(title="Missing details", message="Username and password fields required to proceed", parent=prev_window)
            return

        __username = username
        credentials = self.db_manager.get_user_credentials(__username)
        if not credentials:
            _msgbox.showerror(title="Login failed",message="User '%s' does not exist"%username, parent=prev_window)
            return
        __user_password = credentials[1]
        __password = md5(str.encode(password)).hexdigest()
        passwords_match = __password == __user_password
        if not passwords_match:
            _msgbox.showerror(title="Login failed",message="Invalid log in credentials for user %s"%username, parent=prev_window)
            return
        self.is_admin.set(self.db_manager.get_admin_status(user_name=__username))
        next_window()

    def set_login_entries(self, managed_login_widgets, end):
        self.managed_login_widgets = managed_login_widgets
        self.end = end

    def update_password(self, forgot_password_window, user_name, security_question, security_answer, new_password):
        entries_not_null = all((user_name, security_question, security_answer, new_password))
        if not entries_not_null:
            _msgbox.showwarning(title="Missing credentials", message="All fields are required for password update\n\
Kindly ensure that all fields are field with the appropriate values")
            return
        user_credentials = self.db_manager.get_user_credentials(user_name.lower())
        if not user_credentials:
            _msgbox.showerror(title="Invalid user credentials", message="No user account registered with %s"%user_name, parent=forgot_password_window)
            return
        user_name, __old_password = user_credentials
            
        password_valid, error_or_password = self.validator.validate_password(username=user_name, password=new_password)
        if not password_valid:
            _msgbox.showerror(title="Password error", message=error_or_password)
            return
        security_credentials = self.db_manager.get_user_security_credentials(user_name.lower())
        # if not security_answer:
        #     _msgbox.showerror(title="Missing security answer",message="Security answer field required to proceed")
        #     return
        security_answer = md5(str.encode(security_answer.capitalize())).hexdigest()
        
        if (security_question, security_answer == security_credentials):
            __new_password = md5(str.encode(error_or_password)).hexdigest()
            if __new_password == __old_password:
                _msgbox.showinfo(title="Password not updated", message="Password to be updated does not differ from the current password for %s"%user_name, parent=forgot_password_window)
                return            
            password_updated = self.db_manager.update_password(user_name, __new_password)
            if password_updated:
                _msgbox.showinfo(title="Password updated", message="Successfully updated password for %s"%user_name, parent=forgot_password_window)
            return

        _msgbox.showerror(title="Failed to update password", message="Invalid security details entered for %s"%user_name, parent=forgot_password_window)

    def register_student(self, current_window, **kwargs):
        __matric_number = kwargs["student_matric_number"].upper().strip()
        __student_name = kwargs["student_name"].title().strip()
        __department = kwargs["department"]
        __date_registered = kwargs["date_registered"]
        __registrar = kwargs["registrar"].capitalize()
        credentials = (__matric_number, __student_name, __department, __date_registered)

        credentials_invalid = [True for credential in credentials if not credential]
        if credentials_invalid:
            _msgbox.showwarning(title="Missing credentials", message="All fields are required to proceed", parent=current_window)
            return   

        student_name_valid, invalid_name_message = self.validator.validate_fullname(__student_name)      
        if not student_name_valid:
            _msgbox.showerror(title="Invalid student name", message=invalid_name_message)
            return

        if not self.validator.validate_matric_number(__matric_number):
            invalid_matric_number_message = "{} is not a valid ogitech matric number".format(__matric_number)
            _msgbox.showerror(title="Invalid matric number", message=invalid_matric_number_message)
            return

        student_exists = self.db_manager.get_student(__matric_number)
        if student_exists:
            existing_student_name = student_exists[1]
            _msgbox.showerror(title="Student exists", message="Student named {} has been registered with matric number {}".format(
                                                                                                                        existing_student_name,
                                                                                                                        __matric_number
                                                                                                                    )
                                                                                                                )
            return

        if ABBRV_DEPARTMENT_MATRIC[DEPARTMENT_CHOICE_LIST.index(__department)] != __matric_number[:4]:
            _msgbox.showerror(title="Invalid matric number", message="Student from %s cannot be assigned \
matric number value of %s"%(
                            __department, __matric_number
                        )
                    )
            return

        credentials = (__matric_number, __student_name, __department, __date_registered, __registrar)
        student_registered = self.db_manager.register_student(credentials, current_window)
        if student_registered is None:
            return
        message = "Successfully registered %s"%__student_name if student_registered else "Failed to register %s\nIt could be as a result Matric Number exists"%__student_name
        title = "Success" if student_registered else "Failed"
        _msgbox.showinfo(title=title, message=message, parent=current_window)

    def add_book(self, current_window, **kwargs):
        __book_id = kwargs["book_id"]
        __book_title = kwargs["book_name"].title().strip()
        __author_name = kwargs["book_author"].title().strip()
        __number_of_copies = kwargs["number_of_copies"]
        credentials = (__book_id, __book_title, __author_name, __number_of_copies, __number_of_copies)

        missing_credentials = [True for credential in credentials if not credential]
        if missing_credentials:
            _msgbox.showwarning(title="Missing credentials", message="All fields are required to proceed", parent=current_window)
            return            

        if not __book_id.isdecimal():
            _msgbox.showinfo(title="Book ID error", message="Book ID must be a positive decimal number not %s"%__book_id, parent=current_window)
            return

        if len(__author_name) < 5:
            _msgbox.showinfo(title="Name error", message="Please enter a valid author name,\nThis must be a minimum of 5 characters", parent=current_window)
            return            

        if not __number_of_copies.isdecimal():
            _msgbox.showinfo(title="Stock error", message="Number of books to be added to the store must be a decimal number not %s"%__number_of_copies, parent=current_window)
        
        if not int(__number_of_copies) in list(range(1, 101)):
            _msgbox.showinfo(title="Maximum copies exceeded", message="A minimum of 1 and a maximum of 100 books\nallowed to be added to the library at once", parent=current_window)
            return
        __number_of_copies = int(__number_of_copies)

        existing_book = self.db_manager.get_book(__book_id)
        book_exists = existing_book[1:3] == credentials[1:3]
        if existing_book and (not book_exists):
            _msgbox.showerror(title="Book already exists", parent=current_window, 
                                                        message="Book titled %s by %s already exist with the ID %s"%(
                                                                                                                __book_title,
                                                                                                                __author_name,
                                                                                                                 __book_id
                                                                                                            )
                                                                                                        )
            return
        copy_or_copies = "copy" if __number_of_copies == 1 else "copies"

        if book_exists:
            __previous_total_stock = int(existing_book[-1])
            __previous_available_stock = int(existing_book[-2])
            __existing_book_author = existing_book[2]
            __update_book = _msgbox.askokcancel(
                            title="Update book stock?", parent=current_window,
                            message="%s by %s already in the library\navailable stock = %s\n%s more %s will be added to the library?"%(
                                                                                                                __book_title,
                                                                                                                __existing_book_author,
                                                                                                                __previous_available_stock,
                                                                                                                __number_of_copies,
                                                                                                                copy_or_copies   
                                                                                                            )
                                                                                                        )
            if not __update_book:
                return            
            current_total_stock = __previous_total_stock + __number_of_copies
            total_available_stock = __previous_available_stock + __number_of_copies
            new_book_details = (total_available_stock, current_total_stock, __book_id)
            self.db_manager.update_book_stock(new_book_details)
            _msgbox.showinfo(title="Book(s) updated", parent=current_window, message="Successfully added %s more %s of book titled %s with ID %s to the library"%(
                                                                                                                                                __number_of_copies,
                                                                                                                                                copy_or_copies,
                                                                                                                                                __book_title,
                                                                                                                                                __book_id  
                                                                                                                                                )
                                                                                                                                            )            
            return

        if not _msgbox.askyesno(title="Add book?", parent=current_window, message="Do you want to add %s %s of %s by %s to the library?"%(
                                                                                                                    __number_of_copies,
                                                                                                                    copy_or_copies,
                                                                                                                    __book_title,
                                                                                                                    __author_name
                                                                                                                )
                                                                                                            ):
            return
            
        __book = self.db_manager.add_book(credentials, current_window)
        _msgbox.showinfo(title="Book added", parent=current_window, message="Successfully added %s %s of book titled %s by %s with ID %s to the library"%(
                                                                                                                                      __number_of_copies,
                                                                                                                                      copy_or_copies,
                                                                                                                                      __book_title,
                                                                                                                                      __author_name,
                                                                                                                                      __book_id  
                                                                                                                                    )
                                                                                                                                )

    def create_user(self, user_window, **kwargs):
        __user_id = kwargs["user_id"]
        __user_full_name = kwargs["user_full_name"]
        __user_name = kwargs["user_name"].lower()
        __user_password = kwargs["user_password"]
        __security_question = kwargs["security_question"]
        __security_answer = kwargs["security_answer"].capitalize().strip()
        __admin_status = kwargs["admin_status"]

        credentials = (__user_id, __user_name, __user_full_name, __user_password, __security_question, __security_answer)

        credentials_invalid = [True for credential in credentials if not credential]
        if credentials_invalid:
            _msgbox.showwarning(title="Missing credentials", message="All fields are required to proceed", parent=user_window)
            return 

        if not __user_id.isdecimal():
            _msgbox.showinfo(title="User ID error", message="User ID must be a positive decimal number not %s"%__user_id, parent=user_window)
            return

        __user = self.db_manager.get_user(__user_id)
        if __user:
            __existing_username = __user[1]
            _msgbox.showinfo(title="User already exist", message="Existing user account %s found with ID %s\nKindly select another ID and try again"%(__existing_username, __user_id), parent=user_window)
            return

        __user_by_username = self.db_manager.get_user_by_username(__user_id)
        if __user_by_username:
            __existing_user_by_username = __user_by_username[1]
            _msgbox.showinfo(title="User already exist", message="Existing user account %s found with username %s\nKindly select another username and try again"%(__existing_user_by_username, __user_id), parent=user_window)
            return                  

        user_name_valid, error_or_username = self.validator.validate_username(__user_name)
        if not user_name_valid:
            _msgbox.showerror(title="Username error", message=error_or_username)
            return
        __user_name = error_or_username

        user_full_name_valid, error_or_full_name = self.validator.validate_fullname(__user_full_name)
        if not user_full_name_valid:
            _msgbox.showerror(title="Name error", message=error_or_full_name)
            return
        __user_full_name = error_or_full_name

        password_valid, error_or_password = self.validator.validate_password(username=__user_name, password=__user_password)
        if not password_valid:
            _msgbox.showerror(title="Password error", message=error_or_password)
            return


        __user_password = md5(str.encode(error_or_password)).hexdigest()
        __security_answer = md5(str.encode(__security_answer)).hexdigest()

        credentials = (__user_id, __user_full_name, __user_name, __user_password,
                        __security_question, __security_answer, __admin_status, get_current_date())

        create_user_message = "Are you sure you want to create user {} with user id {} for library management?".format(__user_name, __user_id)
        finally_validated = _msgbox.askyesno(title="Create user?", message=create_user_message, parent=user_window)
        if not finally_validated:
            return                             

        user_created = self.db_manager.create_user(credentials)
        _msgbox.showinfo(title="User created", message= "Successfully created %s"%__user_name, parent=user_window)

    def unregister_student(self, student_window, student_matric_number):
        __matric_number = student_matric_number.upper()

        if not self.validator.validate_matric_number(__matric_number):
            invalid_matric_number_message = "{} is not a valid ogitech matric number".format(__matric_number)
            _msgbox.showerror(title="Invalid matric number", message=invalid_matric_number_message, parent=student_window)
            return

        __student = self.db_manager.get_student(__matric_number)
        if not __student:
            _msgbox.showerror(title="Student does not exist", message="No student registered with matric number %s"%__matric_number, parent=student_window)
            return
        __student_name = __student[1]
        __student_department = __student[2]

        __pending_returns = self.db_manager.get_borrowed_books(matric_number=__matric_number)
        if __pending_returns:
            _msgbox.showerror(title="Book not returned", parent=student_window, message="%s has not returned some books he was issued\nRetrieve all issued books before unregistering student"%__student_name)
            return

        unregister_student_message = "Are you sure you want to unregister {} from department {} with matric number {}?".format(__student_name, __student_department, __matric_number)
        finally_validated = _msgbox.askyesno(title="Unregister student?", message=unregister_student_message, parent=student_window)
        if not finally_validated:
            return 
        
        self.db_manager.unregister_student(__matric_number)
        _msgbox.showinfo(title="Student unregistered", message="Successfully unregistered student %s with matric number %s"%(__student_name, __matric_number), parent=student_window)

    def remove_book(self, book_window, __book_id):
        if not __book_id:
            _msgbox.showinfo(title="Book ID error", message="Book ID field required to proceed", parent=book_window)
            return

        if not __book_id.isdecimal():
            _msgbox.showinfo(title="Book ID error", message="Book ID must be a oositive decimal number", parent=book_window)
            return

        __book = self.db_manager.get_book(__book_id)
        if not __book:
            failure_message = "No book with the ID {} exists".format(__book_id)
            _msgbox.showerror(title="Failed", message=failure_message, parent=book_window)
            return
        __book_title = __book[1]
        __book_author = __book[2]

        __book_issued = self.db_manager.get_borrowed_books(book_id=__book_id)
        if __book_issued:
            failure_message = "Some copies of {} are yet to be returned\nRetrieve all copies before removal of book".format(__book_title)
            _msgbox.showerror(title="Pending retrieval", message=failure_message, parent=book_window)
            return            

        remove_book_message = "Are you sure you want to remove book {} by {} with book id {} from the library?".format(__book_title, __book_author, __book_id)
        finally_validated = _msgbox.askyesno(title="Remove book?", message=remove_book_message, parent=book_window)
        if not finally_validated:
            return    

        self.db_manager.remove_book(__book_id)
        _msgbox.showinfo(title="Book removed", message="Successfully removed all copies of book titled %s from the library"%__book_title, parent=book_window)

    def delete_user(self, user_window, __user_id):
        if not __user_id:
            _msgbox.showinfo(title="User ID error", message="User ID field required to proceed", parent=user_window)
            return

        if not __user_id.isdecimal():
            _msgbox.showinfo(title="User ID error", message="User ID must be a positive decimal number not %s"%__user_id, parent=user_window)
            return

        __user = self.db_manager.get_user(__user_id)
        if not __user:
            _msgbox.showinfo(title="User does not exist", message="No existing user account found with ID %s"%__user_id, parent=user_window)
            return            

        delete_user_message = "Are you sure you want to delete user {} ({}) with user id {} from the library?".format(__user[1], __user[2], __user[0])
        finally_validated = _msgbox.askyesno(title="Delete user?", message=delete_user_message, parent=user_window)
        if not finally_validated:
            return            

        self.db_manager.delete_user(__user_id)
        _msgbox.showinfo(title="User deleted", message="Successfully deleted user %s from user group"%__user[2], parent=user_window)

    def issue_book(self, current_window, book_id, student_matric_number, current_date):
        if not (book_id and student_matric_number):
            _msgbox.showinfo(title="Missing details", message="Book ID and Matric number required to proceed", parent=current_window)
            return

        if not book_id.isdecimal():
            _msgbox.showinfo(title="Book ID error", message="Book ID must be a positive decimal number not %s"%book_id, parent=current_window)
            return

        student_matric_number = student_matric_number.upper()
        if not self.validator.validate_matric_number(student_matric_number):
            invalid_matric_number_message = "{} is not a valid ogitech matric number".format(student_matric_number)
            _msgbox.showerror(title="Invalid matric number", message=invalid_matric_number_message)
            return

        book = self.db_manager.get_book(book_id)
        if not book:
            _msgbox.showinfo(title="Book not found", message="No book found with the ID %s"%book_id, parent=current_window)
            return
        book_name = book[1]       

        student = self.db_manager.get_student(student_matric_number)
        if not student:
            _msgbox.showinfo(title="Student does not exist", message="No student found with the matric number %s"%student_matric_number, parent=current_window)
            return
        student_name = student[1]

        previously_issued = self.db_manager.get_transaction(book_id, student_matric_number)
        if previously_issued:
            _msgbox.showinfo(title="Aready Issued", message="%s has already been issued a copy of %s"%(student_name, book_name), parent=current_window)
            return 

        available_stock = int(book[-2])
        if available_stock < 1:
            _msgbox.showinfo(title="Unavailable", message="All books named %s have been issued out"%book_name, parent=current_window)
            return

        maximum_books_collected = self.db_manager.get_all_borrowed_books(student_matric_number) == 3
        if maximum_books_collected:
            _msgbox.showinfo(title="Limit reached", message="%s has been issued three books, at least one book must be returned before you can be issued %s"%(student_name, book_name), parent=current_window)
            return

        issue_book = _msgbox.askyesno(title="Issue book?", message="Do you want to issue book %s to %s?"%(book_name, student_name), parent=current_window)
        if not issue_book:
            return

        self.db_manager.issue_book(book_id, student_matric_number, available_stock, current_date, current_window, book_name, student_name)
        _msgbox.showinfo(title="Book issued", message="Book titled %s successfully issued to %s"%(book_name, student_name), parent=current_window)   

    def retrieve_book(self, current_window, book_id, student_matric_number):
        if not (book_id and student_matric_number):
            _msgbox.showinfo(title="Missing details", message="Book ID and Matric number required to proceed", parent=current_window)
            return

        if not book_id.isdecimal():
            _msgbox.showinfo(title="Book ID error", message="Book ID must be a decimal number not %s"%book_id, parent=current_window)
            return           

        book = self.db_manager.get_book(book_id)
        if not book:
            _msgbox.showinfo(title="Book not found", message="No book found with the ID %s"%book_id, parent=current_window)
            return    

        student_matric_number = student_matric_number.upper()
        if not self.validator.validate_matric_number(student_matric_number):
            invalid_matric_number_message = "{} is not a valid ogitech matric number".format(student_matric_number)
            _msgbox.showerror(title="Invalid matric number", message=invalid_matric_number_message)
            return

        student = self.db_manager.get_student(student_matric_number)
        if not student:
            _msgbox.showinfo(title="Student does not exist", message="No student found with the matric number %s"%student_matric_number, parent=current_window)
            return

        book_name = book[1]
        student_name = student[1]
        available_stock = int(book[-2])
        current_stock = int(book[-1])

        if current_stock == available_stock:
            _msgbox.showinfo(title="No books issued", message="No copy of %s has been issued out"%book_name, parent=current_window)
            return

        book_was_issued = self.db_manager.get_transaction(book_id, student_matric_number)
        if not book_was_issued:
            _msgbox.showinfo(title="Transaction does not exist", message="Retrieval of Book titled %s from %s is not possible as the transaction never occurred"%(book_name, student_name), parent=current_window)
            return

        retrieve_book = _msgbox.askyesno(title="Retrieve book?", message="Do you want to retrieve book %s from %s?"%(
                                                                                                    book_name, student_name),
                                                                                                    parent=current_window
                                                                                                    )
        if not retrieve_book:
            return 

        self.db_manager.retrieve_book(book_id, student_matric_number, available_stock, current_window, book_name, student_name)
        _msgbox.showinfo(title="Book retrieved", message="Book titled %s successfully retrieved from %s"%(book_name, student_name), parent=current_window)

    def get_transaction_informations(self):
        information = self.db_manager.get_information()
        if not information:
            return
        return information

    def set_students_information_viewer(self, treeview_widget):
        self.students_information_viewer = treeview_widget
        
    def set_books_information_viewer(self, treeview_widget):
        self.books_information_viewer= treeview_widget 

    def set_users_information_viewer(self, treeview_widget):
        self.users_information_viewer = treeview_widget 

    def set_transactions_information_viewer(self, treeview_widget):
        self.transactions_information_viewer = treeview_widget 

    def populate_students_information_treeview(self, current_window):
        if not self.searching_students.get():
            self.students_information = self.db_manager.get_students()
        if not self.students_information:
            _msgbox.showinfo(title="No students", message="No student registered as at now\nStudents will be displayed once any is registered", parent=current_window)
            return
        try:
            for i, found_details in enumerate(self.students_information):
                self.students_information_viewer.insert("", i, i, values=found_details)
        except tk.TclError as e:
            pass

    def depopulate_students_information_treeview(self):
        if not self.students_information:
            return        
        try:
            for i in range(len(self.students_information)):
                self.students_information_viewer.delete(i)
            self.students_information.clear()
        except tk.TclError:
            pass

    def search_students(self, current_window, matric_number=None, student_name=None):
        student_name, matric_number = student_name.get(), matric_number.get()
        if not(student_name or matric_number):
            _msgbox.showerror(title="Empty entries", message="Valid student's name or student's matric number required to proceed")
            return

        if student_name:
            valid_student_name, student_name_or_error = self.validator.validate_name_or_full_name(student_name)
            if not valid_student_name:
                _msgbox.showerror(title="Invalid student name", message=student_name_or_error, parent=current_window)
                return
            student_name = student_name_or_error

        if matric_number:
            matric_number = matric_number.upper()
            valid_matric_number = self.validator.validate_matric_number(matric_number)
            if not valid_matric_number:
                invalid_matric_number_message = "{} is not a valid ogitech matric number".format(matric_number)
                _msgbox.showerror(title="Invalid matric number", message=invalid_matric_number_message, parent=current_window)
                return

        students_information = self.db_manager.search_students(student_name, matric_number)
        if students_information:
            self.depopulate_students_information_treeview()
            self.students_information = students_information
            self.searching_students.set(True)
            self.populate_students_information_treeview(current_window)
            return
        _msgbox.showerror(title="No match found", message="No student named %s found\nKindly ensure you typed in a correct name"%student_name)
        self.clear_searched_students(current_window, (), ())

    def clear_searched_students(self, current_window, entry_widgets, text_variables):
        if entry_widgets and text_variables:
            _clear_search(entry_widgets, text_variables)
        self.depopulate_students_information_treeview()
        self.searching_students.set(False)
        self.populate_students_information_treeview(current_window)

    def students_treeview_select(self, event):
        new = int(self.students_information_viewer.selection()[0])
        student = self.students_information_viewer.item(self.students_information_viewer.focus())
        print(student)

    def populate_books_information_treeview(self, current_window, books_information=[]):
        if books_information:
            self.books_information = books_information
        else:
            self.books_information = self.db_manager.get_books()
        if not self.books_information:
            _msgbox.showinfo(title="No books", message="No book added as at now\nBooks will be displayed once any is added", parent=current_window)
            return
        try:
            for i, found_details in enumerate(self.books_information):
                self.books_information_viewer.insert("", i, i, values=found_details)
        except tk.TclError as e:
            print(e)
            pass


    def depopulate_books_information_treeview(self):
        if not self.books_information:
            return        
        try:
            for i in range(len(self.books_information)):
                self.books_information_viewer.delete(i)
            self.books_information.clear()
        except tk.TclError:
            pass

    def books_treeview_select(self, event):
        new = int(self.books_information_viewer.selection()[0])
        book = self.books_information_viewer.item(self.books_information_viewer.focus())
        print(book)

    def populate_users_information_treeview(self, current_window):
        self.users_information = self.db_manager.get_users()
        if not self.users_information:
            _msgbox.showinfo(title="No users", message="No users exist as at now\nusers will be displayed once any is created", parent=current_window)
            return
        try:
            for i, found_details in enumerate(self.users_information):
                found_details = found_details[:3] + found_details[-3:]
                self.users_information_viewer.insert("", i, i, values=found_details)
        except tk.TclError as e:
            print(e)
            pass

    def depopulate_users_information_treeview(self):
        if not self.users_information:
            return        
        try:
            for i in range(len(self.users_information)):
                self.users_information_viewer.delete(i)
            self.users_information.clear()
        except tk.TclError:
            pass

    def search_users(self, current_window, user_id=None, user_name=None):
        user_id, user_name = user_id.get(), user_name.get()
        if not(user_id or user_name):
            _msgbox.showerror(title="Empty entries", message="Valid users's ID or user's name required to proceed")
            return

        if user_name:
            valid_user_name, user_name_or_error = self.validator.validate_name_or_full_name(user_name)
            if not valid_user_name:
                _msgbox.showerror(title="Invalid username", message=user_name_or_error, parent=current_window)
                return
            user_name = user_name_or_error

        if user_id:
            if not user_id.isdecimal():
                _msgbox.showinfo(title="User ID error", message="User ID must be a positive decimal number not %s"%user_id, parent=user_window)
                return

        self.depopulate_users_information_treeview()
        self.users_information = self.db_manager.search_users(student_name, matric_number)
        if self.students_information:
            self.searching_students.set(True)
            self.populate_students_information_treeview(current_window)
            return
        _msgbox.showerror(title="No match found", message="No student named %s found\nKindly ensure you typed in a correct name"%student_name)
        self.populate_students_information_treeview(current_window)

    def clear_searched_students(self, current_window, entry_widgets, text_variables):
        _clear_search(entry_widgets, text_variables)
        self.depopulate_students_information_treeview()
        self.searching_students.set(False)
        self.populate_students_information_treeview(current_window)

    def users_treeview_select(self, event):
        new = int(self.users_information_viewer.selection()[0])
        user = self.users_information_viewer.item(self.users_information_viewer.focus())
        print(user)

    def populate_transactions_information_treeview(self, current_window):
        if self.found_transactions:
            self.transactions_information = self.found_transactions
            self.searching_transactions.set(True)
        else:
            self.transactions_information = self.get_transaction_informations()
        if not self.transactions_information:
            return
        try:
            for i, found_details in enumerate(self.transactions_information):
                self.transactions_information_viewer.insert("", i, i, values=found_details)
        except tk.TclError as e:
            pass

    def depopulate_transactions_information_treeview(self):
        if not self.transactions_information:
            return  
        try:
            for i in range(len(self.transactions_information)):
                self.transactions_information_viewer.delete(i)
            self.transactions_information.clear()
        except tk.TclError:
            pass

    def search_transactions(self, current_window, book_id=None, matric_number=None):
        if not(book_id or matric_number):
            _msgbox.showerror(title="Empty entries", message="Valid book id or student's matric number required to proceed")
            return

        if matric_number:
            matric_number = matric_number.upper()
            valid_matric_number = self.validator.validate_matric_number(matric_number)
            if not valid_matric_number:
                invalid_matric_number_message = "{} is not a valid ogitech matric number".format(matric_number)
                _msgbox.showerror(title="Invalid matric number", message=invalid_matric_number_message, parent=current_window)
                return

        if book_id:
            book_id = book_id.strip()
            if not book_id.isdecimal():
                _msgbox.showinfo(title="Book ID error", message="Book ID must be a positive decimal number not %s"%book_id, parent=current_window)
                return
        self.found_transactions = self.db_manager.search_transactions(book_id, matric_number)
        if self.found_transactions:
            return
        _msgbox.showerror(title="No match found", message="No transactions with the specified search parameters")

    def clear_searched_transactions(self, entry_widgets, text_variables):
        _clear_search(entry_widgets, text_variables)
        self.found_transactions.clear()
        self.searching_transactions.set(False)

    def transactions_treeview_select(self, event):
        new = int(self.transactions_information_viewer.selection()[0])
        transaction = self.transactions_information_viewer.item(self.transactions_information_viewer.focus())
        print(transaction)

    def clean_login_entries(self):
        for login_widget in self.managed_login_widgets:
            login_widget.delete(0, self.end)

    def _next_modal(self, prev_window, next_window):
        if WIN32:
            prev_window.attributes("-disabled", True)
        next_window.transient(prev_window)

    def _release_modal(self, prev_window, next_window):
        _exit = self.clean_exit(window=prev_window)
        if _exit:
            if WIN32:
                next_window.attributes("-disabled", False)
            next_window.lift()

    def clean_exit(self, window=None, master=None, current_window=None, index_window=None):
        notification = F"Do you want to exit this window?"
        if current_window:
            notification = "Do you want to exit the application?"
            if current_window == "home":
                notification = "You will be logged out if you proceed\nDo you want to continue?"
        if not _msgbox.askyesno(title="Exit?", message=notification, parent=window):
            return False
        window.wm_withdraw()
        if index_window:
            index_window.wm_deiconify()
        if master:
            self.clean_login_entries()
            master.wm_deiconify()
        return True
