from base_object import BaseObject
from core.utils.object.bound_box2d import BoundBox2D
from core.utils.object.bound_box3d import BoundBox3D

from core.datasets.kitti.kitti_object import KittiObject


def objects_to_text(objects):
    """
    Outputs list of objects as text lines
    Args:
        objects [list[Object]]: List of objects
    Returns
        lines [list[string]]: List of text lines
    """

    # Convert objects to KITTI labels text format
    kitti_objects = [KittiObject(sample_id=sample_id, object_=object_) for object_ in objects]
    lines = [kitti_obj.get_line() for kitti_obj in kitti_objects]
    return lines
