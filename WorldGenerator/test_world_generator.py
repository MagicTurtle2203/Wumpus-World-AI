import subprocess
import unittest
from pathlib import Path


class TestWorldGenerator(unittest.TestCase):
    def setUp(self):
        self.worlds = Path(__file__).parent / 'worlds'

    def cleanup_worlds(self):
        for file in self.worlds.iterdir():
            file.unlink()

    def test_generates_correct_number_of_files(self):
        subprocess.run(['python', f"{str(Path(__file__).parent / 'world_generator.py')}", '100', 'test_world'])
        try:
            self.assertEqual(len(list(self.worlds.iterdir())), 100)
        finally:
            self.cleanup_worlds()

    def test_file_is_4x4(self):
        subprocess.run(['python', f"{str(Path(__file__).parent / 'world_generator.py')}", '1', 'test_world'])
        try:
            with open(self.worlds / 'test_world_1.txt', 'r') as file:
                for line in file.readlines():
                    self.assertEqual(4, len(line.strip()))
        finally:
            self.cleanup_worlds()

    def test_start_point_is_always_0(self):
        subprocess.run(['python', f"{str(Path(__file__).parent / 'world_generator.py')}", '100', 'test_world'])
        try:
            for world in self.worlds.iterdir():
                with open(world) as file:
                    self.assertEqual('0', file.readlines()[3][0])
        finally:
            self.cleanup_worlds()

    def test_files_have_wumpus(self):
        subprocess.run(['python', f"{str(Path(__file__).parent / 'world_generator.py')}", '1', 'test_world'])
        try:
            with open(self.worlds / 'test_world_1.txt', 'r') as file:
                self.assertIn('W', file.read())
        finally:
            self.cleanup_worlds()

    def test_files_have_gold(self):
        subprocess.run(['python', f"{str(Path(__file__).parent / 'world_generator.py')}", '1', 'test_world'])
        try:
            with open(self.worlds / 'test_world_1.txt', 'r') as file:
                self.assertIn('G', file.read())
        finally:
            self.cleanup_worlds()


if __name__ == '__main__':
    unittest.main()
