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

        for i in range(2): #range(self.num_frames + 1):
            self.current_frame_idx = i
            current_object_detections = self.frame_detections[self.current_frame_idx]

            associations = self.associate_detections(current_object_detections)

            print(associations)

            self.update_matched_tracklets(associations['matched_detections'])
            self.destroy_unmatched_tracklets(associations['unmatched_tracklets'])
            self.create_tracklets_for_unmatched_detections(associations['unmatched_detections'])

    def associate_detections(self, detections):

        associations = {
            'matched_detections': [],
            'unmatched_detections': [],
            'unmatched_tracklets': []
        }
        association_gate = 2 # 2m distance threshold

        for tracklet in self.current_tracklets:
            predicted_object_state = tracklet.get_predicted_state()
            candidate_detection = None
            candidate_detection_distance = 1000

            for detection in detections:
                difference = np.array([predicted_object_state[0], predicted_object_state[1]]) - np.array([detection.bbox3d.x, detection.bbox3d.y])
                detection_distance = np.linalg.norm(difference)

                if detection_distance < association_gate and detection_distance < candidate_detection_distance:
                    candidate_detection = detection

            if candidate_detection:
                detections.remove(candidate_detection)
                associations['matched_detections'].append((tracklet, candidate_detection))
            else:
                associations['unmatched_tracklets'].append(tracklet)

        associations['unmatched_detections'] = detections

        return associations

    def update_matched_tracklets(self, matched_detections):
        pass

    def destroy_unmatched_tracklets(self, unmatched_tracklets):
        pass

    def create_tracklets_for_unmatched_detections(self, unmatched_detections):
        for detection in unmatched_detections:
            self.current_tracklets.append(Tracklet(detection, self.current_frame_idx))


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



