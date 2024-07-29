"""Converts a directory of images into a movie using FFMPEG."""
import glob
import os
import subprocess
from datetime import date, datetime, timedelta

from camera import Camera
from trainlist import camera_dict


def convert_to_mp4(inpath="", outfile=None, framerate=1):
    """Calls ffmpeg to convert jpg files to mp4."""

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
    """Checks directory for a list of extensions."""

    extensions = {os.path.splitext(x)[1] for x in os.listdir(path)}
    return not not set(search_list).intersection(extensions)


def standardized_framerate(dirname, filetype, duration):
    """Returns a framerate to generate a video of certain duration."""

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
    """Creates an mp4 from the directory for a given camera on a given date."""

    if isinstance(camera, Camera):
        name = camera.name
    elif isinstance(camera, str):
        name = camera
    else:
        raise Error("camera not a valid string or Camera object")
    infile = os.path.join("./images/", name, date)
    outfile = os.path.join("./mp4s/", name, date + ".mp4")
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    framerate = standardized_framerate(infile, "jpg", 180)
    convert_to_mp4(inpath=infile, outfile=outfile, framerate=framerate)


def main():
    today = date.today()
    find_date = today - timedelta(days=1)
    find_date_str = str(find_date).split(" ")[0]

    # walk for directories
    # extract date
    # loop through
    # check for mp4 file
    # add if not already there
    # exclude today
    for root, dirs, files in os.walk("./images"):
        for folder in dirs:
            cam_path, date_str = os.path.split(os.path.join(root, folder))
            base, camera = os.path.split(cam_path)
            if date_str == find_date_str:
                try:
                    create_mp4(camera, date_str)
                except Exception as e:
                    print(f"could not write {camera} for {date_str}\n{e}")
    print("finished writing mp4s")
    # cameras = [Camera(name=k, url=v) for k, v in camera_dict.items()]
    # camera = cameras[1]
    # for camera in cameras:
    #     create_mp4(camera, date_str)


if __name__ == "__main__":
    main()
