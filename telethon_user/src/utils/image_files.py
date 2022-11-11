import os
import string
from random import choice

SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png']


def get_all_images(dir_path: str):
    return [
        os.path.join(dirpath, file) for (dirpath, subdirs, files) in os.walk(dir_path) for file in files
        if file.rsplit('.', 1)[-1].lower() in SUPPORTED_FORMATS
    ]


def generate_random_filename(filename: str) -> str:
    # we do not need path
    filename = filename.split('/')[-1]
    letters = string.ascii_lowercase
    splitted = filename.split('.')
    rand_string = ''.join(choice(letters) for i in range(10))
    if len(splitted) < 2:
        return rand_string + splitted[-1]

    return splitted[0][:4] + '.'.join([rand_string, splitted[-1]])
