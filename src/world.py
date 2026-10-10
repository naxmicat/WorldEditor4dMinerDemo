import shutil
from paths import WORLDS_PATH
import json


def copy_world(old, new):
    """
    Creates a copy of the selected world
    :param old: world name to copy
    :param new: name of a copy
    """

    old_path = WORLDS_PATH / old
    new_path = WORLDS_PATH / new

    shutil.copytree(old_path, new_path)

    info_path = new_path / "info.json"
    with open(info_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    data["name"] = new

    with open(info_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def clear_world(world_name, del_chests=False):
    """
    Delete all chunks from worlds folder
    :param world_name: world name
    :param del_chests:
        in any flat world if zero-chunk is missing the game automatically creates chests
        flag True is used for manually replacing zero-chunk with a flat chunk without chests
    """
    for item in (WORLDS_PATH / world_name / "chunks").iterdir():
        if item.is_file():
            item.unlink()
    if del_chests:
        from src.chunk_loader import ChunkLoader
        from src.utils.functions import flat_space

        loader = ChunkLoader(world_name)
        loader(0, 0, 0).replace(flat_space()).save(True)


def worlds_list(full_path=False):
    """
    :param full_path: True for paths, False for names
    :return: list of world names or paths
    """
    worlds = []
    for item in WORLDS_PATH.iterdir():
        if item.is_dir():
            worlds.append(item if full_path else item.name)
    return worlds
