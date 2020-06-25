import argparse
from pathlib import Path

from AI import ai, manual_ai, world_parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line arguments for running AI models")

    parser.add_argument("-f", "--filepath", help="Path to world file or directory containing world files",
                        action="store", type=str, required=True)
    parser.add_argument("-m", "--manual", help="Send commands manually", action="store_true")
    parser.add_argument("-d", "--debug", help="Enable visualization of world", action="store_true")

    args = parser.parse_args()

    filepath = Path(args.filepath)
    manual = args.manual
    debug = args.debug

    if filepath.exists():
        if filepath.is_dir():
            pass
        elif filepath.is_file():
            if manual:
                AI = manual_ai.ManualAI()
            else:
                AI = ai.AI()

            world = world_parser.World(filepath, AI, debug)
            success, score = world.run()

            if success:
                print("WORLD COMPLETED")
            else:
                print("WORLD FAILED")
            print(f"SCORE: {score}")
    else:
        print("ERROR: Directory or file does not exist!")
