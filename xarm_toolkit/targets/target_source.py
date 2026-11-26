# src/xarm_toolkit/targets/target_source.py
"""Abstract base class for everything that can supply a pointing target."""

""" This file used Gemini Notebook LLM as a guide """

import abc


class TargetSelectionCancelled(RuntimeError):
    """Raised when the user aborts target selection (e.g. closes the window)."""


class TargetSource(abc.ABC):
    """A source of ``(x, y)`` pointing targets."""

    @abc.abstractmethod
    def get_target(self) -> tuple[float, float]:
        """Block until a target is available, then return it as ``(x, y)``.

        May raise :class:`TargetSelectionCancelled` if the user aborts.
        """
        raise NotImplementedError