import os
from sample import constants
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame
from sample.assembly import Assembly

def main():
    camera = Camera()
    camera.storage_path = constants.STANDARD_CAMERA_STORAGE_PATH
    camera.load()
    print(camera)

    ref = ReferenceFrame()
    ref.storage_path = os.path.join(constants.STANDARD_REFERENCE_FRAME_FOLDER, "drone_reference_frame.json")
    ref.load()
    print(ref)

    world = ReferenceFrame()
    world.storage_path = os.path.join(constants.STANDARD_REFERENCE_FRAME_FOLDER, "world_reference_frame.json")
    world.load()
    print(world)

    assembly = Assembly("main")
    assembly.storage_path = os.path.join(constants.STANDARD_ASSEMBLY_FOLDER, "main_assembly.json")
    assembly.load()

    assembly.camera = camera
    assembly.add_reference_frame(world)
    assembly.add_reference_frame(ref)
    print(assembly)

    # to_dict = lambda instance: {key: value for key, value in vars(instance.__class__).items() if isinstance(value, Parameter) and not isinstance(value, PathParameter)}
    # print(to_dict(camera))
    # print(to_dict(ref))
    # print(to_dict(world))
    # print(to_dict(assembly))

    # print(test(assembly))

if __name__ == "__main__":
    main()