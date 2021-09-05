"""
Capture traffic camera jpgs to a file by camera and by day


"""

import os
import time
import urllib.request
from datetime import datetime

from trainlist import camera_dict


class Camera:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return f"Camera: {self.name}"

    def __repr__(self):
        return f'Camera("{self.name}","{self.url}")'


def make_filepath(camera_name):
    """generate a filename using date and camera_name"""

    camera_dir = os.path.join(os.getcwd(), "images", camera_name)
    today_str = str(datetime.now()).split(" ")[0]
    path = os.path.join(camera_dir, today_str)
    if not os.path.exists(path):
        os.makedirs(path)
    file_time = str(datetime.now()).split(".")[0]
    filename = camera_name + " " + file_time
    file_path = os.path.join(path, filename + ".jpg")
    return file_path


def save_camera_image(camera, filepath=None):
    """save image of camera to file"""

    print("[+] retrieving {}".format(camera))
    try:
        if filepath is None:
            filepath = make_filepath(camera.name)
        urlfile = open(filepath, "wb")
        # TODO validate file before writing
        urlfile.write(urllib.request.urlopen(camera.url).read())
    except Exception as err:
        urlfile.close()
        os.remove(filepath)
        print(str(err) + " " + filepath)


def main():
    count = -1
    while True:
        # TODO make this easier to understand
        count = (count + 1) % 5
        if count == 0 and 4 < datetime.now().hour < 22:
            cameras = [Camera(name=k, url=v) for k, v in camera_dict.items()]
            for camera in cameras:
                save_camera_image(camera)
                time.sleep(1)
        time.sleep(24)


if __name__ == "__main__":
    main()
