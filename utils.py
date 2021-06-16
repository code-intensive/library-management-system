from datetime import datetime
from constants import ERROR_DIR, MODE
from os import path


def center_window(window_to_center, non_resizable: bool=True, height=400, width=600):
    '''
    Takes in a tkinter Tk or Toplevel and centers it on the screen
    '''
    window_height = window_to_center.winfo_reqheight()
    window_width = window_to_center.winfo_reqwidth()
    screen_width = window_to_center.winfo_screenwidth()
    screen_height = window_to_center.winfo_screenheight()
    right_window_position = int(screen_width/3 - window_width/3)
    bottom_window_position = int(screen_height/3 - window_height/2)
    window_to_center.geometry("{}x{}+{}+{}".format(width, height, right_window_position, bottom_window_position))
    if non_resizable:
        window_to_center.resizable(0, 0)

def get_current_date(day_only=False, month_only=False, year_only=False):
    '''
    Return the `current date` in `yyyy-mm-dd` format
    '''
    if day_only:
        return datetime.today().date().day
    if month_only:
        return datetime.today().date().month
    if year_only:
        return datetime.today().date().year
    return datetime.today().date()

def get_current_time():
    '''
    Returns the string format of the current time in the 12 hour format\n
    `02/02/21   04:34:18 pm`
    '''
    return datetime.strftime(datetime.today(), "%d/%m/%y   %I:%M:%S %p")

def assign_position(number: int):
    '''
    Returns a `st`,`nd`, `rd` or `th` depending on the number given as an argument for the parameter number
    '''
    number = int(number)
    if number == 1:
        return "{}st".format(number)
    elif number == 2:
        return "{}nd".format(number)
    elif number == 3:
        return "{}rd".format(number)
    else:
        return "{}th".format(number)

def log_errors(error_message):
    error_message = "Error: %s"%error_message
    global MODE
    '''
    Saves all caught errors and logs them using the current date and time,
    Using the seconds ensures that all logged errors are well differentiated,
    '''
    position = assign_position(get_current_date(day_only=True))
    error_message_file = datetime.strftime(datetime.today(), "%A %B {} %Y".format(position))
    logged_error_name = path.join(ERROR_DIR, error_message_file)
    error_file_does_not_exist = path.exists(path.join(logged_error_name, ".txt"))
    if error_file_does_not_exist:
        MODE = "w"

    with open("%s.txt"%logged_error_name, MODE) as logged_errors:
        logged_errors.writelines("#"*150)
        logged_errors.writelines("\n")
        logged_errors.writelines(get_current_time())
        logged_errors.writelines("\n")
        logged_errors.writelines("_"*150)
        logged_errors.writelines("\n")
        logged_errors.writelines(error_message)
        logged_errors.writelines("\n")
        logged_errors.writelines("="*150)
        logged_errors.writelines("\n\n")
    return logged_error_name + ".txt"

def convertToBinaryData(filename):
    '''
    Converts files such as png or other image formats to bytes so as to enable
    data upload
    '''
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def to_string(iterable: list or tuple):
    '''
    Converts a tuple to a string fit for postgres database command operations
    '''
    string_format = ''
    for i in iterable:
        string_format += f"{ repr(i) }, "
    return string_format[:-2]

def show(password_entry, show_switch):
    '''
    Display or hide the value of an entry
    '''
    print("switch is", show_switch.get())
    password = password_entry.get()
    if show_switch.get():
        password_entry.insert(0, password)
    else:
        hidden_password = "*" * len(password)
        password_entry.insert(0, hidden_password)

def _clear_search(entry_widgets, text_variables):
    for entry_widget, text_variable in zip(entry_widgets, text_variables):
        entry_widget.insert(0, "")
        text_variable.set("")  