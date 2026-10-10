import numpy as np
from numba import njit
from src.utils.functions import *
from src.utils.rle import *
from src.chunk_loader import *
from src.world import *
from src.blocks import *
from paths import *

np.set_printoptions(threshold=np.inf, linewidth=200)
