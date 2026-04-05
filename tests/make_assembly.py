import sys
import numpy as np

from tests import make_camera, make_reference_frame
from sample.assembly import Assembly

def make_assembly(name=None):
    assembly = Assembly(name)
    assembly.camera = make_camera.make_camera("test_camera")
    assembly.reference_frames = [
        make_reference_frame.make_reference_frame("ref_frame_1"),
        make_reference_frame.make_reference_frame("ref_frame_2")
    ]

    print(assembly)

if __name__ == "__main__":
    name = None
    if len(sys.argv) > 1:
        name = sys.argv[1]

    make_assembly(name)