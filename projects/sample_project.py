from import_all import *


def main():
    """
    Let's assume we have a flat world named 'StoneTesseract'

    This function:
    - Deletes chests in (0, 0, 0) chunk
    - Creates 8x8x8x8 tesseract of stone in (0, 0, 0) chunk and snow in (1, 0, 0) chunk on surface (y=5+)
    """
    WN = 'StoneTesseract'
    clear_world(WN, del_chests=True)
    space = empty_space(X=2)    # (16, 128, 8, 8)
    space[:8, 5:13, :, :] = STONE
    space[8:, 5:13, :, :] = SNOW

    loader = ChunkLoader(WN)
    for X, Z, W, state in split_into_chunks(space):
        loader(X, Z, W).add(state).save(logging=True)


if __name__ == "__main__":
    main()
