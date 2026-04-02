import os
from sample import constants, utils
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame
from sample.assembly import Assembly

def main():
    camera = Camera()
    camera.storage_path = constants.STANDARD_CAMERA_STORAGE_PATH
    utils.load(camera)
    print(camera)

    ref = ReferenceFrame()
    ref.storage_path = os.path.join(constants.STANDARD_REFERENCE_FRAME_FOLDER, "drone_reference_frame.json")
    utils.load(ref)
    print(ref)

    world = ReferenceFrame()
    world.storage_path = os.path.join(constants.STANDARD_REFERENCE_FRAME_FOLDER, "world_reference_frame.json")
    utils.load(world)
    print(world)

    assembly = Assembly("main")
    assembly.camera = camera
    assembly.add_reference_frame(world)
    assembly.add_reference_frame(ref)
    print(assembly)

if __name__ == "__main__":
    main()