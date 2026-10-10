# WorldEditor4dMinerDemo

Code for editing worlds in 4D Miner Demo.

A tool designed for editing the game world in **4D Miner Demo**. It allows you to read, modify, and generate new chunks in 4D space using NumPy arrays.

---

## 🛠️ Setup and Configuration

1. **Create the environment file:**
   Copy the `.env.example` file and rename it to `.env`.
2. **Specify the game path:**
   Open the newly created `.env` file and set the variable to point to your game's root directory.

---

## 📐 4D Coordinates & Chunk Specifications

* **Coordinate Order:** In-game coordinates follow the strict sequence `(x, y, z, w)`, where **`y` represents the height (vertical axis)**.
* **Chunk Dimensions:** Every game chunk has a fixed 4D size of `(8, 128, 8, 8)`.
* **Chunk Notation:** Coordinates for the game chunks themselves are designated using uppercase letters: `X`, `Z`, and `W`.

---

## 🚀 How to Use

The core workflow consists of the following steps:
1. Create **4D NumPy arrays** (`numpy.ndarray` of dtype numpy.uint8) of the required shape and populate them with your desired block structures.
2. Modify and apply these changes to the game world using the `ChunkLoader` class.

### ⚠️ Important Note on Reading Chunks:
* **Existing Chunks:** To read a chunk from the game files, it must already physically exist there. This means you need to pre-generate it by manually modifying something within that chunk inside the game first.
* **On-the-Fly Generation (Flat World):** If you are working with a flat world, pre-generating chunks manually is not required. You can generate missing chunks directly from the code using `flat_space`.

