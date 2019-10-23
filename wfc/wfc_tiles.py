"""Breaks an image into consituant tiles."""
import numpy as np
from wfc_utilities import hash_downto

def image_to_tiles(img, tile_size):
    """
    Takes an images, divides it into tiles, return an array of tiles.
    >>> image_to_tiles(test_ns.img, test_ns.tile_size)
    array([[[[[255, 255, 255]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[255, 255, 255]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[255, 255, 255]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[255, 255, 255]]]],
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
           [[[[255, 255, 255]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]]],
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
           [[[[255, 255, 255]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[255,   0,   0]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]]],
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
           [[[[255, 255, 255]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]],
    <BLANKLINE>
    <BLANKLINE>
            [[[  0,   0,   0]]]]], dtype=uint8)
    """
    padding_argument = [(0,0),(0,0),(0,0)]
    for input_dim in [0,1]:
        padding_argument[input_dim] = (0, (tile_size - img.shape[input_dim]) % tile_size)
    img = np.pad(img, padding_argument, mode='constant')
    tiles = img.reshape((img.shape[0]//tile_size, 
                       tile_size,
                       img.shape[1]//tile_size,
                       tile_size,
                       img.shape[2]
                      )).swapaxes(1,2)
    return tiles



def make_tile_catalog(image_data, tile_size):
    channels = 3 # Number of color channels in the image
    tiles = image_to_tiles(image_data, tile_size)
    tile_list = np.array(tiles).reshape((tiles.shape[0] * tiles.shape[1], tile_size, tile_size, channels))
    code_list = np.array(hash_downto(tiles, 2)).reshape((tiles.shape[0] * tiles.shape[1]))
    tile_grid = np.array(hash_downto(tiles, 2), dtype=np.int64)
    unique_tiles = np.unique(tile_grid, return_counts=True)
    
    tile_catalog = {}
    for i,j in enumerate(code_list):
        tile_catalog[j] = tile_list[i]
    return tile_catalog, tile_grid, code_list, unique_tiles
    
def test_make_tile_catalog():
    import imageio
    filename = "images/samples/Red Maze.png"
    img = imageio.imread(filename)
    print(img)
    tc, tg, cl, ut = make_tile_catalog(img, 2)
    print(tc)
    print(tg)
    print(cl)
    print(ut)
    assert(ut[1][0] == 1)

if __name__ == "__main__":
    test_make_tile_catalog()