import numpy as np
from stone.api import process
from stone.image import DEFAULT_TONE_PALETTE, DEFAULT_TONE_LABELS, show

setattr(np, "asscalar", lambda x: np.asarray(x).item())

__all__ = ["process", "DEFAULT_TONE_PALETTE", "DEFAULT_TONE_LABELS", "show"]
