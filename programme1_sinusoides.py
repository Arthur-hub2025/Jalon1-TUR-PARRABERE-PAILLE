import time, math
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

DT = 0.01
DUREE = 3 / 0.3
AMPLITUDES = {"roll": 15, "pitch": 15, "yaw": 20, "x": 10, "y": 10, "z": 10}

with ReachyMini(media_backend="no_media") as mini:
    for dim, amp in AMPLITUDES.items():
        t0 = time.time()
        while (t := time.time() - t0) < DUREE:
            val = amp * math.sin(2 * math.pi * 0.3 * t)
            pose = create_head_pose(**{dim: val}, mm=True, degrees=True)
            ant = 0.4 * math.sin(2 * math.pi * t)
            mini.set_target(head=pose, antennas=[ant, -ant])
            time.sleep(DT)
    mini.goto_target(head=create_head_pose(), antennas=[0, 0], duration=1.0)