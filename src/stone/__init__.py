import numpy as np
from stone.api import process
from stone.image import DEFAULT_TONE_PALETTE, show
from stone.utils import __version__, check_version

setattr(np, "asscalar", lambda x: np.asarray(x).item())

__all__ = ["process", "DEFAULT_TONE_PALETTE", "show", "__version__"]

check_version()
