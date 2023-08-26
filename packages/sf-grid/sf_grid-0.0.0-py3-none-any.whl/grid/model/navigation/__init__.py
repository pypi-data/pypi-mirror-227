def _try_register_navigate():
    try:
        from .visualservoing import VisualServoing
        from .objectinspection import ObjectInspect
    except ImportError as e:
        print("register model.nav failed", e)


_try_register_navigate()
