import numpy as np
from .kf import KalmanFilter
from .tracklet import Tracklet

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

            print('-'*40)
            print(associations)

            self.destroy_unmatched_tracklets(associations['unmatched_tracklets'])
            self.update_matched_tracklets(associations['matched_detections'])
            self.create_tracklets_for_unmatched_detections(associations['unmatched_detections'])

            print(self.current_tracklets)

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
            candidate_detection_idx = None

            for i, detection in enumerate(detections):
                difference = np.array([predicted_object_state[0], predicted_object_state[2]]) - np.array([detection.bbox3d.x, detection.bbox3d.z])
                detection_distance = np.linalg.norm(difference)

                if detection_distance < association_gate and detection_distance < candidate_detection_distance:
                    candidate_detection = detection
                    candidate_detection_distance = detection_distance
                    candidate_detection_idx = i

            if candidate_detection:
                detections.pop(candidate_detection_idx)
                associations['matched_detections'].append((tracklet, candidate_detection))
            else:
                associations['unmatched_tracklets'].append(tracklet)

        associations['unmatched_detections'] = detections

        return associations

    def update_matched_tracklets(self, matched_detections):
        pass

    def destroy_unmatched_tracklets(self, unmatched_tracklets):
        for tracklet in unmatched_tracklets:
            self.tracklet_history.append(tracklet)
            self.current_tracklets = [x for x in self.current_tracklets if x.id != tracklet.id]

    def create_tracklets_for_unmatched_detections(self, unmatched_detections):
        for detection in unmatched_detections:
            self.current_tracklets.append(Tracklet(detection, self.current_frame_idx))






