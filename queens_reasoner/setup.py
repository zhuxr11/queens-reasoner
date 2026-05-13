"""Setup utilities for Queens Reasoner."""

from queens_solver.setup import install_playwright_browsers


def install_playwright_browsers_(*args, **kwargs) -> None:
    """Install Playwright browsers for the Queens Reasoner.

    Delegates to ``queens_solver.setup.install_playwright_browsers``.

    Args:
        *args: Positional arguments forwarded to the underlying installer.
        **kwargs: Keyword arguments forwarded to the underlying installer.

    Returns:
        None
    """
    install_playwright_browsers(*args, **kwargs)
