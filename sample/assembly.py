import numpy as np

from sample import constants
from sample.base_model import BaseModel
from sample.parameter import Parameter as P, PathParameter as PP
from sample.camera import Camera
from sample.reference_frame import ReferenceFrame

class Assembly(BaseModel):
    camera_path: P[str] = P('camera_path', None, can_be_none=False)
    reference_frames_paths: P[list[str]] = P('reference_frames_paths', None, can_be_none=True)

    def __init__(self, name=None):
        super().__init__(name=name)
        self.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS = constants.AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS
        self.AUTO_ASSIGN_PARENT_FRAME = constants.AUTO_ASSIGN_PARENT_FRAME

        self.set_initial('reference_frames_paths', [])

    @property
    def camera(self):
        if self.camera_path is None:
            return None

        camera = Camera()
        camera.storage_path = self.camera_path
        camera.load()
        return camera

    @camera.setter
    def camera(self, value):
        if value is None:
            self.camera_path = None
            return

        if not isinstance(value, Camera):
            raise ValueError("camera must be a Camera instance or None.")

        self.camera_path = value.storage_path

    @property
    def reference_frames(self):
        paths = self.reference_frames_paths or []
        frames = []
        for path in paths:
            frame = ReferenceFrame()
            frame.storage_path = path
            frame.load()
            frames.append(frame)
        return frames

    @reference_frames.setter
    def reference_frames(self, value):
        if value is None:
            self.reference_frames_paths = []
            return

        if not isinstance(value, list):
            raise ValueError("reference_frames must be a list of ReferenceFrame instances.")
        if not all(isinstance(frame, ReferenceFrame) for frame in value):
            raise ValueError("reference_frames must be a list of ReferenceFrame instances.")

        self.reference_frames_paths = [frame.storage_path for frame in value]

    def add_reference_frame(self, reference_frame):
        if not isinstance(reference_frame, ReferenceFrame):
            raise ValueError("reference_frame must be a ReferenceFrame instance.")

        frames = list(self.reference_frames)

        if self.AUTO_ASSIGN_PARENT_FRAME:
            reference_frame.parent_frame = frames[-1].name if len(frames) > 0 else None
        frames.append(reference_frame)
        self.reference_frames = frames

    def remove_reference_frame(self, name):
        frames = list(self.reference_frames)
        rf_index = next((i for i, rf in enumerate(frames) if rf.name == name), None)
        if rf_index is not None:
            if self.AUTO_ASSIGN_PARENT_FRAME and rf_index + 1 < len(frames):
                frames[rf_index + 1].parent_frame = frames[rf_index].parent_frame if rf_index > 0 else None
            frames.pop(rf_index)
            self.reference_frames = frames

    def get_screen_point(self, point):
        if self.camera is None:
            raise ValueError("Camera is not set for this assembly.")

        point_homogeneous = np.append(point, 1)
        for rf in self.reference_frames:
            point_homogeneous = rf.conversion_matrix_from_parent_4x4 @ point_homogeneous

        pixel_coords_homogeneous = self.camera.intrinsic_matrix_4x4 @ point_homogeneous
        pixel_x = pixel_coords_homogeneous[0] / pixel_coords_homogeneous[2]
        pixel_y = pixel_coords_homogeneous[1] / pixel_coords_homogeneous[2]

        return (pixel_x, pixel_y)