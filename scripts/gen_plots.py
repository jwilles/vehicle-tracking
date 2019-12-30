import os
import yaml
import numpy as np
import matplotlib.pyplot as plt

import core
from core.datasets.kitti.sequence.kitti_sequence import KittiSequence
from core.utils.dir_utils import make_dir


def main():
    # Load configuration
    with open("config/default.yaml") as file:
        config = yaml.full_load(file)

    # Get directories
    detections_dir = os.path.join(core.data_dir(), "detections")
    dataset_dir = os.path.join("~/Kitti/tracking")
    results_dir = os.path.join(core.top_dir(), "results")
    plot_dir = os.path.join(results_dir, "plots")
    make_dir(plot_dir)
    ylabels = ["$x$ [m]", "$y$ [m]", "$x$ [m]", "$\theta$ [rad]", "$l$ [m]", "$h$ [m]", "$w$ [m]"]
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

            # Compute error and std dev
            error = x - gt_track
            error[3, :] = np.unwrap(error[3, :])
            t = np.arange(error.shape[1])
            var = np.transpose(P.diagonal())
            std_dev = np.sqrt(var)

            for i, ylabel in enumerate(ylabels):
                plot_file = os.path.join(plot_dir, str(i) + ".png")
                plt.plot(t, error[i, :], t, 3*std_dev[i, :], 'r--', t, -3*std_dev[i, :], 'r--')
                plt.savefig(plot_file)
                plt.close()


if __name__ == '__main__':
    main()
