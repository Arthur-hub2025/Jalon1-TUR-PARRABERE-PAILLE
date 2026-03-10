import time, math
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

DT = 0.01

with ReachyMini(media_backend="no_media") as mini:
    t0 = time.time()
    while (t := time.time() - t0) < 3 / 0.2:
        pose = create_head_pose(y=10 * math.sin(2 * math.pi * 0.2 * t),
                                pitch=12 * math.sin(2 * math.pi * 0.8 * t),
                                mm=True, degrees=True)
        mini.set_target(head=pose)
        time.sleep(DT)

    t0 = time.time()
    while (t := time.time() - t0) < 3 / 0.2:
        a = 2 * math.pi * 0.2 * t
        pose = create_head_pose(x=10 * math.cos(a), y=10 * math.sin(a), z=5, mm=True)
        mini.set_target(head=pose)
        time.sleep(DT)

    mini.goto_target(head=create_head_pose(), antennas=[0, 0], duration=1.0)