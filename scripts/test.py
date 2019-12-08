import os
import yaml

import core
from core.datasets.kitti.sequence.kitti_sequence import KittiSequence
from core.tracker import Tracker


def main():
    # Load configuration
    with open("config/test.yaml") as file:
        config = yaml.full_load(file)

    # Load detections
    detections_dir = os.path.join(core.data_dir(), "KITTI", "detections")
    dataset_dir = os.path.join("~/Kitti/tracking")
    sequence_detections = KittiSequence(
        detections_dir=detections_dir, dataset_dir=dataset_dir, seq_id=0)

    tracks = Tracker(sequence_detections)
    tracks.run()

    # print(tracks.tracklet_history)
    breakpoint()


if __name__ == '__main__':
    main()
