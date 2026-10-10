import numpy as np
from numba import njit


@njit(fastmath=True, boundscheck=False, cache=True)
def pack_rle(arr):
    """
    compresses 4D array chunk using Run-Length Encoding (RLE) into uint8 format.

    flattens the input array and encodes sequences of identical elements into
    (value, count) pairs.
    the maximum sequence length per pair is capped at 255.
    """
    arr = arr.flatten()
    n = len(arr)
    output = np.empty(n * 2, dtype=np.uint8)

    i = 0
    out_idx = 0
    while i < n:
        block_id = arr[i]
        count = 1
        i += 1
        while i < n and arr[i] == block_id and count < 255:
            count += 1
            i += 1

        output[out_idx] = block_id
        output[out_idx + 1] = count
        out_idx += 2

    return output[:out_idx]


@njit(fastmath=True, cache=True, boundscheck=False)
def unpack_rle(compressed):
    """
    decompresses uint8 RLE-encoded array into 4D array chunk

    decodes sequential (value, count) pairs and reconstructs the data,
    automatically reshaping the final output into 8x128x8x8 array.
    """
    blocks = np.empty(65536, dtype=np.uint8)
    i = end = 0

    while i < len(compressed):
        start = end
        block_id = compressed[i]
        count = compressed[i + 1]
        end += count
        blocks[start:end] = block_id
        i += 2

    return blocks.reshape(8, 128, 8, 8)