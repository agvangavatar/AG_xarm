"""" This file was made with assistance from LLLM """

import xarm_sim as xarm
from xarm_toolkit.targets.mock_click import MockClickTarget
from xarm_toolkit.targets.target_source import TargetSelectionCancelled

arm = xarm.Controller('USB')
target_source = MockClickTarget()


def to_servo(x, y):
    pan = int(x / 800 * 1000)           # left/right -> servo 6 (shoulder pan)
    lift = int((1 - y / 600) * 1000)    # up/down    -> servo 5 (shoulder lift)
    return max(0, min(1000, pan)), max(0, min(1000, lift))


while True:
    try:
        x, y = target_source.get_target()   # blocks until one click
    except TargetSelectionCancelled:
        break
    pan, lift = to_servo(x, y)
    print(f"clicked ({x:.0f}, {y:.0f}) -> pan {pan}, lift {lift}")
    arm.setPosition([[6, pan], [5, lift]], duration=500, wait=True)