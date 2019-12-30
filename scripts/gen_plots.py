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
    ylabels = [r"$x$ [m]", r"$y$ [m]", r"$z$ [m]",
               r"$\theta$ [rad]", r"$l$ [m]", r"$h$ [m]", r"$w$ [m]"]
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
            track_id = "38882006386010313624536118754.npy"
            x_file = os.path.join(track_dir, "x", track_id)
            P_file = os.path.join(track_dir, "P", track_id)
            x = np.load(x_file)
            x = x[:7, :]
            P = np.load(P_file)
            P = P[:7, :7, :]

            # Compute error and std dev
            t = np.arange(x.shape[1])
            error = x - gt_track
            error[3, :] = np.unwrap(error[3, :])
            var = np.transpose(P.diagonal())
            std_dev = np.sqrt(var)

            fig = plt.figure(figsize=(12, 7))
            plot_file = os.path.join(plot_dir, "error.png")
            for i, ylabel in enumerate(ylabels):
                ax = fig.add_subplot(241 + i)
                line1 = ax.plot(t, error[i, :])
                line2 = ax.plot(t, 3*std_dev[i, :], 'r--',
                                t, -3*std_dev[i, :], 'r--')[0]
                ax.set_xlabel('Frame')
                ax.set_ylabel(ylabel)

            fig.legend([line1, line2],
                       labels=['Error', 'Uncertainty Envelope'],
                       bbox_to_anchor=(0.97, 0.28),
                       loc="center right")
            plt.tight_layout()
            plt.savefig(plot_file)
            plt.close()


if __name__ == '__main__':
    main()
