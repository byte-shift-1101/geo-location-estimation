import json
import math
import numpy as np

from sample import hooks, constants, utils
from sample.parameter import Parameter as P, PathParameter as PP

np.set_printoptions(precision=4, suppress=True)

class Camera:
    focal_length: P[float] = P('focal_length', 'millimeters', min_value=0, hooks=[
        hooks.hook_auto_calculate_fov,
        hooks.hook_auto_calculate_sensor_size,
        hooks.hook_auto_save
    ])
    sensor_width: P[float] = P('sensor_width', 'millimeters', min_value=0, hooks=[
        hooks.hook_auto_calculate_fov,
        hooks.hook_auto_calculate_focal_length,
        hooks.hook_auto_save
    ])
    sensor_height: P[float] = P('sensor_height', 'millimeters', min_value=0, hooks=[
        hooks.hook_auto_calculate_fov,
        hooks.hook_auto_calculate_focal_length,
        hooks.hook_auto_save
    ])
    horizontal_field_of_view: P[float] = P('horizontal_field_of_view', 'degrees', min_value=0, max_value=180, hooks=[
        hooks.hook_auto_calculate_focal_length,
        hooks.hook_auto_calculate_sensor_size,
        hooks.hook_auto_save
    ])
    vertical_field_of_view: P[float] = P('vertical_field_of_view', 'degrees', min_value=0, max_value=180, hooks=[
        hooks.hook_auto_calculate_focal_length,
        hooks.hook_auto_calculate_sensor_size,
        hooks.hook_auto_save
    ])
    image_width: P[int] = P('image_width', 'pixels', min_value=0)
    image_height: P[int] = P('image_height', 'pixels', min_value=0)

    storage_path: PP = PP('storage_path')

    def __init__(self):
        self.SKIP_HOOKS = False
        self.UPDATE_JSON_ON_ATTRIBUTE_SET = constants.UPDATE_JSON_ON_ATTRIBUTE_SET
        self.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS = constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS

        self.storage_path = utils.get_unique_path(constants.STANDARD_CAMERA_STORAGE_PATH)

    def calculate_fov(self):
        if utils.params_exist(self, ['focal_length', 'sensor_width']):
            self.horizontal_field_of_view = 2 * math.atan(self.sensor_width / (2 * self.focal_length)) * constants.RAD_TO_DEG
        
        if utils.params_exist(self, ['focal_length', 'sensor_height']):
            self.vertical_field_of_view = 2 * math.atan(self.sensor_height / (2 * self.focal_length)) * constants.RAD_TO_DEG

    def calculate_focal_length(self):
        if utils.params_exist(self, ['horizontal_field_of_view', 'sensor_width']):
            self.focal_length = (self.sensor_width / 2) / math.tan((self.horizontal_field_of_view / 2) * constants.DEG_TO_RAD)
        
        if utils.params_exist(self, ['vertical_field_of_view', 'sensor_height']):
            self.focal_length = (self.sensor_height / 2) / math.tan((self.vertical_field_of_view / 2) * constants.DEG_TO_RAD)

    def calculate_sensor_size(self):
        if utils.params_exist(self, ['focal_length', 'horizontal_field_of_view']):
            self.sensor_width = 2 * self.focal_length * math.tan((self.horizontal_field_of_view / 2) * constants.DEG_TO_RAD)
        
        if utils.params_exist(self, ['focal_length', 'vertical_field_of_view']):
            self.sensor_height = 2 * self.focal_length * math.tan((self.vertical_field_of_view / 2) * constants.DEG_TO_RAD)

    @property
    def intrinsic_matrix_3x4(self):
        if not utils.params_exist(self, ['focal_length', 'sensor_width', 'sensor_height', 'image_width', 'image_height']):
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

    @property
    def intrinsic_matrix_4x4(self):
        intrinsic_3x4 = self.intrinsic_matrix_3x4
        intrinsic_4x4 = np.vstack([intrinsic_3x4, [0, 0, 0, 1]])
        return intrinsic_4x4

    def to_dict(self):
        return {key: value for key, value in vars(Camera).items() if isinstance(value, P) and not isinstance(value, PP)}

    def __str__(self):
        data = utils.to_str(self)
        data += f"\nStored at: {self.storage_path}"
        return data