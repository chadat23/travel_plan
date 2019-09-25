import os


def _make_uri(prefix, folder, file_name):
    path = os.path.join(folder, file_name)

    return prefix + path


class Config:
    EMAIL_ADDRESS = "<email@address.com>"
    EMAIL_PASSWORD = "<password>"
    DEFAULT_EMAIL_LIST = ["<default@email.1>", "d<efault@email.2>"]

    PDF_FOLDER_PATH = "<example/folder/path/to/file/save/location>"

    SECRET_KEY = '<24? character security key>'
    SQLALCHEMY_DB_PREFIX = '<sqlite:///>'
    DB_FOLDER_PATH = "<example/folder/path/to/db/location>"
    DB_FILE_NAME = "<site.db>"
    SQLALCHEMY_DATABASE_URI = _make_uri(SQLALCHEMY_DB_PREFIX, DB_FOLDER_PATH, DB_FILE_NAME)
