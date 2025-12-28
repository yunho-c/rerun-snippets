import math
import time

import rerun as rr
import rerun.blueprint as rrb


def _orbit_blueprint(position: tuple[float, float, float]) -> rrb.Blueprint:
    return rrb.Blueprint(
        rrb.Spatial3DView(
            origin="/",
            eye_controls=rrb.EyeControls3D(
                kind=rrb.Eye3DKind.Orbital,
                position=position,
                look_target=(0.0, 0.0, 0.0),
                eye_up=(0.0, 1.0, 0.0),
                spin_speed=0.0,
            ),
        )
    )


def main() -> None:
    rr.init("orbit_camera_example", spawn=True)

    rr.log("scene/origin", rr.Points3D([[0.0, 0.0, 0.0]], colors=[255, 255, 255]))
    rr.log("scene/marker", rr.Points3D([[2.0, 0.0, 0.0]], colors=[255, 80, 80], radii=[0.15]))

    radius = 5.0
    height = 2.0
    orbit_speed = 0.6  # radians per second
    fps = 30.0

    rr.send_blueprint(_orbit_blueprint((radius, height, 0.0)))

    start = time.time()
    while True:
        angle = (time.time() - start) * orbit_speed
        position = (
            radius * math.cos(angle),
            height,
            radius * math.sin(angle),
        )

        rr.send_blueprint(_orbit_blueprint(position))
        time.sleep(1.0 / fps)


if __name__ == "__main__":
    main()
