import os
from sample import constants, utils
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame

def main():
    camera = Camera()
    camera.storage_path = constants.STANDARD_CAMERA_STORAGE_PATH
    utils.load(camera)
    print(camera)

    ref = ReferenceFrame()
    ref.storage_path = os.path.join(constants.STANDARD_REFERENCE_FRAME_FOLDER, "drone_reference_frame.json")
    utils.load(ref)
    ref.position = [4, 5, 6]
    
    print(ref)

if __name__ == "__main__":
    main()