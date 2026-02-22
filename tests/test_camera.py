from sample.camera import Camera

def main():
    camera = Camera()
    camera.focal_length = 21.0
    camera.horizontal_field_of_view = 81.0
    camera.vertical_field_of_view = 62.93495402960169
    camera.image_width = 1920
    camera.image_height = 1080
    print(camera)

    # camera.save()

if __name__ == "__main__":
    main()