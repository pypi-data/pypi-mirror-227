def _try_register_simenv():
    try:
        from grid.world.airgen_fire import AirGenEnv
        from grid.world.airgen_inspection import AirGenEnv

    except ImportError as e:
        tool_import_error = e

        print("World registration failed", e)


_try_register_simenv()
