def _try_register_git():
    try:
        from .msgit import GITBase
    except ImportError as e:
        print("Registering model.perception.vqa.msgit failed", e)


def _try_register_llava():
    try:
        from .gllava import GLLaVA
    except ImportError as e:
        print("register model.perception.vqa.llava failed:", e)


def _try_register_model_perception_vqa():
    _try_register_git()
    _try_register_llava()


_try_register_model_perception_vqa()
