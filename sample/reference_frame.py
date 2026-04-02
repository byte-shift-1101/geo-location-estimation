import numpy as np
from numpy import typing as npt

from sample import utils, constants
from sample.base_model import BaseModel
from sample.parameter import Parameter as P, PathParameter as PP

class ReferenceFrame(BaseModel):
    position: P[npt.NDArray[np.float64]] = P('position', 'meters', strict_length=3)
    orientation: P[npt.NDArray[np.float64]] = P('orientation', 'degrees', min_value=0, max_value=360, strict_length=3)
    parent_frame: P[str] = P('parent_frame', None, can_be_none=True)

    def __init__(self, name=None):
        super().__init__(name=name)
        self.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS = constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS

    @property
    def conversion_matrix_from_parent_4x4(self):
        if self.parent_frame is None:
            return np.eye(4)

        orientation_rad = np.radians(self.orientation)

        Rx = np.array([[1, 0, 0],
                       [0, np.cos(orientation_rad[0]), np.sin(orientation_rad[0])],
                       [0, -np.sin(orientation_rad[0]), np.cos(orientation_rad[0])]])

        Ry = np.array([[np.cos(orientation_rad[1]), 0, -np.sin(orientation_rad[1])],
                       [0, 1, 0],
                       [np.sin(orientation_rad[1]), 0, np.cos(orientation_rad[1])]])

        Rz = np.array([[np.cos(orientation_rad[2]), np.sin(orientation_rad[2]), 0],
                       [-np.sin(orientation_rad[2]), np.cos(orientation_rad[2]), 0],
                       [0, 0, 1]])

        R = Rx @ Ry @ Rz

        C = np.eye(4)
        C[:3, :3] = R
        C[:3, 3] = -self.position

        return C

    @property
    def conversion_matrix_to_parent_4x4(self):
        if self.parent_frame is None:
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