# DOT-traincam
## a Python Department of Transportation Traffic Cam scraper

## Usage
`python save_camera_images.py`

## Requirements

python version >3.8

## Why

I love trains and want to know when they arrive/depart in the Portland, Oregon area.
`DOT-traincam` takes advantage of several Oregon and Washington Department of Transportation (DOT) traffic cameras which overlook train tracks. 

## How it works

`save_camera_images.py` is a simple script which reads in a list of cameras and their urls (currently stored in `trainlist.py`). Each camera is looped over infinitely and saved to its own folder for each day. 
