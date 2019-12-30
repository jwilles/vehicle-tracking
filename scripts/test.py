import os
import yaml
import time

import core
from core.datasets.kitti.sequence.kitti_sequence import KittiSequence
from core.tracker import Tracker


def main():
    # Load configuration
    with open("config/default.yaml") as file:
        config = yaml.full_load(file)

    # Get directories
    detections_dir = os.path.join(core.data_dir(), "detections")
    dataset_dir = os.path.join("~/Kitti/tracking")
    results_dir = os.path.join(core.top_dir(), "results")
    duration = 0
    frames = 0
    for split in config["splits"]:
        for class_ in config["classes"]:
            for seq_id in range(config["num_sequences"]):
                print("Processing: {}".format(seq_id))

                # Load detections
                sequence_detections = KittiSequence(
                    detections_dir=detections_dir, dataset_dir=dataset_dir, seq_id=seq_id, split=split, class_=class_)

                start = time.time()
                sequence_tracker = Tracker(sequence_detections)
                sequence_tracker.run()
                duration = duration + (time.time() - start)
                frames = frames + len(sequence_detections)

                # Output text predictions
                if config["output_text"]:
                    text_dir = os.path.join(results_dir, "text", split, class_)

                    # Make file if doesn't exists
                    if not os.path.exists(text_dir):
                        os.makedirs(text_dir)

                    text_file = os.path.join(text_dir, str(seq_id).zfill(4) + ".txt")

                    sequence_tracker.generate_text_output(output_file=text_file)

                # Output bounding box visualization
                if config["output_vis"]:
                    vis_path = os.path.join(results_dir, "vis", split, class_,
                                            str(seq_id).zfill(4))
                    sequence_tracker.generate_visualization(output_path=vis_path)

                # Output error and covariance plots
                if config["output_tracks"]:
                    track_dir = os.path.join(results_dir, "tracks", split,
                                             class_, str(seq_id).zfill(4))

                    # Make file if doesn't exists
                    if not os.path.exists(track_dir):
                        os.makedirs(track_dir)

                    sequence_tracker.generate_track_output(output_path=track_dir)

    print("FPS {}".format(frames/duration))


if __name__ == '__main__':
    main()
