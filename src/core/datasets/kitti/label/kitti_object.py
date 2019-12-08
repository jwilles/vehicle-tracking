from src.core.utils.object.object import Object
from src.core.utils.object.bound_box2d import BoundBox2D
from src.core.utils.object.bound_box3d import BoundBox3D


class KittiObject(Object):
    """ Kitti 3D Object Label """

    def __init__(self, line):
        """
        Converts a line from the KITTI labels text file into the KittiObject format.
        See https://github.com/xinshuoweng/AB3DMOT/blob/master/README.md for more details
        Args:
            line [string]: Line in the KITTI object detection text file
        """
        label = line.strip().split(',')
        self.frame = int(label[0])
        class_id = int(label[1])

        # 2D bounding box in pixel coordinates [px]
        bound_box2d = BoundBox2D(u1=float(label[2]), v1=float(label[3]),
                                 u2=float(label[4]), v2=float(label[5]))

        # 3D bounding box in camera coordinates [m,rad]
        bound_box3d = BoundBox3D(x=float(label[10]),
                                 y=float(label[11]),
                                 z=float(label[12]),
                                 z_dim=float(label[9]),
                                 x_dim=float(label[8]),
                                 y_dim=float(label[7]),
                                 theta=float(label[13]))

        self.alpha = float(label[14])
        score = float(label[6]) 
        track_id = None
        
        # Parent class initialization
        super(KittiObject, self).__init__(class_id, bound_box2d, bound_box3d, track_id, score)
