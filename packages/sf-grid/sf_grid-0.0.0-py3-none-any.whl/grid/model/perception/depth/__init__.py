def _try_register_model_perception_depth():
    try:
        from .midas import MIDAS
    except ImportError as e:
        print("register model.perception.depth failed:", e)


_try_register_model_perception_depth()
