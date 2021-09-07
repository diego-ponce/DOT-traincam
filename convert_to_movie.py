"""Converts a directory of images into a movie using FFMPEG"""
import glob
import os
import subprocess
from datetime import date, datetime, timedelta

from camera import Camera
from trainlist import camera_dict


def convert_to_mp4(inpath="", outfile=None, framerate=1):
    """calls ffmpeg to convert jpg files to mp4"""

    if outfile is None:
        outfile = "out.mp4"
    glob_pattern = os.path.join(inpath, "*.jpg")
    call_list = [
        "ffmpeg",
        "-framerate",
        f"{framerate}",
        "-pattern_type",
        "glob",
        "-i",
        f"{glob_pattern}",
        "-y",
        "-vf",
        "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        f"{outfile}",
    ]

    subprocess.run(call_list)


def directory_contains_extensions(path=".", search_list=[".jpg"]):
    """checks directory for a list of extensions"""

    extensions = {os.path.splitext(x)[1] for x in os.listdir(path)}
    return not not set(search_list).intersection(extensions)


def standardized_framerate(dirname, filetype, duration):
    """returns a framerate to generate a video of certain duration"""

    if duration < 0:
        raise Exception("duration must be a positive number")
    if "." not in filetype:
        filetype = "." + filetype

    glob_pattern = os.path.join(dirname, "*" + filetype)
    files = glob.glob(glob_pattern)
    if not files:
        raise Exception(f"No files of filetype {filetype} found in {dirname}")
    return round(len(files) / duration, 2)


def create_mp4(camera, date):
    """creates an mp4 from the directory for a given camera on a given date"""

    infile = os.path.join("./images/", camera.name, date)
    outfile = os.path.join("./mp4s/", camera.name, date + ".mp4")
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    framerate = standardized_framerate(infile, "jpg", 180)
    convert_to_mp4(inpath=infile, outfile=outfile, framerate=framerate)


def main():
    today = date.today()
    yesterday = today - timedelta(days=1)
    date_str = str(yesterday).split(" ")[0]
    cameras = [Camera(name=k, url=v) for k, v in camera_dict.items()]
    camera = cameras[1]
    for camera in cameras[:1]:
        create_mp4(camera, date_str)


if __name__ == "__main__":
    main()
