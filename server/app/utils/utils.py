import os

def cleanup(image_path):
    if image_path is not None:
        if os.path.exists(image_path):
            os.remove(image_path)