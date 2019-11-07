from .kitti_label import KittiLabel
from ..boundbox.kitti_bbox2d import KittiBBox2D
from ..boundbox.kitti_bbox3d import KittiBBox3D


class KittiObject(KittiLabel):
    """ Kitti 3D Object Label """

    def __init__(self, line):
        """
        Converts a line from the KITTI labels text file into the KittiObject format.
        See https://github.com/xinshuoweng/AB3DMOT/blob/master/README.md for more details
        Args:
            line [string]: Line in the KITTI object detection text file
        """
        label = line.strip().split(',')
        params = {}
        params["frame"] = int(label[0])
        params["type"] = int(label[1])

        # 2D bounding box in pixel coordinates [px]
        params["bbox2d"] = KittiBBox2D(x1=float(label[2]), y1=float(label[3]),
                                       x2=float(label[4]), y2=float(label[5]))

        # 3D bounding box in camera coordinates [m,rad]
        params["bbox3d"] = KittiBBox3D(x=float(label[10]),
                                       y=float(label[11]),
                                       z=float(label[12]),
                                       length=float(label[9]),
                                       width=float(label[8]),
                                       height=float(label[7]),
                                       theta=float(label[13]))

        params["alpha"] = float(label[14])
        params["score"] = float(label[6])
        super(KittiObject, self).__init__(params)
