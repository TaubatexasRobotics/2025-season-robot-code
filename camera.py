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