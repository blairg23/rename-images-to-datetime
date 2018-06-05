import os
import datetime
import glob

from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

if __name__ == '__main__':
    input_directory = os.path.join(os.getcwd(), 'input')

    glob_path = os.path.join(input_directory, '*.*')

    filepaths = glob.glob(glob_path)

    for filepath in filepaths:
        filename, extension = os.path.splitext(filepath)
        # print(get_exif(filepath)['DateTimeOriginal'])
        date_taken = datetime.datetime.strptime(get_exif(filepath)['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')

        new_filename = date_taken.strftime('%Y-%m-%dT%H.%M.%S')

        new_filename += extension

        new_filepath = os.path.join(input_directory, new_filename)

        number = 0

        while os.path.exists(new_filepath):
            number += 1
            new_filename, extension = os.path.splitext(new_filepath)
            new_filename += '.' + str(number) + extension
            new_filepath = os.path.join(input_directory, new_filename)

        os.rename(filepath, new_filepath)