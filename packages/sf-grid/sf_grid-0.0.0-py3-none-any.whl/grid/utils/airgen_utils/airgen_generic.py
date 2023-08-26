from typing import List
import os
from platform import uname
import airgen


def vector3d2list(vector3d: airgen.Vector3r) -> List[float]:
    return [vector3d.x_val, vector3d.y_val, vector3d.z_val]


def airgenClient() -> airgen.MultirotorClient:
    client = None
    if (
        "linux" in uname().system.lower() and "microsoft" in uname().release.lower()
    ):  # In WSL2
        if "WSL_HOST_IP" in os.environ:
            HOST = os.environ["WSL_HOST_IP"]
            client = airgen.MultirotorClient(ip=HOST)
    else:
        client = airgen.MultirotorClient()
    return client
