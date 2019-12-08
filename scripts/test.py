import os
import yaml

import src.core
from src.core.datasets.kitti.sequence.kitti_sequence import KittiSequence
from src.core.tracker import Tracker

def main():
    # Load configuration
    with open("config/test.yaml") as file:
        config = yaml.full_load(file)

    # Load detections
    detections_dir = os.path.join(src.core.data_dir(), "KITTI", "detections")
    dataset_dir = os.path.join("~/Kitti/tracking")
    sequence_detections = KittiSequence(
        detections_dir=detections_dir, dataset_dir=dataset_dir, seq_id=0)

    sequence_tracker = Tracker(sequence_detections)
    sequence_tracker.run()
    # for track in sequence_tracker.tracklet_history:
    #     print(track.x.shape)
    sequence_tracker.generate_results("/Users/johnwilles/Documents/dev/AER-1513/AER-1513-vehicle-tracking/results")

if __name__ == '__main__':
    main()
