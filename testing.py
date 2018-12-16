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
    input_directory = os.path.join(os.getcwd(), 'input')
    glob_path = os.path.join(input_directory, '*.jpg')

    filepaths = glob.glob(glob_path)

    for filepath in filepaths:
        filename, extension = os.path.splitext(filepath)

        try:
            # img = PILimage.open(path + filename)
            img = PILimage.open(filepath)
            image = Worker(img)
            date = image.date
            print(date)

        except Exception as e:
            print(e)
