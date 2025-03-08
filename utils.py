import math

class Utils:
    @staticmethod
    def calculateDistanceToTargetMeters(
        cameraHeightMeters: float,
        targetHeightMeters: float,
        cameraPitchRadians: float,
        targetPitchRadians: float
    ) -> float:
        return (targetHeightMeters - cameraHeightMeters) / math.tan(cameraPitchRadians + targetPitchRadians)
