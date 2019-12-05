import numpy as np
import uuid
from .kf import KalmanFilter

class Tracklet():

    def __init__(self, initial_detection, initial_frame):
        self.id = uuid.uuid4()
        self.creation_frame_idx = initial_frame
        self.kf = KalmanFilter()

        self.state = np.array([
            initial_detection.bbox3d.x,
            initial_detection.bbox3d.y,
            initial_detection.bbox3d.z,
            0,
            0,
            0,
            initial_detection.bbox3d.theta,
            0
        ])
        self.covariance = np.diag([1, 1, 1])

    def get_predicted_state(self):
        return self.kf.update_motion(self.state)

    def update(self):
        pass