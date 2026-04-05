import sys
import numpy as np

from sample.reference_frame import ReferenceFrame

def make_reference_frame(name=None):
    reference_frame = ReferenceFrame(name)
    reference_frame.position = np.array([1.0, 2.0, 3.0])
    reference_frame.orientation = np.array([45.0, 30.0, 60.0])
    reference_frame.parent_frame = None
    
    print(reference_frame)

if __name__ == "__main__":
    name = None
    if len(sys.argv) > 1:
        name = sys.argv[1]

    make_reference_frame(name)