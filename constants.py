from os import path
from sys import platform


# filesystem paths
BASE_DIR = path.abspath(path.dirname(__file__))
ERROR_DIR = path.join(BASE_DIR, "Logs")
WINDOW_ICON_BITMAP_PATH = path.join(BASE_DIR, "imgs/libico.ico")
WINDOW_ICON_PHOTO_PATH = path.join(BASE_DIR, "imgs/libico.gif")


# Database credentials
DATABASE_NAME = "ogitech library"
DATABASE_OWNER = "postgres"
DATABASE_PASSWORD = "~8373"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_CREDENTIALS = (DATABASE_NAME, DATABASE_OWNER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT)


# Window titles
SHORT_WINDOW_TITLE = "OGILIB"
INSTITUTE_NAME = "OGITECH"
WINDOW_TITLE = "{} LIBRARY MANAGEMENT SYSTEM ({})".format(INSTITUTE_NAME, SHORT_WINDOW_TITLE)
FORGOT_PASSWORD_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - PASSWORD RECOVERY"
INDEX_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - HOME"
REGISTER_STUDENT_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - ADD STUDENT"
ADD_BOOK_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - ADD BOOK"
CREATE_USER_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - CREATE USER"
DATABASE_SETUP_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - DATABASE SETUP"
UNREGISTER_STUDENT_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - UNREGISTER STUDENT"
REMOVE_BOOK_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - REMOVE BOOK"
DELETE_USER_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - DELETE USER"
ISSUE_BOOK_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - ISSUE BOOK"
RETRIEVE_BOOK_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - RETRIEVE BOOK"
STUDENTS_INFORMATION_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - STUDENTS INFORMATION"
BOOKS_INFORMATION_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - BOOKS INFORMATION"
USERS_INFORMATION_WINDOW_TITLE = SHORT_WINDOW_TITLE + " - USERS INFORMATION"


# Colors
ADD_STUDENT_WINDOW_BACKGROUND = "#151720"
DEFAULT_BACKGROUND_COLOR = "#d1c4c4"
DEFAULT_FOREGROUND_COLOR = "#000000"
LOGIN_BACKGROUND_COLOR = DEFAULT_BACKGROUND_COLOR


# Fonts
HEADER_FONT_1 = ("Times new roman", 22, 'bold')
HEADER_FONT_2 = ("Arial bold", 18, "bold")
DEFAULT_FONT = ("Times new roman", 12)
DEFAULT_BUTTON_FONT = ("Times new roman", 8)
DEFAULT_ENTRY_FONT = ("Times New roman", 14)
FONT_1 = ("Times New roman", 18)
FONT_10 = "-family {Franklin Gothic Medium} -size 13"
INDEX_ENTRY_FONT = ("Times new roman", 18)
DROPDOWN_FONT = ("Times new roman", 10)
DEFAULT_LABEL_FONT = ('Comic Scan Ms', 10, 'bold')
INDEX_LABEL_FONT = ("Times new roman", 18, "bold")
HEADER_FONT = ('AlGERIAN', 25, 'bold')


# Dropdown menus
SECURITY_QUESTIONS = (
                        'What is your lucky number?',
                        'What was your first nick name?',
                        'What is your special combination?',
                    )

DEPARTMENT_CHOICE_LIST = (
            'Computer Science',
            'Electrical Engineering',
            'Computer Engineering',
            'Science Laboratory Technology',
            'Banking And Finance',
            'Mass Communication',
            'Building Management',
            'Estate Management',
            'Architectural Technology',
            'Public Administration',
            'Business Administration',
)

ABBRV_DEPARTMENT_MATRIC = (
                            'NCSF',
                            'NEEF',
                            'NCEF',
                            'NSLF',
                            'NBFF',
                            'NMCF',
                            'NBMF',
                            'NEMF',
                            'NATF',
                            'NPAF',
                            'NBAF',
)


MATRIC_RE_GROUP = '|'.join(ABBRV_DEPARTMENT_MATRIC)

# Others
MODE = "a"
WIN32 = platform == "win32"
LINUX = platform == "linux"

# regular expression patterns
MATRIC_NUMBER_PATTERN = r"(%s)/([0|1][0-9]|[2][0-1])/[0-1]\d{3}"%(MATRIC_RE_GROUP)
PHONE_NUMBER_PATTERN = r"^(091|090|081|080|070)[0-9]{8}$"
