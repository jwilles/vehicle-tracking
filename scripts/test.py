import os
import yaml

import src
from src.core.datasets.kitti.sequence.kitti_sequence import KittiSequence
from src.core.tracker import Tracker


def main():
    # Load configuration
    with open("config/test.yaml") as file:
        config = yaml.full_load(file)

    # Load detections
    dataset_dir = os.path.join(src.core.data_dir(), "KITTI")
    sequence_detections = KittiSequence(dataset_dir, 0, format="detections")

    tracks = Tracker(sequence_detections)
    tracks.run()

    # print(tracks.tracklet_history)


if __name__ == '__main__':
    main()
