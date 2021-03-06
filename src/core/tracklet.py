import numpy as np
import uuid
import math
from .kf import KalmanFilter
from core.utils.object.object import Object
from core.utils.object.bound_box2d import BoundBox2D
from core.utils.object.bound_box3d import BoundBox3D


class Tracklet():

    def __init__(self, initial_detection, initial_frame):
        self.id = uuid.uuid4()
        self.creation_frame_idx = initial_frame
        self.kf = KalmanFilter()
        self.class_id = initial_detection.class_id
        self.initial_velocity = 10
        self.memory = 0
        self.scores = np.array([initial_detection.score])

        self.x = np.array([
            initial_detection.bound_box3d.x,
            initial_detection.bound_box3d.y,
            initial_detection.bound_box3d.z,
            initial_detection.bound_box3d.theta,
            initial_detection.bound_box3d.x_dim,
            initial_detection.bound_box3d.y_dim,
            initial_detection.bound_box3d.z_dim,
            self.initial_velocity * math.cos(initial_detection.bound_box3d.theta),
            0,
            self.initial_velocity * math.sin(initial_detection.bound_box3d.theta),
            0
        ])
        self.P = np.eye(11) * 0.1

        self.x = self.x.reshape((11, 1))
        self.P = self.P.reshape((11, 11, 1))

    def __len__(self):
        return self.x.shape[1]

    def exists_for_frame(self, frame_idx):
        if self.creation_frame_idx <= frame_idx and frame_idx <= self._last_frame():
            return True
        return False

    def has_minimum_length(self):
        state_dim = self.x.shape
        if state_dim[1] > 30:
            return True
        return False

    def get_track_frame(self, frame_idx):
        state_idx = frame_idx - (self.creation_frame_idx + 1)
        state = self.x[:, state_idx]
        bbox2d = BoundBox2D(0, 0, 0, 0)
        bbox3d = BoundBox3D(
            state[0],
            state[1],
            state[2],
            state[4],
            state[5],
            state[6],
            state[3]
        )
        return Object(self.class_id, bbox2d, bbox3d, self.id, np.mean(self.scores))

    def update_prediction(self):
        _x, _P = self.kf.update_prediction(self.x[:, -1], self.P[:, :, -1])
        _x[3] = np.unwrap(np.array([_x[3]]))
        _x = _x.reshape((11, 1))
        _P = _P.reshape((11, 11, 1))

        self.x = np.append(self.x, _x, axis=1)
        self.P = np.append(self.P, _P, axis=2)

    def update_correction(self, detection):
        self.x[:, -1], self.P[:, :, -1] = self.kf.update_correction(
            self.x[:, -1], self.P[:, :, -1], self._format_detection(detection))
        self.x[3, -1] = np.unwrap(np.array([self.x[3, -1]]))
        self.scores = np.append(self.scores, detection.score)

    def _last_frame(self):
        return self.creation_frame_idx + self.x.shape[1]

    def _format_detection(self, detection):
        formatted_detction = np.array([
            detection.bound_box3d.x,
            detection.bound_box3d.y,
            detection.bound_box3d.z,
            detection.bound_box3d.theta,
            detection.bound_box3d.x_dim,
            detection.bound_box3d.y_dim,
            detection.bound_box3d.z_dim,
        ])
        return formatted_detction
