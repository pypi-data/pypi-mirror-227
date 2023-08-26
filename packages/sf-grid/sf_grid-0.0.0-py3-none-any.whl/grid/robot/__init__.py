def _try_register_robot():
    try:
        from grid.robot.airgen_drone import AirGenDrone
        from grid.robot.airgen_collector import AirGenCollector
        from grid.robot.airgendrone_classic import AirGenDrone

    except ImportError as e:
        print("Robot registration failed", e)


_try_register_robot()
