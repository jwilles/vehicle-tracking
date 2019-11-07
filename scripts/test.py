import os
import yaml

import src
#import src.core.evaluation.results
from src.core.datasets.kitti.kitti_detections import KittiDetections
from src.core.tracker import Tracker


def main():
    # Load configuration
    with open("config/test.yaml") as file:
        config = yaml.full_load(file)

    # Load detections
    dataset_dir = os.path.join(src.core.data_dir(), "KITTI")
    kitti_detections = {split: {class_: KittiDetections(dataset_dir=dataset_dir, split=split, class_=class_)
                                for class_ in config["classes"]}
                        for split in config["splits"]}

    # Load ground truth
    #gt_tracklets =  # TO DO

    tracks = Tracker(kitti_detections[split][class_])
    tracks.run()

    # # Initialize trackers
    # trackers = {split: {class_: Tracker(kitti_detections[split][class_])
    #                     for class_ in config["classes"]}
    #             for split in config["splits"]}
    #
    # # Run the trackers
    # tracklets = {split: {class_: trackers[split][class_].run()
    #                      for class_ in config["classes"]}
    #              for split in config["splits"]}
    #
    # # Generate and save the results
    # generate_results(tracklets, gt_tracklets)

if __name__ == '__main__':
    main()