import unittest
from pathlib import Path

from action import ActionType
from world_parser import World


class TestWorldParser(unittest.TestCase):
    def test_created_board_matches_text_file(self):
        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("0000\n")
            file.write("W00P\n")
            file.write("000G\n")

        try:
            world = World(test_file)

            # coordinates should be (row, column)
            self.assertEqual(world.board[0][0], World.TileType.BLANK)
            self.assertEqual(world.board[2][0], World.TileType.WUMPUS)
            self.assertEqual(world.board[2][3], World.TileType.PIT)
            self.assertEqual(world.board[3][3], World.TileType.GOLD)
        finally:
            test_file.unlink()

    def test_agent_receives_correct_senses1(self):
        class AI:
            def __init__(self):
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses
                return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("000G\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("00WP\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, False, False])
        finally:
            test_file.unlink()

    def test_agent_receives_correct_senses2(self):
        class AI:
            def __init__(self):
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses
                return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0W0G\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [True, False, False, False, False])
        finally:
            test_file.unlink()

    def test_agent_receives_correct_senses3(self):
        class AI:
            def __init__(self):
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses
                return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("000G\n")
            file.write("P000\n")
            file.write("W000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, True, False, False, False])
        finally:
            test_file.unlink()

    def test_agent_receives_correct_senses4(self):
        class AI:
            def __init__(self):
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses
                return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0W0G\n")
            file.write("P000\n")
            file.write("0000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [True, True, False, False, False])
        finally:
            test_file.unlink()

    def test_agent_senses_glitter_when_on_gold_tile(self):
        class AI:
            def __init__(self):
                self.received_senses = None
                self.move_count = 0

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0G0W\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, True, False, False])
        finally:
            test_file.unlink()

    def test_agent_turns_correctly1(self):
        class AI:
            def __init__(self):
                self.move_count = 0

            def get_action(self, senses):
                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0W0G\n")
            file.write("P000\n")
            file.write("0000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(world.agent.direction_index, 3)
        finally:
            test_file.unlink()

    def test_agent_turns_correctly2(self):
        class AI:
            def __init__(self):
                self.move_count = 0

            def get_action(self, senses):
                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.TURNRIGHT
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0W0G\n")
            file.write("P000\n")
            file.write("0000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(world.agent.direction_index, 1)
        finally:
            test_file.unlink()

    def test_agent_moves_to_correct_location1(self):
        class AI:
            def __init__(self):
                self.move_count = 0

            def get_action(self, senses):
                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("P000\n")
            file.write("0000\n")
            file.write("0W0G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual((world.agent.X, world.agent.Y), (1, 0))
            self.assertEqual(world.agent.direction_index, 0)
        finally:
            test_file.unlink()

    def test_agent_moves_to_correct_location2(self):
        class AI:
            def __init__(self):
                self.move_count = 0

            def get_action(self, senses):
                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0W0G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual((world.agent.X, world.agent.Y), (0, 1))
            self.assertEqual(world.agent.direction_index, 3)
        finally:
            test_file.unlink()

    def test_agent_moves_to_correct_location3(self):
        class AI:
            def __init__(self):
                self.move_count = 0

            def get_action(self, senses):
                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 2:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 3:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 4:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("w000\n")
            file.write("0000\n")
            file.write("0G00\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual((world.agent.X, world.agent.Y), (1, 3))
            self.assertEqual(world.agent.direction_index, 3)
        finally:
            test_file.unlink()

    def test_agent_dies_when_walking_into_pit(self):
        class AI:
            def get_action(self, senses):
                return ActionType.FORWARD

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0P0G\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            score = world.run()

            self.assertLess(score, -1000)
        finally:
            test_file.unlink()

    def test_agent_dies_when_walking_into_wumpus(self):
        class AI:
            def get_action(self, senses):
                return ActionType.FORWARD

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0W0G\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            score = world.run()

            self.assertLess(score, -1000)
        finally:
            test_file.unlink()

    def test_agent_receives_bump_when_walking_into_a_wall1(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.TURNRIGHT
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0W0G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, True, False])
        finally:
            test_file.unlink()

    def test_agent_receives_bump_when_walking_into_a_wall2(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count < 2:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 2:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0W0G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, True, False])
        finally:
            test_file.unlink()

    def test_agent_receives_bump_when_walking_into_a_wall3(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count < 4:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("0W0G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, True, False])
        finally:
            test_file.unlink()

    def test_agent_receives_bump_when_walking_into_a_wall4(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count < 5:
                    self.move_count += 1
                    return ActionType.FORWARD
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("000W\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("000G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, True, False])
        finally:
            test_file.unlink()

    def test_wumpus_screams_when_shot_with_arrow1(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.SHOOT
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("000W\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("000G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, False, True])
        finally:
            test_file.unlink()

    def test_wumpus_screams_when_shot_with_arrow2(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.SHOOT
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("W000\n")
            file.write("0000\n")
            file.write("000G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, False, True])
        finally:
            test_file.unlink()

    def test_wumpus_screams_when_shot_with_arrow3(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 2:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 3:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 4:
                    self.move_count += 1
                    return ActionType.SHOOT
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("W000\n")
            file.write("0000\n")
            file.write("000G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, False, True])
        finally:
            test_file.unlink()

    def test_wumpus_screams_when_shot_with_arrow4(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 2:
                    self.move_count += 1
                    return ActionType.TURNRIGHT
                elif self.move_count == 3:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 4:
                    self.move_count += 1
                    return ActionType.TURNRIGHT
                elif self.move_count == 5:
                    self.move_count += 1
                    return ActionType.SHOOT
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0W00\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("000G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, False, True])
        finally:
            test_file.unlink()

    def test_agent_cannot_shoot_arrow_twice(self):
        class AI:
            def __init__(self):
                self.move_count = 0
                self.received_senses = None

            def get_action(self, senses):
                self.received_senses = senses

                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.SHOOT
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.TURNLEFT
                elif self.move_count == 2:
                    self.move_count += 1
                    return ActionType.SHOOT
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0000\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("W00G\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            world.run()

            self.assertEqual(AI_agent.received_senses, [False, False, False, False, False])
        finally:
            test_file.unlink()

    def test_agent_can_grab_gold_and_exit(self):
        class AI:
            def __init__(self):
                self.move_count = 0

            def get_action(self, senses):
                if self.move_count == 0:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 1:
                    self.move_count += 1
                    return ActionType.GRAB
                elif self.move_count == 2:
                    self.move_count += 1
                    return ActionType.TURNRIGHT
                elif self.move_count == 3:
                    self.move_count += 1
                    return ActionType.TURNRIGHT
                elif self.move_count == 4:
                    self.move_count += 1
                    return ActionType.FORWARD
                elif self.move_count == 5:
                    self.move_count += 1
                    return ActionType.CLIMB
                else:
                    return 0

        test_file = Path(__file__).parent / 'test_world.txt'

        with open(test_file, 'w') as file:
            file.write("0G00\n")
            file.write("0000\n")
            file.write("0000\n")
            file.write("000W\n")

        try:
            AI_agent = AI()
            world = World(test_file, AI_agent)
            score = world.run()

            self.assertGreater(score, 900)
        finally:
            test_file.unlink()


if __name__ == '__main__':
    unittest.main()
