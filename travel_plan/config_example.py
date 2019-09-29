import os


def _make_uri(prefix, folder, file_name):
    path = os.path.join(folder, file_name)

    return prefix + path


class Config:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "<email@address.com>"
    MAIL_PASSWORD = "<password>"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    DEFAULT_EMAIL_LIST = ["<default@email.1>", "d<efault@email.2>"]

    PDF_FOLDER_PATH = "<example/folder/path/to/file/save/location>"

    SECRET_KEY = '<24? character security key>'
    SQLALCHEMY_DB_PREFIX = '<sqlite:///>'
    DB_FOLDER_PATH = "<example/folder/path/to/db/location>"
    DB_FILE_NAME = "<site.db>"
    SQLALCHEMY_DATABASE_URI = _make_uri(SQLALCHEMY_DB_PREFIX, DB_FOLDER_PATH, DB_FILE_NAME)
