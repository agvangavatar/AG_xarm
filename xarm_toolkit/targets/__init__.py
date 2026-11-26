"""Interchangeable target sources for xarm_toolkit."""
""" This file was made with the assistance of Claude"""

from .target_source import TargetSource, TargetSelectionCancelled
from .mock_click import MockClickTarget
from .ari_tracker import ARIPersonTracker

__all__ = [
    "TargetSource",
    "TargetSelectionCancelled",
    "MockClickTarget",
    "ARIPersonTracker",
]