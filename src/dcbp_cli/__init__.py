"""
DCBP CLI - DC Blueprint pour Claude Code.

Système de mémoire persistante et workflows structurés.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dcbp-cli")
except PackageNotFoundError:
    __version__ = "0.0.0"
