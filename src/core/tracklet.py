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
            initial_detection.bbox3d.x,         
            initial_detection.bbox3d.y,  
            initial_detection.bbox3d.z,       
            initial_detection.bbox3d.theta,   
            initial_detection.bbox3d.length,
            initial_detection.bbox3d.width,
            initial_detection.bbox3d.height,
            self.initial_velocity * math.sin(initial_detection.bbox3d.theta),
            0,
            self.initial_velocity * math.cos(initial_detection.bbox3d.theta),
            0
        ])
        self.P = np.eye(11) * 0.1

    def update_prediction(self):
        self.x, self.P = self.kf.update_prediction(self.x, self.P)
    