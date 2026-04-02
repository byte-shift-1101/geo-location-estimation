import os
from sample import constants, utils
from sample.camera import Camera
from sample.parameter import Parameter, PathParameter
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

    # assembly = Assembly("main")
    # assembly.camera = camera
    # assembly.add_reference_frame(world)
    # assembly.add_reference_frame(ref)
    # print(assembly)

    # to_dict = lambda instance: {key: value for key, value in vars(instance.__class__).items() if isinstance(value, Parameter) and not isinstance(value, PathParameter)}
    # print(to_dict(camera))
    # print(to_dict(ref))
    # print(to_dict(world))
    # print(to_dict(assembly))

    # print(test(assembly))

if __name__ == "__main__":
    main()