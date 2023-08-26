def _try_register_blip2():
    try:
        from .blip2 import BLIPv2
    except ImportError as e:
        print("register model.perception.blip2 failed:", e)


def _try_register_model_perception_caption():
    _try_register_blip2()


_try_register_model_perception_caption()
