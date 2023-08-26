def _try_register_model_perception_segmentation():
    try:
        from .clipseg import CLIPSeg
        from .gsam import GroundedSAM
    except ImportError as e:
        print("Registering model.perception.segmentation failed", e)


_try_register_model_perception_segmentation()
