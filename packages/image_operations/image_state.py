from dataclasses import dataclass
import numpy as np


@dataclass
class ImageState:
    frame_counter: np.uint64
