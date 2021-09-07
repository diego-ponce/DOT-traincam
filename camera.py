"""
a Camera class to hold data related to web accessible cameras
"""


class Camera:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.current_image = None

    def __str__(self):
        return f"Camera: {self.name}"

    def __repr__(self):
        return f'Camera("{self.name}","{self.url}")'
