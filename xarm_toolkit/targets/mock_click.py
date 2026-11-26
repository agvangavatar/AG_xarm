# src/xarm_toolkit/targets/mock_click.py
"""MockClickTarget: simulates an external tracker using mouse input."""

""" This file used Gemini Notebook LLM as a guide """

import logging

import pygame

from .target_source import TargetSelectionCancelled, TargetSource

logger = logging.getLogger(__name__)


class MockClickTarget(TargetSource):
    """Return the pixel position of a mouse click in a Pygame window."""

    def __init__(
        self,
        title: str = "Click a target",
        window_size: tuple[int, int] = (800, 600),
    ) -> None:
        # GIVEN: store settings; warn if the size breaks the shared contract.
        self._title = title
        self._size = window_size
        if window_size != (800, 600):
            logger.warning(
                "Window %s is not canonical: clicks will not match the "
                "shared target space.", window_size,
            )

    def get_target(self) -> tuple[float, float]:
        """Open window, blit instructions, block for one click, and return (x, y)."""
        pygame.init()
        try:
            screen = pygame.display.set_mode(self._size)
            pygame.display.set_caption(self._title)
            clock = pygame.time.Clock()

            self._draw_instructions(screen)
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    # Abort on window close (QUIT) or Escape key
                    if event.type == pygame.QUIT:
                        raise TargetSelectionCancelled("Window closed by user.")
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        raise TargetSelectionCancelled("Selection cancelled with Escape.")
                    
                    # Return target on mouse click
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        return float(x), float(y)

                clock.tick(60)
        finally:
            pygame.quit()

    @staticmethod
    def _draw_instructions(screen: pygame.Surface) -> None:
        """Blit a one-line hint to the user."""
        screen.fill((30, 30, 30))
        if pygame.font.get_init():
            font = pygame.font.SysFont(None, 24)
            text = font.render("Click anywhere to aim arm (ESC/Close to quit)", True, (255, 255, 255))
            screen.blit(text, (20, 20))