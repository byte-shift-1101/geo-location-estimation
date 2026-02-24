import numpy as np
from numpy import typing as npt
import os

from sample import utils, constants
from sample.parameter import Parameter as P, PathParameter as PP

class ReferenceFrame:
    name: P[str] = P('name', None)
    position: P[npt.NDArray[np.float64]] = P('position', 'meters', strict_length=3)
    orientation: P[npt.NDArray[np.float64]] = P('orientation', 'degrees', min_value=0, max_value=360, strict_length=3)
    parentFrame: P['ReferenceFrame'] = P('parentFrame', None, canBeNone=True)

    storage_path: PP = PP('storage_path')

    def __init__(self, name=None):
        self.SKIP_HOOKS = False
        self.UPDATE_JSON_ON_ATTRIBUTE_SET = constants.UPDATE_JSON_ON_ATTRIBUTE_SET
        self.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS = constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS

        storage_filename = f"{name}_reference_frame.json" if name is not None else "reference_frame.json"
        self.storage_path = utils.get_unique_path(os.path.join(constants.STANDARD_REFERENCE_FRAME_FOLDER, storage_filename))

    def conversion_matrix_4x4(self):
        if self.parentFrame is None:
            return np.eye(4)

        orientation_rad = np.radians(self.orientation)

        Rx = np.array([[1, 0, 0],
                       [0, np.cos(orientation_rad[0]), -np.sin(orientation_rad[0])],
                       [0, np.sin(orientation_rad[0]), np.cos(orientation_rad[0])]])

        Ry = np.array([[np.cos(orientation_rad[1]), 0, np.sin(orientation_rad[1])],
                       [0, 1, 0],
                       [-np.sin(orientation_rad[1]), 0, np.cos(orientation_rad[1])]])

        Rz = np.array([[np.cos(orientation_rad[2]), -np.sin(orientation_rad[2]), 0],
                       [np.sin(orientation_rad[2]), np.cos(orientation_rad[2]), 0],
                       [0, 0, 1]])

        R = Rz @ Ry @ Rx

        C = np.eye(4)
        C[:3, :3] = R
        C[:3, 3] = self.position

        return C

    def to_dict(self):
        return {key: value for key, value in vars(ReferenceFrame).items() if isinstance(value, P) and not isinstance(value, PP)}
    
    def __str__(self):
        data = utils.to_str(self)
        data += f"\nStored at: {self.storage_path}"
        return data