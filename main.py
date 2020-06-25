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
            num_worlds = 0
            total_success = 0
            scores = []

            for worldpath in filepath.iterdir():
                num_worlds += 1

                if manual:
                    AI_type = manual_ai.ManualAI()
                else:
                    AI_type = ai.AI()

                world = world_parser.World(worldpath, AI_type, debug)
                success, score = world.run()

                if success:
                    total_success += 1

                scores.append(score)

            print("---------------Your agent's results:---------------")
            print(f"Success rate:\t{(total_success/num_worlds)*100:.2f}%")
            print(f"Average score:\t{sum(scores)/num_worlds:.2f}")

        elif filepath.is_file():
            if manual:
                AI_type = manual_ai.ManualAI()
            else:
                AI_type = ai.AI()

            world = world_parser.World(filepath, AI_type, debug)
            success, score = world.run()

            if success:
                print("WORLD COMPLETED")
            else:
                print("WORLD FAILED")
            print(f"SCORE: {score}")
    else:
        print("ERROR: Directory or file does not exist!")
