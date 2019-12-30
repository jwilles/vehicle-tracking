import os
import yaml
import numpy as np

import core
from core.datasets.kitti.sequence.kitti_sequence import KittiSequence


def main():
    # Load configuration
    with open("config/default.yaml") as file:
        config = yaml.full_load(file)

    # Get directories
    detections_dir = os.path.join(core.data_dir(), "detections")
    dataset_dir = os.path.join("~/Kitti/tracking")
    results_dir = os.path.join(core.top_dir(), "results")
    ylabels = ["X [m]", "Y [m", ]
    for split in config["splits"]:
        for class_ in config["classes"]:
            seq_id = 15
            gt_track_id = 2
            # Load ground truth
            sequence = KittiSequence(
                detections_dir=detections_dir, dataset_dir=dataset_dir, seq_id=seq_id, split=split, class_=class_)
            gt_track = sequence.get_track(gt_track_id)
            gt_track = gt_track[:, 2:]

            # Load track
            track_dir = os.path.join(results_dir, "tracks", split, class_, str(seq_id).zfill(4))
            track_id = "34365336289527131679102792918.npy"
            x_file = os.path.join(track_dir, "x", track_id)
            P_file = os.path.join(track_dir, "P", track_id)
            x = np.load(x_file)
            x = x[:7, :]
            P = np.load(P_file)
            P = P[:7, :7, :]

            for i, ylabel in enumerate(ylabels):


if __name__ == '__main__':
    main()
