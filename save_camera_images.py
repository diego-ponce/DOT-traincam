"""
Capture traffic camera jpgs to a file by camera and by day


"""

import hashlib
import logging
import os
import time
import urllib.request
from datetime import datetime
from urllib.error import URLError

from camera import Camera
from trainlist import camera_dict

logging.basicConfig(
    filename="save_camera_images.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

RETRIABLE_EXCEPTIONS = (URLError,)


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


def get_image(url, max_retries=5, wait_time=2):
    """return image blob from url"""
    for _ in range(max_retries):
        try:
            image = urllib.request.urlopen(url).read()
            break
        except RETRIABLE_EXCEPTIONS as e:
            error = f"a retriable error occurred: {e}"
            logging.error(error)
            time.sleep(wait_time)
    else:
        error = f"max retries exceeded for {url}"
        logging.error(error)
        return None
    return image


def save_camera_image(camera, filepath=None):
    """save image of camera to file"""

    print("[+] retrieving {}".format(camera))
    try:
        if filepath is None:
            filepath = make_filepath(camera.name)
        urlfile = open(filepath, "wb")
        # TODO validate file before writing
        urlfile.write(camera.current_image)
    except Exception as err:
        urlfile.close()
        os.remove(filepath)
        logging.error(err)


def main():
    logging.info("Starting save_camera_images.")
    count = -1
    previous_hashes = set()
    while True:
        # TODO make this easier to understand
        count = (count + 1) % 5
        if count == 0 and 4 < datetime.now().hour < 22:
            cameras = [Camera(name=k, url=v) for k, v in camera_dict.items()]
            image_hashes = set()
            for camera in cameras:
                camera.current_image = get_image(camera.url)
                if camera.current_image is None:
                    continue
                image_hash = hashlib.md5(camera.current_image).hexdigest()
                image_hashes.add(image_hash)
                if image_hash not in previous_hashes:
                    save_camera_image(camera)
                time.sleep(1)
            previous_hashes = image_hashes.copy()
        time.sleep(24)


if __name__ == "__main__":
    main()
