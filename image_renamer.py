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
        self.exif_data = exif_data
        # return exif_data 

    def get_date_time(self):
        if 'DateTime' in self.exif_data:
            date_and_time = self.exif_data['DateTime']
            return date_and_time 


def main():
    date = image.date
    print(date)

if __name__ == '__main__':
    # If True, will use the file creation datetime
    # If False, will use a predefined format
    using_file_creation_date = False
    from_datetime_format = '%Y%m%d_%H%M%S'
    to_datetime_format = '%Y-%m-%d %H.%M.%S' # Dropbox Camera Uploads naming format

    input_directory = os.path.join(os.getcwd(), 'input')

    file_formats = ['*.JPG', '*.dng', '*.jpg', '*.mp4']



    for file_format in file_formats:
        glob_path = os.path.join(input_directory, file_format)

        filepaths = glob.glob(glob_path)

        for filepath in filepaths:
            filename, extension = os.path.splitext(filepath)
            filename = os.path.basename(filename)

            try:
                if using_file_creation_date:
                    with PILimage.open(filepath) as img:
                        image = Worker(img)
                        image_datetime = image.date
                        date_taken = datetime.datetime.strptime(image_datetime, '%Y:%m:%d %H:%M:%S')
                else:
                    date_taken = datetime.datetime.strptime(filename, from_datetime_format)

                new_filename = date_taken.strftime(to_datetime_format)
                
                new_filepath = os.path.join(input_directory, new_filename+extension)

                number = 0

                while os.path.exists(new_filepath):
                    number += 1
                    # new_filename, extension = os.path.splitext(new_filepath)
                    new_new_filename = new_filename + '.' + str(number)
                    new_filepath = os.path.join(input_directory, new_new_filename + extension)

                os.rename(filepath, new_filepath)

            except Exception as e:
                    print(e)