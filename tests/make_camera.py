import sys
from sample.camera import Camera

def make_camera(camera_name=None):
    camera = Camera(camera_name)
    camera.focal_length = 21.0
    camera.sensor_width = 35.8713887894656
    camera.sensor_height = 25.704851173919568
    camera.horizontal_field_of_view = 81.0
    camera.vertical_field_of_view = 62.93495402960169
    camera.image_width = 1920
    camera.image_height = 1080
    camera.reference_frame = None

    print(camera)

if __name__ == "__main__":
    camera_name = None
    if len(sys.argv) > 1:
        camera_name = sys.argv[1]

    make_camera(camera_name)