# DOT-traincam
## a Python Department of Transportation Traffic Cam scraper

## Usage
save images (to `images` directory, nested folder structure per camera per day) 
`python save_camera_images.py`

convert yesterdays images to mp4 (requires ffmpeg)
`python convert_to_movie`

## Requirements

`python` version >3.8

[`ffmpeg`](https://ffmpeg.org/)

## Why

I love trains and want to know when they arrive/depart in the Portland, Oregon area.
`DOT-traincam` takes advantage of several Oregon and Washington Department of Transportation (DOT) traffic cameras which overlook train tracks. 

## How it works

`save_camera_images.py` is a simple script which reads in a list of cameras and their urls (currently stored in `trainlist.py`). Each camera is looped over infinitely and saved to its own folder for each day. 
