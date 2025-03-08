import photonlibpy
from typing import Optional

from photonlibpy.targeting.photonTrackedTarget import PhotonTrackedTarget

class AprilTagCamera:
    def __init__(self, camera: str) -> None:
        self.camera = photonlibpy.PhotonCamera(camera)

    def getBestTarget(self) -> Optional[PhotonTrackedTarget]:
        result = self.camera.getLatestResult()
        if result.hasTargets():
            target = result.getBestTarget()
            return target
        return None

    def getYaw(self, tag) -> float:
        target_yaw = 0
        target_range = 0
        results = self.camera.getAllUnreadResults()
        if len(results) > 0:
            result = results[-1]
            for target in result.getTargets():
                if target.getFiducialId() == tag:
                    return target.getYaw()
        return -1
