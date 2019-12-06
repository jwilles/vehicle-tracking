import numpy as np

class KalmanFilter():

    def __init__(self):
        self.frame_rate = 0.1

        #self.x = None
        #self.P = np.eye(11) * 0.1

        self.A = np.eye(11)
        self.A[0, 7] = self.frame_rate
        self.A[1, 8] = self.frame_rate
        self.A[2, 9] = self.frame_rate
        self.A[3, 10] = self.frame_rate

        self.Q = np.eye(11) * 0.1

    # def update(self, state, covariance, detections):
    #     self.x = state
    #     self.P = covariance

    #     self.update_prediction()
    #     self.update_kalman_gain()
    #     self.update_correction()

    #     return self.x, self.P

    def update_prediction(self, x, P):
        #x = np.matlmul(self.A, x)
        x = self.A @ x
        P = self.A @ P @ np.transpose(self.A) + self.Q
        return x, P

    def update_kalman_gain(self):
        pass

    def update_correction(self):
        pass

    def update_motion(self, state):
        return np.matmul(self.A, state)

    def observation(self):
        pass

