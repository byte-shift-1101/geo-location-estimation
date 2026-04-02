import os
import numpy as np
from sample import constants
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame
from sample.assembly import Assembly

def main():
    camera = Camera("siyi_a8_mini")
    camera.focal_length = 21.0
    camera.sensor_width = 35.871388789465605
    camera.sensor_height = 25.704851173919568
    camera.horizontal_field_of_view = 81.0
    camera.vertical_field_of_view = 62.93495402960169
    camera.image_width = 1920
    camera.image_height = 1080

    ref = ReferenceFrame("drone")
    ref.position = [1.0, 2.0, 3.0]
    ref.orientation = [10.0, 20.0, 30.0]

    world = ReferenceFrame("world")
    world.position = [0.0, 0.0, 0.0]
    world.orientation = [0.0, 0.0, 0.0]

    assembly = Assembly("sihaag")
    assembly.camera = camera
    assembly.add_reference_frame(world)
    assembly.add_reference_frame(ref)
    print(assembly)

if __name__ == "__main__":
    main()