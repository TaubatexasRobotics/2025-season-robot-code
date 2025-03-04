import photonlibpy

class AprilTagCamera:
    def __init__(self, camera: str) -> None:
        self.camera = photonlibpy.PhotonCamera(camera)

    def getBestTarget(self) -> (photonlibpy.PhotonTrackedTarget | None):
        result = self.camera.getLatestResult()
        if result.hasTargets():
            target = result.getBestTarget()
            return target
        return None