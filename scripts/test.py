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
    sequence_dir = os.path.join(src.core.data_dir(), "KITTI", 'detections', 'val', 'car')
    sequence_detections = KittiSequence(sequence_dir, 0)

    tracks = Tracker(sequence_detections)
    tracks.run()

if __name__ == '__main__':
    main()