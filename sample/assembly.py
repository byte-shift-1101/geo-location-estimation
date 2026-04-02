import os
import numpy as np

from sample import constants, utils
from sample.base_model import BaseModel
from sample.parameter import Parameter as P, PathParameter as PP
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame

class Assembly(BaseModel):
    name: P[str] = P('name', None)
    camera: P[Camera] = P('camera', None)
    referenceFrames: P[list[ReferenceFrame]] = P('referenceFrames', [])

    storage_path: PP = PP('storage_path')

    def __init__(self, name=None):
        super().__init__()
        self.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS = constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS
        self.AUTO_ASSIGN_PARENT_FRAME = constants.AUTO_ASSIGN_PARENT_FRAME

        storage_filename = f"{name}_assembly.json" if name is not None else "assembly.json"
        self.storage_path = utils.get_unique_path(os.path.join(constants.STANDARD_ASSEMBLY_FOLDER, storage_filename))
        if name is not None:
            self.name = name

    def add_reference_frame(self, reference_frame):
        if self.referenceFrames is None:
            self.referenceFrames = []

        if self.AUTO_ASSIGN_PARENT_FRAME:
            reference_frame.parentFrame = self.referenceFrames[-1].name if len(self.referenceFrames) > 0 else None
        self.referenceFrames.append(reference_frame)

    def remove_reference_frame(self, name):
        if self.referenceFrames is not None:
            rf_index = next((i for i, rf in enumerate(self.referenceFrames) if rf.name == name), None)
            if rf_index is not None:
                if self.AUTO_ASSIGN_PARENT_FRAME and rf_index + 1 < len(self.referenceFrames):
                    self.referenceFrames[rf_index + 1].parentFrame = self.referenceFrames[rf_index].parentFrame if rf_index > 0 else None
                self.referenceFrames.pop(rf_index)

    def get_screen_point(self, point):
        point_homogeneous = np.append(point, 1)
        for rf in self.referenceFrames:
            point_homogeneous = rf.conversion_matrix_from_parent_4x4 @ point_homogeneous

        intrinsic_matrix = self.camera.intrinsic_matrix_4x4
        pixel_coords_homogeneous = intrinsic_matrix @ point_homogeneous
        pixel_x = pixel_coords_homogeneous[0] / pixel_coords_homogeneous[2]
        pixel_y = pixel_coords_homogeneous[1] / pixel_coords_homogeneous[2]

        return (pixel_x, pixel_y)