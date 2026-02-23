import json
import math
import numpy as np
import os
from sample import parameter, constants, utils

np.set_printoptions(precision=4, suppress=True)

def hook_auto_save(instance):
    if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
        instance.save()

class Camera:
    focal_length = parameter.Parameter('focal_length', 'Focal Length', 'mm', min_value=0, hooks=[hook_auto_save])
    sensor_width = parameter.Parameter('sensor_width', 'Sensor Width', 'mm', min_value=0, hooks=[hook_auto_save])
    sensor_height = parameter.Parameter('sensor_height', 'Sensor Height', 'mm', min_value=0, hooks=[hook_auto_save])
    horizontal_field_of_view = parameter.Parameter('horizontal_field_of_view', 'Horizontal Field of View', 'degrees', min_value=0, max_value=180, hooks=[hook_auto_save])
    vertical_field_of_view = parameter.Parameter('vertical_field_of_view', 'Vertical Field of View', 'degrees', min_value=0, max_value=180, hooks=[hook_auto_save])
    image_width = parameter.Parameter('image_width', 'Image Width', 'pixels', min_value=0, hooks=[hook_auto_save])
    image_height = parameter.Parameter('image_height', 'Image Height', 'pixels', min_value=0, hooks=[hook_auto_save])

    storage_path = parameter.PathParameter('storage_path', 'Storage Path')

    def __init__(self):
        self.storage_path = utils.get_unique_path(constants.STANDARD_CAMERA_STORAGE_PATH)

    # @property
    # def focal_length(self):
    #     return self._focal_length

    # @focal_length.setter
    # def focal_length(self, value):
    #     if value is None:
    #         raise ValueError("Cannot set focal length to None.")
    #     elif value <= 0:
    #         raise ValueError("Focal length must be greater than 0.")
        
    #     self._focal_length = value
    #     if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
    #         self._auto_calculate_fov()
    #         self._auto_calculate_sensor_size()
    #     if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
    #         self._save_to_json()

    # @property
    # def sensor_width(self):
    #     return self._sensor_width

    # @sensor_width.setter
    # def sensor_width(self, value):
    #     if value is None:
    #         raise ValueError("Cannot set sensor width to None.")
    #     elif value <= 0:
    #         raise ValueError("Sensor width must be greater than 0.")

    #     self._sensor_width = value
    #     if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
    #         self._auto_calculate_fov()
    #         self._auto_calculate_focal_length()
    #     if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
    #         self._save_to_json()

    # @property
    # def sensor_height(self):
    #     return self._sensor_height

    # @sensor_height.setter
    # def sensor_height(self, value):
    #     if value is None:
    #         raise ValueError("Cannot set sensor height to None.")
    #     elif value <= 0:
    #         raise ValueError("Sensor height must be greater than 0.")
        
    #     self._sensor_height = value
    #     if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
    #         self._auto_calculate_fov()
    #         self._auto_calculate_focal_length()
    #     if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
    #         self._save_to_json()

    # @property
    # def horizontal_field_of_view(self):
    #     return self._horizontal_field_of_view

    # @horizontal_field_of_view.setter
    # def horizontal_field_of_view(self, value):
    #     if value is None:
    #         raise ValueError("Cannot set horizontal field of view to None.")
    #     elif (value < 0 or value > 180):
    #         raise ValueError("Horizontal field of view must be between 0 and 180 degrees.")
        
    #     self._horizontal_field_of_view = value
    #     if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
    #         self._auto_calculate_focal_length()
    #         self._auto_calculate_sensor_size()
    #     if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
    #         self._save_to_json()

    # @property
    # def vertical_field_of_view(self):
    #     return self._vertical_field_of_view

    # @vertical_field_of_view.setter
    # def vertical_field_of_view(self, value):
    #     if value is None:
    #         raise ValueError("Cannot set vertical field of view to None.")
    #     elif (value < 0 or value > 180):
    #         raise ValueError("Vertical field of view must be between 0 and 180 degrees.")
        
    #     self._vertical_field_of_view = value
    #     if constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS:
    #         self._auto_calculate_focal_length()
    #         self._auto_calculate_sensor_size()
    #     if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
    #         self._save_to_json()

    # @property
    # def storage_path(self):
    #     return self._storage_path

    # @storage_path.setter
    # def storage_path(self, value):
    #     if value is None:
    #         raise ValueError("Storage path cannot be None.")
    #     elif not os.path.exists(value):
    #         raise ValueError("File path does not exist.")
        
    #     self._storage_path = value
    #     if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
    #         self._save_to_json()

    # @property
    # def image_width(self):
    #     return self._image_width
    
    # @image_width.setter
    # def image_width(self, value):
    #     if value is None:
    #         raise ValueError("Image width cannot be None.")
    #     elif value <= 0:
    #         raise ValueError("Image width must be greater than 0.")
        
    #     self._image_width = value
    #     if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
    #         self._save_to_json()

    # @property
    # def image_height(self):
    #     return self._image_height
    
    # @image_height.setter
    # def image_height(self, value):
        # if value is None:
        #     raise ValueError("Image height cannot be None.")
        # elif value <= 0:
        #     raise ValueError("Image height must be greater than 0.")
        
        # self._image_height = value
        # if constants.UPDATE_JSON_ON_ATTRIBUTE_SET:
        #     self._save_to_json()

    # def _auto_calculate_fov(self):
    #     if self._focal_length is not None and self._sensor_width is not None:
    #         self._horizontal_field_of_view = 2 * math.atan(self._sensor_width / (2 * self._focal_length)) * constants.RAD_TO_DEG
        
    #     if self._focal_length is not None and self._sensor_height is not None:
    #         self._vertical_field_of_view = 2 * math.atan(self._sensor_height / (2 * self._focal_length)) * constants.RAD_TO_DEG

    # def _auto_calculate_focal_length(self):
    #     if self._horizontal_field_of_view is not None and self._sensor_width is not None:
    #         self._focal_length = (self._sensor_width / 2) / math.tan((self._horizontal_field_of_view / 2) * constants.DEG_TO_RAD)
        
    #     if self._vertical_field_of_view is not None and self._sensor_height is not None:
    #         self._focal_length = (self._sensor_height / 2) / math.tan((self._vertical_field_of_view / 2) * constants.DEG_TO_RAD)

    # def _auto_calculate_sensor_size(self):
    #     if self._focal_length is not None and self._horizontal_field_of_view is not None:
    #         self._sensor_width = 2 * self._focal_length * math.tan((self._horizontal_field_of_view / 2) * constants.DEG_TO_RAD)
        
    #     if self._focal_length is not None and self._vertical_field_of_view is not None:
    #         self._sensor_height = 2 * self._focal_length * math.tan((self._vertical_field_of_view / 2) * constants.DEG_TO_RAD)

    

    @property
    def intrinsic_matrix_3x4(self):
        if self.focal_length is None or self.sensor_width is None or self.sensor_height is None or self.image_width is None or self.image_height is None:
            raise ValueError("Cannot calculate intrinsic matrix. Missing parameters.")
        
        focal_length_x = -self.focal_length * self.image_width / self.sensor_width
        focal_length_y = -self.focal_length * self.image_height / self.sensor_height

        principal_point_x = self.image_width / 2
        principal_point_y = self.image_height / 2

        intrinsic_matrix = np.array([
            [focal_length_x, 0, principal_point_x, 0],
            [0, focal_length_y, principal_point_y, 0],
            [0, 0, 1, 0]
        ])
        return intrinsic_matrix

    def to_dict(self):
        return {key: value for key, value in vars(Camera).items() if isinstance(value, parameter.Parameter) and not isinstance(value, parameter.PathParameter)}

    def save(self):
        data = self.to_dict()
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        with open(self.storage_path, 'r') as f:
            data = json.load(f)

        for key, value in data.items():
            setattr(self, key, value)

    def __str__(self):
        data = self.to_dict()
        summary = ""
        for key, value in data.items():
            summary += f"\t{value.name}: {getattr(self, key)} {value.unit}\n"

        return f"Camera\n{summary}\nStored at: {self.storage_path}"
