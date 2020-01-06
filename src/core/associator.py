import numpy as np


class TrackletAssociator():

    def __init__(self):
        self.matched_detections = []
        self.unmatched_detections = []
        self.unmatched_tracklets = []

        self.association_gate = 2 # 2m distance threshold

    def associate_detections(self, detections, current_tracklets):

        self.matched_detections = []
        self.unmatched_detections = []
        self.unmatched_tracklets = []

        for tracklet in current_tracklets:
            predicted_object_state = tracklet.x[:, -1]
            candidate_detection = None
            candidate_detection_distance = 1000
            candidate_detection_idx = None

            for i, detection in enumerate(detections):
                difference = np.array([predicted_object_state[0], predicted_object_state[2]]) - \
                    np.array([detection.bound_box3d.x,
                              detection.bound_box3d.z])
                detection_distance = np.linalg.norm(difference)

                if detection_distance < self.association_gate and detection_distance < candidate_detection_distance:
                    candidate_detection = detection
                    candidate_detection_distance = detection_distance
                    candidate_detection_idx = i

            if candidate_detection:
                detections.pop(candidate_detection_idx)
                self.matched_detections.append((tracklet, candidate_detection))
            else:
                self.unmatched_tracklets.append(tracklet)

        self.unmatched_detections = detections
