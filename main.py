import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line arguments for running AI models")

    parser.add_argument("-f", "--filepath", help="Path to world file or directory containing world files",
                        action="store", type=str, required=True)
    parser.add_argument("-d", "--debug", help="Enable visualization of world", action="store_true")

    args = parser.parse_args()

    filepath = Path(args.filepath)
    debug = args.debug

    if filepath.exists():
        if filepath.is_dir():
            pass
        elif filepath.is_file():
            pass
    else:
        print("ERROR: Directory or file does not exist!")
