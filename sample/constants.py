import math

# Tweakble constants
STANDARD_CAMERA_STORAGE_PATH = "./configs/cameras/camera.json"
# OVERWRITE_CAMERA_CONFIG = False

UPDATE_JSON_ON_ATTRIBUTE_SET = True
AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS = True

# Fixed constants
# UPDATED_THIS_RUN = False

# TODO: Centralize the 3 parameters

FOCAL_LENGTH_KEY = "focal_length"
SENSOR_WIDTH_KEY = "sensor_width"
SENSOR_HEIGHT_KEY = "sensor_height"
HORIZONTAL_FIELD_OF_VIEW_KEY = "horizontal_field_of_view"
VERTICAL_FIELD_OF_VIEW_KEY = "vertical_field_of_view"
IMAGE_WIDTH_KEY = "image_width"
IMAGE_HEIGHT_KEY = "image_height"

PARAMETER_NAMES = {
    FOCAL_LENGTH_KEY: "Focal Length",
    SENSOR_WIDTH_KEY: "Sensor Width",
    SENSOR_HEIGHT_KEY: "Sensor Height",
    HORIZONTAL_FIELD_OF_VIEW_KEY: "Horizontal Field of View",
    VERTICAL_FIELD_OF_VIEW_KEY: "Vertical Field of View",
    IMAGE_WIDTH_KEY: "Image Width",
    IMAGE_HEIGHT_KEY: "Image Height"
}

PARAMETER_UNITS = {
    FOCAL_LENGTH_KEY: "mm",
    SENSOR_WIDTH_KEY: "mm",
    SENSOR_HEIGHT_KEY: "mm",
    HORIZONTAL_FIELD_OF_VIEW_KEY: "degrees",
    VERTICAL_FIELD_OF_VIEW_KEY: "degrees",
    IMAGE_WIDTH_KEY: "pixels",
    IMAGE_HEIGHT_KEY: "pixels"
}

DEG_TO_RAD = math.pi / 180
RAD_TO_DEG = 180 / math.pi