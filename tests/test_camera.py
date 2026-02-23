from sample.camera import Camera

def main():
    camera = Camera()
    camera.storage_path = "./configs/cameras/camera.json"
    camera.load()

    camera.focal_length = 30.0
    camera.sensor_width = 35.8713887894656
    print(camera)
    # print(camera.intrinsic_matrix_3x4)

if __name__ == "__main__":
    main()