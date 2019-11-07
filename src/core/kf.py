import numpy as np


class KalmanFilter():

    def __init__(self):
        self.frame_rate = 0.1

        self.A = np.eye(8)
        self.A[1, 4] = self.frame_rate
        self.A[2, 5] = self.frame_rate

    def prediction(self):
        pass

    def kalman_gain(self):
        pass

    def correction(self):
        pass

    def update_motion(self, state):
        return np.matmul(self.A, state)

    def observation(self):
        pass

