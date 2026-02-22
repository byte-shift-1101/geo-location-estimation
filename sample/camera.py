import json
import math
import os
import sample.constants as constants

class Camera:
    def __init__(self):
        self._focal_length = None
        self._sensor_width = None
        self._sensor_height = None
        self._horizontal_field_of_view = None
        self._vertical_field_of_view = None
        self._image_width = None
        self._image_height = None

        self._storage_path = self._generate_unique_path()
        self._save_to_json()

    @property
    def focal_length(self):
        return self._focal_length

    @focal_length.setter
    def focal_length(self, value):
        if value is None:
            raise ValueError("Cannot set focal length to None.")
        elif value <= 0:
            raise ValueError("Focal length must be greater than 0.")
        
        self._focal_length = value
        if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
            self._auto_calculate_fov()
            self._auto_calculate_sensor_size()
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    @property
    def sensor_width(self):
        return self._sensor_width

    @sensor_width.setter
    def sensor_width(self, value):
        if value is None:
            raise ValueError("Cannot set sensor width to None.")
        elif value <= 0:
            raise ValueError("Sensor width must be greater than 0.")

        self._sensor_width = value
        if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
            self._auto_calculate_fov()
            self._auto_calculate_focal_length()
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    @property
    def sensor_height(self):
        return self._sensor_height

    @sensor_height.setter
    def sensor_height(self, value):
        if value is None:
            raise ValueError("Cannot set sensor height to None.")
        elif value <= 0:
            raise ValueError("Sensor height must be greater than 0.")
        
        self._sensor_height = value
        if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
            self._auto_calculate_fov()
            self._auto_calculate_focal_length()
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    @property
    def horizontal_field_of_view(self):
        return self._horizontal_field_of_view

    @horizontal_field_of_view.setter
    def horizontal_field_of_view(self, value):
        if value is None:
            raise ValueError("Cannot set horizontal field of view to None.")
        elif (value < 0 or value > 180):
            raise ValueError("Horizontal field of view must be between 0 and 180 degrees.")
        
        self._horizontal_field_of_view = value
        if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
            self._auto_calculate_focal_length()
            self._auto_calculate_sensor_size()
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    @property
    def vertical_field_of_view(self):
        return self._vertical_field_of_view

    @vertical_field_of_view.setter
    def vertical_field_of_view(self, value):
        if value is None:
            raise ValueError("Cannot set vertical field of view to None.")
        elif (value < 0 or value > 180):
            raise ValueError("Vertical field of view must be between 0 and 180 degrees.")
        
        self._vertical_field_of_view = value
        if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
            self._auto_calculate_focal_length()
            self._auto_calculate_sensor_size()
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    @property
    def storage_path(self):
        return self._storage_path

    @storage_path.setter
    def storage_path(self, value):
        if value is None:
            raise ValueError("Storage path cannot be None.")
        elif not os.path.exists(value):
            raise ValueError("File path does not exist.")
        
        self._storage_path = value
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    @property
    def image_width(self):
        return self._image_width
    
    @image_width.setter
    def image_width(self, value):
        if value is None:
            raise ValueError("Image width cannot be None.")
        elif value <= 0:
            raise ValueError("Image width must be greater than 0.")
        
        self._image_width = value
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    @property
    def image_height(self):
        return self._image_height
    
    @image_height.setter
    def image_height(self, value):
        if value is None:
            raise ValueError("Image height cannot be None.")
        elif value <= 0:
            raise ValueError("Image height must be greater than 0.")
        
        self._image_height = value
        if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
            self._save_to_json()

    def _auto_calculate_fov(self):
        if self._focal_length is not None and self._sensor_width is not None:
            self._horizontal_field_of_view = 2 * math.atan(self._sensor_width / (2 * self._focal_length)) * constants.RAD_TO_DEG
        
        if self._focal_length is not None and self._sensor_height is not None:
            self._vertical_field_of_view = 2 * math.atan(self._sensor_height / (2 * self._focal_length)) * constants.RAD_TO_DEG

    def _auto_calculate_focal_length(self):
        if self._horizontal_field_of_view is not None and self._sensor_width is not None:
            self._focal_length = (self._sensor_width / 2) / math.tan((self._horizontal_field_of_view / 2) * constants.DEG_TO_RAD)
        
        if self._vertical_field_of_view is not None and self._sensor_height is not None:
            self._focal_length = (self._sensor_height / 2) / math.tan((self._vertical_field_of_view / 2) * constants.DEG_TO_RAD)

    def _auto_calculate_sensor_size(self):
        if self._focal_length is not None and self._horizontal_field_of_view is not None:
            self._sensor_width = 2 * self._focal_length * math.tan((self._horizontal_field_of_view / 2) * constants.DEG_TO_RAD)
        
        if self._focal_length is not None and self._vertical_field_of_view is not None:
            self._sensor_height = 2 * self._focal_length * math.tan((self._vertical_field_of_view / 2) * constants.DEG_TO_RAD)

    def _generate_unique_path(self):
        if not os.path.exists(constants.STANDARD_CAMERA_STORAGE_PATH):
            return constants.STANDARD_CAMERA_STORAGE_PATH

        base, ext = os.path.splitext(constants.STANDARD_CAMERA_STORAGE_PATH)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path

    def to_dict(self):
        dict_representation = {}
        for key in constants.PARAMETER_NAMES.keys():
            dict_representation[key] = getattr(self, f"_{key}")
        return dict_representation

    def _save_to_json(self):
        data = self.to_dict()
        with open(self._storage_path, 'w') as f:
            json.dump(data, f, indent=4)

    def _parameter_summary(self):
        data = self.to_dict()
        summary = []
        for key in data.keys():
            name = constants.PARAMETER_NAMES[key]
            value = data[key]
            unit = constants.PARAMETER_UNITS[key]
            summary.append(f"\t{name}: {value} {unit}")
        return "\n".join(summary)
    
    def __str__(self):
        return f"Camera\n{self._parameter_summary()}\n\nStored at: {self._storage_path}"
