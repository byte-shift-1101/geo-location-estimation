import os
import numpy as np
from sample import constants
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame
from sample.assembly import Assembly

def main():
    assembly = Assembly("sihaag")
    assembly.storage_path = os.path.join(constants.CONFIG_FOLDER, "assembly/sihaag.json")
    assembly.load()
    print(assembly)

    print(assembly.camera)
    for rf in assembly.reference_frames:
        print(rf)

    pixel_x, pixel_y = assembly.get_screen_point((1, 2, 3))
    print(f"Screen point: ({pixel_x}, {pixel_y})")

if __name__ == "__main__":
    main()