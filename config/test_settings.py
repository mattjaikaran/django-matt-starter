"""Test settings - uses SQLite by default."""

import os

# Force SQLite for tests
os.environ["USE_SQLITE"] = "true"

from config.settings import *  # noqa: F401, F403, E402
