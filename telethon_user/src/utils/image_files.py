import os

SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png']


def get_all_images(dir_path: str):
    return [
        os.path.join(dirpath, file) for (dirpath, subdirs, files) in os.walk(dir_path) for file in files
        if file.rsplit('.', 1)[-1].lower() in SUPPORTED_FORMATS
    ]
