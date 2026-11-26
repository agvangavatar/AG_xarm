"""ARIPersonTracker: ROS2 target source translating ARI vision tracking into canonical space."""

import logging
from .target_source import TargetSelectionCancelled, TargetSource

logger = logging.getLogger(__name__)


class ARIPersonTracker(TargetSource):
    """Subscribes to ROS2 tracking messages from ARI and returns canonical (x, y) targets."""

    def __init__(self, topic: str = "/ari/person_tracking/target") -> None:
        self._topic = topic
        self._latest: tuple[float, float] | None = None
        # Initialize ROS2 node / subscriber setup here during Session 15