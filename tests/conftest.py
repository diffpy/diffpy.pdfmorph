import json
from pathlib import Path

import numpy as np
import pytest


@pytest.fixture
def user_filesystem(tmp_path):
    base_dir = Path(tmp_path)
    home_dir = base_dir / "home_dir"
    home_dir.mkdir(parents=True, exist_ok=True)
    cwd_dir = base_dir / "cwd_dir"
    cwd_dir.mkdir(parents=True, exist_ok=True)

    home_config_data = {"username": "home_username", "email": "home@email.com"}
    with open(home_dir / "diffpyconfig.json", "w") as f:
        json.dump(home_config_data, f)

    yield tmp_path


@pytest.fixture
def heaviside():
    """The Heaviside function as a pytest fixture."""

    def heaviside_function(x, lb, ub):
        y = np.ones_like(x)
        y[x < lb] = 0.0
        y[x > ub] = 0.0
        return y

    return heaviside_function
