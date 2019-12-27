import os
import yaml

import src.core
from src.core.datasets.kitti.sequence.kitti_sequence import KittiSequence
from src.core.tracker import Tracker


def main():
    # Load configuration
    with open("config/default.yaml") as file:
        config = yaml.full_load(file)

    # Get directories
    detections_dir = os.path.join(core.data_dir(), "detections")
    dataset_dir = os.path.join("~/Kitti/tracking")
    results_dir = os.path.join(core.top_dir(), "results")

    for split in config["splits"]:
        for class_ in config["classes"]:
            for seq_id in range(config["num_sequences"]):

                # Load detections
                sequence_detections = KittiSequence(
                    detections_dir=detections_dir, dataset_dir=dataset_dir, seq_id=seq_id)

                sequence_tracker = Tracker(sequence_detections)
                sequence_tracker.run()

                # Output text predictions
                if config["output_text"]:
                    text_file = os.path.join(results_dir, "text", split, class_,
                                             str(seq_id).zfill(4) + ".txt")
                    sequence_tracker.generate_text_output(output_file=text_file)

                # Output bounding box visualization
                if infer_config["output_vis"]:
                    vis_path = os.path.join(results_dir, "vis", split, class_,
                                            str(seq_id).zfill(4))
                    sequence_tracker.generate_visualization(output_path=vis_path)


if __name__ == '__main__':
    main()
