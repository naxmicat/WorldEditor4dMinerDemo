import numpy as np
from numba import njit


def full_chunks_blocks(blocks: int) -> int:
    """
    :param blocks: number of blocks
    :return: the number of chunks required to hold a specified number of blocks
    """
    return int(np.ceil(blocks / 8))



def full_chunks(shape: tuple) -> int:
    """
    :param shape: shape of an array
    :return: the number of chunks in 3 directions required to hold a specified shape
    """
    return full_chunks_blocks(blocks[0]),  full_chunks_blocks(blocks[2]), full_chunks_blocks(blocks[3])

def zeros(shape) -> np.ndarray:
    """
    short name of the numpy function with dtype = np.uint8
    """
    return np.zeros(shape, dtype=np.uint8)


def ones(shape) -> np.ndarray:
    """
    short name of the numpy function with dtype = np.uint8
    """
    return np.ones(shape, dtype=np.uint8)


def full(shape, value) -> np.ndarray:
    """
    short name of the numpy function with dtype = np.uint8
    """
    return np.full(shape, value, dtype=np.uint8)


def empty_space(X=1, Z=1, W=1) -> np.ndarray:
    """
    :return: np.zeros with specified size of chunks
    """
    return np.zeros((X*8, 128, Z*8, W*8), dtype=np.uint8)


def flat_space(x=1, z=1, w=1) -> np.ndarray:
    """
    flat chunk contains:
        - height (127-5) is empty
        - height (4) is the grass block
        - height (2-3) are dirt blocks
        - height (0-1) are stone blocks
     :return: flat space block with specified size of chunks
     """
    space = empty_space(x, z, w)
    space[:, 2] = 3
    space[:, 2:4] = 2
    space[:, 4] = 1
    return space


@njit(fastmath=True, boundscheck=False, cache=True)
def _extract_chunk(
        space: np.ndarray,
        cx: int,
        cz: int,
        cw: int,
        x_start: int,
        z_start: int,
        w_start: int,
        x_size: int,
        z_size: int,
        w_size: int
) -> np.ndarray:
    """
    extracts spectified chunk from space
    """
    chunk_x_world = cx * 8
    chunk_z_world = cz * 8
    chunk_w_world = cw * 8

    x_start_local = max(0, chunk_x_world - x_start)
    x_end_local = min(x_size, chunk_x_world + 8 - x_start)
    z_start_local = max(0, chunk_z_world - z_start)
    z_end_local = min(z_size, chunk_z_world + 8 - z_start)
    w_start_local = max(0, chunk_w_world - w_start)
    w_end_local = min(w_size, chunk_w_world + 8 - w_start)

    chunk_data = space[x_start_local:x_end_local, :,
                 z_start_local:z_end_local,
                 w_start_local:w_end_local]

    if (chunk_data.shape[0] == 8 and
            chunk_data.shape[2] == 8 and
            chunk_data.shape[3] == 8):
        return chunk_data
    else:
        full_chunk = np.zeros((8, 128, 8, 8), dtype=np.uint8)

        x_offset = (x_start_local + x_start) % 8
        z_offset = (z_start_local + z_start) % 8
        w_offset = (w_start_local + w_start) % 8

        full_chunk[x_offset:x_offset + chunk_data.shape[0],
        :,
        z_offset:z_offset + chunk_data.shape[2],
        w_offset:w_offset + chunk_data.shape[3]] = chunk_data

        return full_chunk


def split_into_chunks(
        space: np.ndarray,
        x_start: int = 0,
        z_start: int = 0,
        w_start: int = 0
):
    """
    a generator used to split space into chunks.

    it is assumed that (x_start, 0, z_start, w_start) world corrdinates
    are correspond to the (0, 0, 0, 0) coordinates of the 'space'.
    :return: (X, Z, Y) world chunk coordinates and its сutted 'space' version
    """
    x_size, _, z_size, w_size = space.shape
    x_min, z_min, w_min = x_start, z_start, w_start
    x_max, z_max, w_max = x_start + x_size, z_start + z_size, w_start + w_size

    for cx in range(x_min // 8, (x_max + 7) // 8):
        for cz in range(z_min // 8, (z_max + 7) // 8):
            for cw in range(w_min // 8, (w_max + 7) // 8):
                yield cx, cz, cw, _extract_chunk(space, cx, cz, cw, x_start, z_start, w_start, x_size, z_size, w_size)


def get_mapping(ids: np.ndarray, p=None) -> callable:
    """
    used to create mapping function that maps random noise to block ids
    :param ids: array of block ids
    :param p: probabilities. if p is None it uses uniform distribution
    :return: mapping fuction
    """
    if p is None:
        cum_p = np.arange(1, len(ids)+1) / len(ids)
    else:
        cum_p = np.cumsum(p)

    def f(noise: np.ndarray) -> np.ndarray:
        indices = np.searchsorted(cum_p, noise)
        return ids[indices]

    return f
