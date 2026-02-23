from sample import constants
from sample.camera import Camera

def main():
    camera = Camera()
    camera.storage_path = constants.STANDARD_CAMERA_STORAGE_PATH
    camera.load()
    # print(camera.intrinsic_matrix_3x4)

if __name__ == "__main__":
    main()