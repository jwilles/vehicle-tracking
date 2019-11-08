import numpy as np


class KalmanFilter():

    def __init__(self):
        self.frame_rate = 0.1

        self.x = None
        self.P = None

        self.A = np.eye(8)
        self.A[1, 4] = self.frame_rate
        self.A[2, 5] = self.frame_rate


    def update(self, state, covariance, detections):
        self.x = state
        self.P = covariance

        self.update_prediction()
        self.update_kalman_gain()
        self.update_correction()

        return self.x, self.P

    def update_prediction(self):
        self.x = np.matlmul(self.A, self.x)
        self.P = self.A @ covariance @ np.transpose(self.A)

    def update_kalman_gain(self):
        pass

    def update_correction(self):
        pass

    def update_motion(self, state):
        return np.matmul(self.A, state)

    def observation(self):
        pass

