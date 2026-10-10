import json
from src.utils.rle import *
from src.utils.functions import flat_space
from paths import WORLDS_PATH, Path


class Chunk:
    default_chunk = flat_space()    # used as the default state if chunk file is missing

    def __init__(self, X:int, Z: int, W: int, bin_fp: Path, json_fp: Path):
        """
        Chunk class is used for:
            - loading current chunk state from game files
            - editing / replacing current state
            - saving / deleting chunk
        """
        self.X, self.Z, self.W = X, Z, W
        self.bin_fp = bin_fp
        self.json_fp = json_fp
        self.name = f"Chunk {(X, Z, W)}"
        self.state = None

    def load(self, logging=False):
        """
        loads the chunk from game files
        """
        self.state = self._load(logging)
        return self

    def required_loading(self):
        """
        loads the state if needed
        """
        if self.state is None:
            self.load()

    def is_able_to_load(self) -> bool:
        """
        checks if the chunk game file exists
        """
        try:
            with open(self.bin_fp, "rb") as f:
                return True
        except FileNotFoundError:
            return False

    def _load(self, logging=False):
        """
        uses 'unpack_rle' function to create 4d numpy array and returns if chunk file exists
        else returns copy of the 'default chunk'
        """
        try:
            with open(self.bin_fp, "rb") as f:
                arr = unpack_rle(f.read())

            if logging:
                print(f"{self.name} has been loaded")

            return arr

        except FileNotFoundError:
            print(f"Warning: missing {self.name}")
            return self.default_chunk.copy()

    def update(
            self,
            new_state: np.array,
            mask: np.array,
            logging=False
    ):
        """
        updates the 'state' by mask
        :param new_state: updated state
        :param mask: mask of blocks to replace
        """
        self.required_loading()
        self.state[mask] = new_state[mask]
        if logging:
            print(f"{self.name} has been updated")
        return self

    def add(self, new_state, logging=False):
        """
        adds new blocks to the 'state' where the blocks are missing
        :param new_state: updated state
        """
        self.required_loading()
        return self.update(new_state=new_state, mask=(self.state == 0), logging=logging)

    def insert(self, new_state, logging=False):
        """
        inserts the new blocks that are no empty in the 'state'
        :param new_state: update state
        """
        return self.update(new_state=new_state, mask=new_state != 0, logging=logging)

    def replace(self, new_state, logging=False):
        """
        sets the 'state' to be new state
        :param new_state: updated state
        :param logging:
        :return:
        """
        self.state = new_state.copy()
        if logging:
            print(f"{self.name} has been replaced")
        return self

    def cut(self, mask, logging=False):
        """
        cuts the 'state' by mask (delete blocks)
        :param mask: mask to cut
        """
        self.required_loading()
        self.state[mask] = 0
        if logging:
            print(f"{self.name} has been cutted")
        return self

    def save(self, logging=False):
        """
        saves the chunk to the game files
        """
        with open(self.bin_fp, "wb") as f:
            f.write(bytes(pack_rle(self.state)))

        with open(self.json_fp, "w", encoding="utf-8") as f:
            json.dump([], f)

        if logging:
            print(f"{self.name} has been saved")

        return self

    def delete(self, logging=False):
        """
        deletes bin and json file of a chunk from world folder
        :param logging:
        :return:
        """
        self.bin_fp.unlink(missing_ok=True)
        self.json_fp.unlink(missing_ok=True)

        if logging:
            print(f"{self.name} has been deleted")
        return self


class ChunkLoader:
    def __init__(self, world_name: str):
        """
        ChunkLoader class is used to create Chunk class objects
        :param world_name: world name (str)
        """
        self.chunks_path = WORLDS_PATH / world_name / "chunks"

    def __call__(self, X: int, Z: int, W: int) -> Chunk:
        """
        :return: Chunk class object of (X,Z,W) coordinates
        """
        return Chunk(
            X, Z, W,
            self.chunks_path / f"x{X}z{Z}w{W}.bin",
            self.chunks_path / f"x{X}z{Z}w{W}.json"
        )



