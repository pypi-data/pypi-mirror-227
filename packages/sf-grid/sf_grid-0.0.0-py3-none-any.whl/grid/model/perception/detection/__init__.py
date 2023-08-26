def _try_gdino():
    try:
        from .detr import DeticDETR
        from .gdino import GroundingDINO
    except ImportError as e:
        print("register model.perception.detection.gdino failed", e)


def _try_yolo():
    try:
        from .yolo import Yolo
    except ImportError as e:
        print("register model.perception.detection.yolo failed", e)


def _try_detr():
    try:
        from .detr import DeticDETR
    except ImportError as e:
        print("register model.perception.detection.detr failed", e)


def _try_register_model_perception_detection():
    _try_gdino()
    _try_yolo()
    _try_detr()


_try_register_model_perception_detection()
