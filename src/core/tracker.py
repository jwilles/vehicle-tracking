import numpy as np
import uuid
from .kf import KalmanFilter

class Tracker():
    """ Global Tracking Manager """

    def __init__(self, kitti_frame_detections):
        """
        Initializes the Global Track Manager

        :param kitti_detections: kitti detections object
        """
        self.frame_detections = kitti_frame_detections
        self.num_frames = kitti_frame_detections.num_frames
        self.tracklet_history = []
        self.current_tracklets = []
        self.current_frame_idx = 0

    def run(self):
        """
        Execute Tracking for each Kitti Sequence
        :return:
        """

        for i in range(1):#range(self.num_frames + 1):
            self.current_frame_idx = i
            current_object_detections = self.frame_detections[self.current_frame_idx]

            matched_detections, unmatched_detections, \
                unmatched_tracklets = self.associate_detections(current_object_detections)

            self.update_matched_tracklets(matched_detections)
            self.destroy_unmatched_tracklets(unmatched_tracklets)
            self.create_tracklets_for_unmatched_detections(unmatched_detections)

        print(self.current_tracklets[0].state)


            #object_predictions = self.get_predictions()

    def associate_detections(self, detections):
        if not self.current_tracklets:
            return [], detections, []

    def update_matched_tracklets(self, matched_detections):
        pass

    def destroy_unmatched_tracklets(self, unmatched_tracklets):
        pass

    def create_tracklets_for_unmatched_detections(self, unmatched_detections):
        for detection in unmatched_detections:
            self.current_tracklets.append(Tracklet(detection, self.current_frame_idx))

class Tracklet():

    def __init__(self, detection, initial_frame):
        self.creation_frame_idx = initial_frame
        self.state = detection
        self.covariance = np.diag([1, 1, 1])
        self.kf = KalmanFilter()
        self.id = uuid.uuid4()

    def get_predicted_state(self):
        pass

    def update(self):
        pass



