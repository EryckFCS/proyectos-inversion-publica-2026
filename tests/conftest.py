from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture(autouse=True)
def reset_lpi_config_singleton():
    from src.core.config import LPIConfig

    LPIConfig._instance = None
    yield
    LPIConfig._instance = None
