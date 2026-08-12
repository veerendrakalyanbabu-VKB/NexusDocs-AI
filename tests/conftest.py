"""Shared pytest fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def sample_txt_path() -> Path:
    return Path("data/sample/portfolio-overview.txt")
