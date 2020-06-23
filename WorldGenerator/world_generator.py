import argparse
import random
from pathlib import Path


def generate_worlds(num_files: int, base_filename: str) -> None:
    """
    Generates N number of random worlds specified by num_files.
    Each world will be a text file named base_filename followed by a number.
    """
    if not (Path(__file__).parent / 'worlds').exists():
        (Path(__file__).parent / 'worlds').mkdir()

    for num in range(1, num_files + 1):
        generate_world_file(f"{base_filename}_{num}.txt")


def generate_world_file(filename: str) -> None:
    """
    Generates a single Wumpus World based on the description in Artificial Intelligence: A Modern Approach
    by Peter Norvig and Stuart J. Russell. The world is stored in a 4x4 grid in a text file. In a world, only
    1 wumpus and 1 gold can exist, but there can be multiple pits. Pits appear randomly with a probability of 0.2.
    The starting point, the lower left hand corner, is always left empty.

    Symbols:
        0 = empty
        W = wumpus
        G = gold
        P = pit

    Example world:
        000P
        WGP0
        0000
        00P0
    """
    world_path = Path(__file__).parent / 'worlds' / filename

    world = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

    for idx, _ in enumerate(world[1:], 1):
        if random.random() < 0.2:   # Generate pit with probability of 0.2
            world[idx] = 'P'

    wumpus, gold = random.sample(range(1, len(world)), 2)   # Grab two tiles to mark as wumpus and gold
    world[wumpus] = 'W'
    world[gold] = 'G'

    with open(world_path, 'w') as file:
        for line in [world[i:i + 4] for i in range(0, len(world), 4)]:    # Splits list into 4 equal segments
            file.write(''.join(line) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process command line arugments for world generation")

    parser.add_argument("num_files", help="Number of world files to create", action="store", type=int)
    parser.add_argument("base_filename", nargs='?', help="Base filename", action="store", type=str, default="world")

    args = parser.parse_args()

    num_files = args.num_files
    base_filename = args.base_filename

    generate_worlds(num_files, base_filename)
