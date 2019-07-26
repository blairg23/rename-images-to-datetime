'''
Stolen straight from https://stackoverflow.com/a/51337247/1224827
'''
try:
    import PIL
    import PIL.Image as PILimage
    from PIL import ImageDraw, ImageFont, ImageEnhance
    from PIL.ExifTags import TAGS, GPSTAGS
    import os
    import glob
    import datetime
    import json
except ImportError as err:
    exit(err)


class Worker(object):
    def __init__(self, img):
        self.img = img
        self.get_exif_data()
        self.date =self.get_date_time()
        super(Worker, self).__init__()

    def get_exif_data(self):
        exif_data = {}
        info = self.img._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        # self._exif_data = exif_data
        return exif_data

    def get_date_time(self):
        if 'DateTime' in self.exif_data:
            print('exif:', self.exif_data)
            print('-------\n')
            # print(json.dumps(self.exif_data, indent=4))
            date_and_time = self.exif_data.get('DateTime')
            print('date_and_time:', date_and_time)
            # For those weird cases where midnight is portrayed as 24:00:00 instead of 00:00:00
            date_and_time = date_and_time.replace(' 24:', ' 00:')
            date_and_time = datetime.datetime.strptime(date_and_time, '%Y:%m:%d %H:%M:%S')

            if self._debug:
                print('date_and_time:', date_and_time)

            return date_and_time
        else:
            print('DateTime not found...')
            if self._debug:
                print('exif:', self._exif_data)


def main():
    date = image.date
    print(date)


if __name__ == '__main__':
    # If True, will use the file creation datetime
    # If False, will use a predefined format
    DEBUG = True
    using_file_creation_date = True
    from_datetime_format = '%Y%m%d_%H%M%S'
    to_datetime_format = '%Y-%m-%d %H.%M.%S'  # Dropbox Camera Uploads naming format

    input_directory = os.path.join(os.getcwd(), 'input')

    file_formats = ['*.jpg', '*.png', '*.mp4']

    print('--------------------------------------------------------')
    for file_format in file_formats:
        print('FILE FORMAT:', file_format)
        glob_path = os.path.join(input_directory, file_format)
        filepaths = glob.glob(glob_path)

        if DEBUG:
            print('GLOB PATH:', glob_path)
            print('FILEPATHS:', filepaths)

        filepaths_to_rename = {}

        for filepath in filepaths:
            filename, extension = os.path.splitext(filepath)
            filename = os.path.basename(filename)

            try:
                if using_file_creation_date:
                    with PILimage.open(filepath) as img:
                        image = Worker(img, debug=DEBUG)
                        date_taken = image._date
                else:
                    date_taken = datetime.datetime.strptime(filename, from_datetime_format)

                new_filename = date_taken.strftime(to_datetime_format)
                
                new_filepath = os.path.join(input_directory, new_filename+extension)

                number = 0

                if DEBUG:
                    print('new_filepath:', new_filepath)
                    print('isfile:', os.path.isfile(new_filepath))
                    print('exists:', os.path.exists(new_filepath))

                while os.path.isfile(new_filepath):
                    number += 1
                    # new_filename, extension = os.path.splitext(new_filepath)
                    new_new_filename = new_filename + '.' + str(number)
                    new_filepath = os.path.join(input_directory, new_new_filename + extension)

                print(f'Renaming {filepath} to {new_filepath}')

                os.rename(filepath, new_filepath)

            except Exception as e:
                print('filename:', filename)
                print(e)
                print('\n')

        # print(filepaths_to_rename)
        # for filepath, new_filepath in filepaths_to_rename.items():
        #     print(f'Renaming {filepath} to {new_filepath}')
        #     os.rename(filepath, new_filepath)
        print('\n--------------------------------------------------------')