import json
import requests
import config
import urllib
import os
import glob
import imageio
from PIL import Image

api_token = config.token
dates_call = 'https://api.nasa.gov/EPIC/api/natural/available?api_key=' + api_token
img_call = 'https://api.nasa.gov/EPIC/api/natural/date/{}?api_key=' + api_token
img_url = 'https://epic.gsfc.nasa.gov/archive/natural/{}/{}/{}/png/{}.png' # YYYY/MM/DD/png/title

def get_images(date):
    response = requests.get(img_call.format(date))
    if response.status_code == 200:
        data = response.json()
        print 'Loading images. This might take a while...'
        for index, item in enumerate(data):
            urllib.urlretrieve(img_url.format(date[0:4], date[5:7], date[8:10], item['image']), str(index+100) + '.png')
            print 'Image retrieved [{}/{}]'.format(index+1, len(data))
        create_gif()

def create_gif():
    with imageio.get_writer('earth.gif', mode='I') as writer:
        images = glob.glob('*.png')
        images.sort()
        for img in images:
            # change image quality first
            im = Image.open(img)
            size = im.size
            ratio = 0.4
            reduced_size = int(size[0] * ratio), int(size[1] * ratio)
            im_resized = im.resize(reduced_size, Image.ANTIALIAS)
            im_resized.save(img, "PNG")
            # add image to gif
            image = imageio.imread(img)
            writer.append_data(image)
            # delete image
            os.remove(img)
        print 'Done.'

# change the date here
get_images('2015-10-31')
