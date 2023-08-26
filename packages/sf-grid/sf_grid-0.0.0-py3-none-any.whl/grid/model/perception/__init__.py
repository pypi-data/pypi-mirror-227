def _try_detection():
    try:
        import grid.model.perception.detection

    except ImportError as e:
        print("model.perception.detection registration failed", e)


def _try_depth():
    try:
        import grid.model.perception.depth

    except ImportError as e:
        print("model.perception.depth registration failed", e)


def _try_vqa():
    try:
        import grid.model.perception.vqa

    except ImportError as e:
        print("model.perception.vaq registration failed", e)


def _try_segmentation():
    try:
        import grid.model.perception.segmentation
    except ImportError as e:
        print("model.perception.segmentation registration failed", e)


def _try_register_perception():
    _try_detection()
    _try_depth()
    _try_vqa()
    _try_segmentation()


_try_register_perception()
