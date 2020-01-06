import numpy as np


class KalmanFilter():

    def __init__(self):
        self.frame_rate = 0.1

        # Motion
        self.A = np.eye(11)
        self.A[0, 7] = self.frame_rate
        self.A[1, 8] = self.frame_rate
        self.A[2, 9] = self.frame_rate
        self.A[3, 10] = self.frame_rate

        self.Q = np.eye(11) * 0.01

        # Observation
        self.C = np.eye(7)
        self.C = np.block([self.C,  np.zeros((7, 4))])
        self.R = np.eye(7) * 0.01

    def update_prediction(self, x, P):
        x = self.A @ x
        P = self.A @ P @ np.transpose(self.A) + self.Q
        return x, P

    def update_correction(self, x, P, y):
        K = P @ np.transpose(self.C) @ np.linalg.inv(self.C @ P @ np.transpose(self.C) + self.R)
        P = (np.eye(11) - K @ self.C) @ P
        x = x + K @ (y - self.C @ x)
        return x, P
