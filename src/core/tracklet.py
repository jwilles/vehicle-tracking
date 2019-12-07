import numpy as np
import uuid
import math
from .kf import KalmanFilter


class Tracklet():

    def __init__(self, initial_detection, initial_frame):
        self.id = uuid.uuid4()
        self.creation_frame_idx = initial_frame
        self.kf = KalmanFilter()

        self.initial_velocity = 10

        self.x = np.array([
            initial_detection.bound_box3d.x,
            initial_detection.bound_box3d.y,
            initial_detection.bound_box3d.z,
            initial_detection.bound_box3d.theta,
            initial_detection.bound_box3d.x_dim,
            initial_detection.bound_box3d.y_dim,
            initial_detection.bound_box3d.z_dim,
            self.initial_velocity * math.sin(initial_detection.bound_box3d.theta),
            0,
            self.initial_velocity * math.cos(initial_detection.bound_box3d.theta),
            0
        ])
        self.P = np.eye(11) * 0.1

        self.x = self.x.reshape((11, 1))
        self.P = self.P.reshape((11, 11, 1))

    def last_frame(self):
        return self.creation_frame_idx + self.x.shape[1]
        
    def update_prediction(self):
        _x, _P = self.kf.update_prediction(self.x[:, -1], self.P[:, :, -1])
        #self.x, self.P = self.kf.update_prediction(self.x, self.P)

        _x = _x.reshape((11, 1))
        _P = _P.reshape((11, 11, 1))

        self.x = np.append(self.x, _x, axis=1)
        self.P = np.append(self.P, _P, axis=2)

    def update_correction(self, detection):
        self.x[:, -1], self.P[:, :, -1] = self.kf.update_correction(
            self.x[:, -1], self.P[:, :, -1], self._format_detection(detection))

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
