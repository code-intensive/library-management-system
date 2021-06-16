import psycopg2
from utils import to_string, get_current_date
from tkinter.messagebox import showerror, showinfo
from tkinter.messagebox import askyesno
from constants import DATABASE_CREDENTIALS, DATABASE_NAME
from utils import log_errors


class PostgresConnect:
    '''
    Class for all database related operations
    All SQL operations carried out from the backend are handled by its methods
    The model database is `Postgresql`
    '''
    def __init__(self, dbname:str=None, user:str=None, password:str=None, host:str=None, post:str=None, table_name: str=None, root_window=None):
        try:
            connection = psycopg2.connect(
                "dbname='{}' user='{}' password='{}' host='{}' port='{}'".format(*DATABASE_CREDENTIALS)
            )
            connection.autocommit = True
            self.cursor = connection.cursor()
            self.table_name = table_name
        except Exception as error_message:
            error_path = log_errors(error_message)
            showerror(title="Fatal error", message="There was an error connecting to the database (%s) using the given credentials\n\
Please validate the details and try reloading the application\n\
Check log at %s\nfor detailed information about the cause"%(DATABASE_NAME, error_path), parent=root_window)
            exit(0)

    

    def create_student_table(self):
        '''
        Create database table for students
        '''
        create_student_table_command = '''
                                        CREATE TABLE public.students (
                                            matric_number varchar NOT NULL,
                                            student_name varchar NOT NULL,
                                            department varchar NOT NULL,
                                            date_registered date NOT NULL,
                                            registrar varchar NOT NULL
                                        );
                                    '''
        try:
            self.cursor.execute(create_student_table_command)
        except Exception as handled_exception:
            error_path = log_errors(handled_exception)
            showerror(title="Failed to create table", message="Failed to create student table for database %s\n\
Kindly confirm all credentials are valid\n\
Check log at %s for detailed information about the cause"%(DATABASE_NAME, error_path))
        else:
            showinfo(title="Student table created", message="Successfully created student table for database %s"%DATABASE_NAME)

    def create_book_table(self):
        '''
        Create database table for books
        '''
        create_book_table_command = '''
                                        CREATE TABLE public.books (
                                            book_id int4 NOT NULL,
                                            book_name varchar NOT NULL,
                                            book_author varchar NOT NULL,
                                            available_stock int4 NOT NULL DEFAULT 1,
                                            current_stock int4 NOT NULL DEFAULT 1
                                        );
                                    '''
        try:
            self.cursor.execute(create_book_table_command)
        except Exception as handled_exception:
            error_path = log_errors(handled_exception)
            showerror(title="Failed to create table", message="Failed to create book table for database %s\nKindly confirm all credentials are valid\n\
Check log at %s for detailed information about the cause"%(DATABASE_NAME, error_path))
        else:
            showinfo(title="Book table created", message="Successfully created book table for database %s"%DATABASE_NAME)

    def create_user_table(self):
        '''
        Create database table for users
        '''
        create_user_table_command = '''
                                            CREATE TABLE public.users (
                                            user_id int NOT NULL,
                                            user_name varchar NOT NULL,
                                            user_full_name varchar  NOT NULL,
                                            user_password varchar NOT NULL,
                                            security_question varchar NOT NULL,
                                            security_answer varchar NOT NULL,
                                            admin_status bool NOT NULL,
                                            date_created date NOT NULL,
                                            creator varchar NOT NULL
                                        );
                                    '''
        default_user_credentials = (1, "Default Admin", "admin", "ea8a21d05bedaf5e00b0d94943aea477",
                            "What is your special combination?", "46b6726a8a327e007d41d9f603bae95d", "true", get_current_date())  
        try:
            self.cursor.execute(create_user_table_command)
            # Create a default admin user with username: admin and password: `nimda12345`
            # Security question: `What is your special combination?`, security answer: `nimda`
            self.create_user(default_user_credentials)
        except Exception as handled_exception:
            error_path = log_errors(handled_exception)
            showerror(title="Failed to create table", message="Failed to create user table for database %s\n\
Kindly confirm all credentials are valid\n\
Check log at %s for detailed information about the cause"%(DATABASE_NAME, error_path))
        else:
            showinfo(title="User table created", message="Successfully created user table for database %s"%DATABASE_NAME)
  
    def create_transaction_table(self):
        '''
        Create database table for transactions
        '''
        create_transaction_table_command = '''
                                        CREATE TABLE public.transcations (
                                            matric_number varchar NOT NULL,
                                            book_id int4 NOT NULL,
                                            transaction_date date NOT NULL
                                        );
                                    '''
        try:
            self.cursor.execute(create_transaction_table_command)
        except Exception as handled_exception:
            error_path = log_errors(handled_exception)
            showerror(title="Failed to create table", message="Failed to create transaction table for database %s\nKindly confirm all credentials are valid\n\
Check log at %s for detailed information about the cause"%(DATABASE_NAME, error_path))
        else:
            showinfo(title="Transaction table created", message="Successfully created transaction table for database %s"%DATABASE_NAME)

    def set_up_database(self):
        '''
        Automatically generates database tables for the library using the default tables
        `students`, `books`, `users` and `transactions`
        '''
        try:
            self.create_student_table()
            self.create_book_table()
            self.create_user_table()
            self.create_transaction_table()
        except Exception as handled_exception:
            error_path = log_errors(handled_exception)
            showerror(title="Failed", message="Failed to create database tables for %s\n\
For detailed info about the error view the log file at %s"%(DATABASE_NAME, error_path))
        else:
            success_message = '''
    Successfully created the following tables in the %s database:
    1. students
    2. books
    3. users
    4. transactions
                            '''.format(
                                        DATABASE_NAME
                                    ) 
            showinfo(title="Success", message=success_message)

    def register_student(self, student_credentials: list, current_window):
        '''
        Register new students into the database
        '''
        sql_values = to_string(student_credentials)
        register_student_command = 'INSERT INTO public.students(matric_number, student_name,\
        department, date_registered, registrar) VALUES ({});'.format(sql_values)
        register_student_message = "Are you sure you want to register {} with matric number {}?".format(
                                                                                                        student_credentials[1], 
                                                                                                        student_credentials[0]
                                                                                                        )
        finally_validated = askyesno(title="Register student?", message=register_student_message, parent=current_window)
        if not finally_validated:
            return        
        try:
            self.cursor.execute(register_student_command)
        except Exception as handled_exception:
            error_path = log_errors(handled_exception)
            return False
        else:
            return True

    def add_book(self, book_details: list=[], current_window=None):
        '''
        Add new book with the given book details
        '''
        sql_values = to_string(book_details)
        add_book_command = 'INSERT INTO public.books(book_id, book_name, book_author, available_stock, current_stock) VALUES ({});'.format(
                                                                                                                                sql_values
                                                                                                                                )
        self.cursor.execute(add_book_command)

    def create_user(self, user_credentials: list):
        '''
        Creates new user with the given credentials
        '''
        sql_values = to_string(user_credentials)
        create_user_command = 'INSERT INTO public.users(user_id, user_full_name, user_name, user_password,\
            security_question, security_answer, admin_status, date_created) VALUES ({});'.format(sql_values)    
        self.cursor.execute(create_user_command)

    def unregister_student(self, matric_no: str):
        '''
        Unregister student with a given matric number by deleting student from the database
        '''
        unregister_student_command = "DELETE FROM public.students WHERE matric_number='{}';".format(matric_no)
        self.cursor.execute(unregister_student_command)

    def remove_book(self, book_id: str):
        '''
        Remove a book with a specified id from the database
        '''
        remove_book_command = "DELETE FROM public.books WHERE book_id='{}';".format(book_id)  
        self.cursor.execute(remove_book_command)

    def delete_user(self, user_id):
        '''
        Delete a user by a given id from the database
        '''
        remove_user_command = "DELETE FROM public.users WHERE user_id='{}';".format(user_id)
        self.cursor.execute(remove_user_command)   

    def get_students(self):
        '''
        Returns an array of all existing students from the database
        '''
        try:
            self.cursor.execute('SELECT * FROM public.students')
        except Exception:
            return
        else:
            students = self.cursor.fetchall()
            return students

    def get_books(self):
        '''
        Returns an array of all existing books from the database
        '''
        try:
            self.cursor.execute('SELECT * FROM public.books')
        except Exception:
            return
        else:
            books = self.cursor.fetchall()
            return books

    def get_users(self):
        '''
        Return an array of all existing users from the database
        '''
        try:
            self.cursor.execute('SELECT * FROM public.users')
        except Exception:
            return
        else:
            users = self.cursor.fetchall()
            return users

    def get_transactions(self):
        '''
        Returns an array of all existing transactions made
        '''
        try:
            self.cursor.execute('SELECT * FROM public.transactions')
        except Exception:
            return
        else:
            transactions = self.cursor.fetchall()
            if transactions:
                return transactions
            return

    def get_transaction(self, book_id, matric_number):
        '''
        Get details of a transaction by querying the transactions table for transactions matching the given book id and student's matric number
        '''
        self.cursor.execute("SELECT * FROM public.transactions WHERE book_id='{}' AND matric_number='{}';".format(
                                                                                                            book_id,
                                                                                                            matric_number
                                                                                                        )
                                                                                                    )
        transaction = self.cursor.fetchone() or None
        return transaction       

    def get_borrowed_books(self, matric_number=None, book_id=None):
        '''
        Returns books borrowed identified either by matric number or book
        '''
        if matric_number:
            get_borrowed_books_command = "SELECT * FROM public.transactions WHERE matric_number='{}';".format(matric_number)
        elif book_id:
            get_borrowed_books_command = "SELECT * FROM public.transactions WHERE book_id='{}';".format(book_id)
        else:
            return
        self.cursor.execute(get_borrowed_books_command)
        borrowed_books = self.cursor.fetchall()
        return borrowed_books

    def get_student(self, matric_no: str):
        '''
        Returns an empty array if a student exists with a given matric number or a student's details if a student is found
        '''
        get_student_command = "SELECT * FROM public.students WHERE matric_number='{}';".format(matric_no)
        try:
            self.cursor.execute(get_student_command)
            student = self.cursor.fetchone() or []
        except Exception:
            return []
        return student

    def get_similar_students_by_name(self, student_name):
        get_similar_students_command = "SELECT * FROM public.students WHERE \
student_name LIKE '%{}%';".format(
                                    student_name,
                                )
        self.cursor.execute(get_similar_students_command)
        return self.cursor.fetchall()

    def get_student_by_details(self, student_name, matric_number):
        get_similar_students_command = "SELECT * FROM public.students WHERE \
student_name LIKE '%{}%'AND matric_number='{}';".format(
                                    student_name,
                                    matric_number
                                )
        self.cursor.execute(get_similar_students_command)
        return self.cursor.fetchall()

    def get_book(self, book_id: str):
        '''
        Returns an empty array if a book exists with a given id or a book's details if a book is found
        '''        
        get_book_command = "SELECT * FROM public.books WHERE book_id='{}';".format(book_id)
        try:
            self.cursor.execute(get_book_command)
            book = self.cursor.fetchone() or []
        except Exception:
            return []
        return book

    def get_user(self, user_id: int):
        '''
        Returns an empty array if a user exists with a given id or a user's details if a user is found
        '''        
        get_user_command = "SELECT * FROM public.users WHERE user_id='{}';".format(user_id)
        try:
            self.cursor.execute(get_user_command)
            user = self.cursor.fetchone() or []
        except Exception:
            return []
        else:
            return user

    def get_user_by_username(self, user_name: str):
        '''
        Returns an empty array if a user exists with a given username or a user's details if a user is found
        '''         
        get_user_by_username_command = "SELECT * FROM public.users WHERE user_name='{}';".format(user_name)
        try:
            self.cursor.execute(get_user_by_username_command)
            user = self.cursor.fetchone() or []
        except Exception:
            return []
        else:
            return user

    def get_all_borrowed_books(self, matric_number):
        '''
        Returns all existing books that have been borrowed out to students
        '''
        get_all_borrowed_books_command = "SELECT count(*) FROM public.transactions WHERE matric_number='{}';".format(matric_number)
        self.cursor.execute(get_all_borrowed_books_command)
        # Returns a tuple containing a single element so it is sliced to get the needed integer
        number_of_books_borrowed = self.cursor.fetchone()[0]
        return number_of_books_borrowed

    def get_user_credentials(self, user_name):
        '''
        Returns login credentials for a g given user identified by a username from the database
        '''
        get_user_credentials_command = "SELECT user_name, user_password FROM public.users WHERE user_name='{}';".format(user_name)
        try:
            self.cursor.execute(get_user_credentials_command)
            user_credentials = self.cursor.fetchone()
            if not user_credentials:
                return
        except Exception:
            return
        else:
            return user_credentials

    def get_information(self):
        '''
        Manipulates details of all transactions such that book and student info for a particular transaction
        is well structured for insertion into the information tree view widget
        '''
        information = []
        transactions = self.get_transactions()
        if not transactions:
            return 
        for transaction in transactions:
            matric_number, book_id, date_issued = transaction
            student = self.get_student(matric_number)
            book = self.get_book(book_id)
            book_name = book[1]
            student_name = student[1]
            transaction_information = [book_id, matric_number, student_name, book_name, date_issued]
            information.append(transaction_information)
        return information

    def search_students(self, student_name, matric_number):
        '''
        Returns all students whose credentials match a query's return value from the database
        '''
        if all((student_name, matric_number)):
            results = self.get_student_by_details(student_name, matric_number) or []
        elif student_name:
            results = self.get_similar_students_by_name(student_name) or []
        else:
            results = [self.get_student(matric_number),] or []
        return results
    
    def search_transactions(self, search_book_id, student_matric_number):
        '''
        Manipulates details of a transaction so that book and student info for a particular transaction
        is well structured for insertion into the information tree view widget
        '''
        found_information = []
        transactions = []
        if all((search_book_id, student_matric_number)):
            transactions = [self.get_transaction(search_book_id, student_matric_number),]
        elif search_book_id:
            transactions = self.get_borrowed_books(book_id=search_book_id)
        else:
            transactions = self.get_borrowed_books(matric_number=student_matric_number)
        if not transactions:
            return 
        for transaction in transactions:
            matric_number, book_id, date_issued = transaction
            student = self.get_student(matric_number)
            book = self.get_book(book_id)
            book_name = book[1]
            student_name = student[1]
            transaction_information = [book_id, matric_number, student_name, book_name, date_issued]
            found_information.append(transaction_information)
        return found_information

    def get_user_security_credentials(self, user_name):
        '''
        Returns the security question and answer of a user identified by his or her username from the database
        '''
        get_user_security_credentials_command = "SELECT security_question, security_answer FROM public.users WHERE user_name='{}';".format(
                                                                                                                                    user_name
                                                                                                                                    )
        try:
            self.cursor.execute(get_user_security_credentials_command)
            user_security_credentials = self.cursor.fetchone()
            if not user_security_credentials:
                return
        except Exception:
            showerror(title="Fatal error", message="User security credentials have been manually tampered with from the database")
            return
        else:
            return user_security_credentials

    def get_admin_status(self, user_name):
        '''
        Returns the admin status of a user with a given user_name from the database
        '''
        get_admin_status_command = "SELECT admin_status FROM public.users WHERE user_name='{}';".format(user_name)
        try:
            self.cursor.execute(get_admin_status_command)
            admin_status = self.cursor.fetchone()
        except Exception:
            return
        else:
            return admin_status[0]

    def update_password(self, user_name, new_password):
        '''
        Updates password into the database for a given user identified by a username
        '''
        password_update_command = "UPDATE public.users SET user_password='{}' WHERE user_name='{}';".format(new_password, user_name)
        self.cursor.execute(password_update_command)
        return new_password

    def update_book_stock(self, book_details: tuple):
        '''
        Sets the value for available and current stock for a particular book
        '''
        book_stock_update_command = "UPDATE public.books SET available_stock='{}', current_stock='{}' WHERE book_id='{}';".format(
                                                                                                                            *book_details
                                                                                                                            )
        self.cursor.execute(book_stock_update_command)

    def issue_book(self, book_id, matric_number, available_stock, date_issued, current_window, book_name, student_name):
        '''
        Issue book identified by an ID to a student with a given matric number
        '''
        available_stock -= 1
        issue_book_command = "INSERT INTO public.transactions (book_id, matric_number, date_issued) VALUES ({}, '{}', '{}');".format(
                                                                                                                            book_id,
                                                                                                                            matric_number,
                                                                                                                            date_issued
                                                                                                                         )
        update_stock_command = "UPDATE public.books SET available_stock='{}' WHERE book_id='{}';".format(available_stock, book_id)
        self.cursor.execute(issue_book_command)
        self.cursor.execute(update_stock_command)
        return True

    def retrieve_book(self, book_id, matric_number, available_stock, current_window, book_name, student_name):
        '''
        Retrieves book identified by an ID to a student with a given matric number
        '''            
        available_stock += 1
        retrieve_book_command = "DELETE FROM public.transactions WHERE book_id='{}' AND matric_number='{}';".format(
                                                                                                                        book_id,
                                                                                                                        matric_number,
                                                                                                                    )
        update_stock_command = "UPDATE public.books SET available_stock='{}' WHERE book_id='{}';".format(available_stock, book_id)
        self.cursor.execute(retrieve_book_command)
        self.cursor.execute(update_stock_command)
        return True
        